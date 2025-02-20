from requests.structures import CaseInsensitiveDict
import os
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request

from src.model.user import User, UserUpdate

from dotenv import load_dotenv

load_dotenv()

if os.getenv("FAKE") == str(True):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! FAKE SERVICE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    import src.mock.user as service
else:
    import src.service.user as service

from src.errors import Missing, Duplicate, Validation

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/user")

# --- Новые данные auth
# Эта зависимость создает сообщение в каталоге
# "/user/token" (из формы с именем пользователя и паролем)
# и возвращает токен доступа.
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")


async def unauthed(detail="Incorrect username or password"):
    raise HTTPException(
        status_code=401,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


# К этой конечной точке направляется любой вызов,
# содержащий зависимость oauth2_dep():
@router.post("/token")
async def create_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """Получение имени пользователя и пароля
    из формы OAuth, возврат токена доступа"""
    try:
        user = service.auth_user(form_data.username, form_data.password)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    if not user:
        await unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={
            "sub": user.name,
        },
        expires=expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# http http://127.0.0.1:8000/user/token  "Authorization: Bearer <token>"
@router.get("/token", openapi_extra={
        "security": [{"bearerAuth": []}],  # Используем схему "bearerAuth"
        "description": "Возврат текущего токена доступа.  Требуется заголовок Authorization: Bearer <token>",
    }
)
async def get_access_token(request: Request, token: str = Depends(oauth2_dep)) -> dict:
    """Возврат текущего токена доступа"""
    print("HEADERS: ", request.headers)
    return {"token": token, 'data': service.get_current_user(token), 'headers': dict(request.headers)}


async def login_required(user_data: dict = Depends(get_access_token)):
    try:
        user = user_data['data']['user']
    except KeyError:
        await unauthed(
            detail="Not authenticated",
        )
    return user


@router.get("/test_jwtauth")
async def get_test_jwt_auth(request: Request, user = Depends(login_required)):
    return user



@router.get("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all() -> list[User]:
    return service.get_all()


@router.get("/{name}", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.get("/{name}/", status_code=status.HTTP_200_OK)
async def get_one(name) -> User | None:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("", status_code=status.HTTP_201_CREATED, include_in_schema=False)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=400, detail=exc.msg)


@router.patch("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.patch("/", status_code=status.HTTP_200_OK)
async def modify(name: str, user: UserUpdate) -> User:
    try:
        return service.modify(name, user.model_dump(exclude_unset=True))
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    except (Validation, Duplicate) as exc:
        raise HTTPException(status_code=400, detail=exc.msg)


@router.put("", status_code=status.HTTP_200_OK, include_in_schema=False)
@router.put("/", status_code=status.HTTP_200_OK)
async def replace(user: User) -> User:
    try:
        return service.replace(user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
@router.delete("/{name}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
