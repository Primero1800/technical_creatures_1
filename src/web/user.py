import os
import src.dependencies.authentification as auth_depends

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request

from src.model.AuthJWT import TokenInfo
from src.settings import oauth2_scheme
from src.config.swagger_config import Tags
from src.model.user import User, UserUpdate


if os.getenv("FAKE") == str(True):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! FAKE SERVICE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    import src.mock.user as service
else:
    import src.service.user as service

from src.utils.errors import Missing, Duplicate, Validation


router = APIRouter(prefix="/user")

# --- Новые данные auth
# Эта зависимость создает сообщение в каталоге
# "/user/token" (из формы с именем пользователя и паролем)
# и возвращает токен доступа.
# oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")
oauth2_dep = oauth2_scheme


# К этой конечной точке направляется любой вызов,
# содержащий зависимость oauth2_dep():
@router.post("/token", response_model=TokenInfo, tags=[Tags.AUTH_TAG,])
async def create_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """Получение имени пользователя и пароля
    из формы OAuth, возврат токена доступа"""
    return await auth_depends.generate_token_for_user(
        username=form_data.username,
        password=form_data.password
    )


# http http://127.0.0.1:8000/user/token  "Authorization: Bearer <token>"
@router.get("/token",
    openapi_extra={
        # "security": [{"bearerAuth": []}],  # Используем схему "bearerAuth"
        "description": "Возврат текущего токена доступа.  Требуется заголовок Authorization: Bearer <token>",
    },
    tags=[Tags.AUTH_TAG,]
)
async def get_access_token(request: Request, token: str = Depends(auth_depends.get_token_from_request)) -> dict:
    """Возврат текущего токена доступа"""
    return {"token": token, 'data': service.get_current_user(token), 'headers': dict(request.headers)}


@router.get("/test_jwtauth", tags=[Tags.TECH_TAG,])
async def get_test_jwt_auth(user=Depends(auth_depends.login_required)):
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
@router.post("/register", status_code=status.HTTP_201_CREATED, tags=[Tags.AUTH_TAG]) # registration root
async def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as exc:
        raise HTTPException(status_code=400, detail=exc.msg)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenInfo,
    tags=[Tags.AUTH_TAG,]) # login root
async def login(token_info: TokenInfo = Depends(auth_depends.generate_token_for_user)) -> TokenInfo:
    return token_info


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
