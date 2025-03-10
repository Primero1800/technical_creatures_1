import os

import jwt

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

from src.utils.errors import Missing, Duplicate, Validation, JWTError

router = APIRouter(prefix="/user")


@router.post("/token", response_model=TokenInfo, tags=[Tags.AUTH_TAG,])
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Получение имени пользователя и пароля
    из формы OAuth, возврат токена доступа"""
    return await auth_depends.generate_token_for_user(
        username=form_data.username,
        password=form_data.password
    )


# http http://127.0.0.1:8000/user/token  "Authorization: Bearer <token>"
@router.get("/token",
    openapi_extra={
        "security": [{"bearerAuth": []}],  # Используем схему "bearerAuth"
        "description": "Возврат текущего токена доступа.  Требуется заголовок Authorization: Bearer <token>",
    },
    tags=[Tags.AUTH_TAG,]
)
async def get_access_token(
        request: Request,
        # token: HTTPAuthorizationCredentials | str = Depends(HTTP_BEARER)
        token: str = Depends(oauth2_scheme)
) -> dict:
    """Возврат текущего токена доступа"""
    try:
        return {
            "token": token, 'data': service.get_current_user(token), 'headers': dict(request.headers)
        }
    except jwt.PyJWTError as error:
        detail = error.msg if hasattr(error, 'msg') else f"{error}"
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


@router.post(
    "/refresh", status_code=status.HTTP_200_OK,
    include_in_schema=False, response_model=TokenInfo,
    response_model_exclude_none=True,
)
@router.post(
    "/refresh/", status_code=status.HTTP_200_OK,
    tags=[Tags.AUTH_TAG], response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def refresh_access_token(token_info: TokenInfo = Depends(auth_depends.generate_token_for_refresh)) -> TokenInfo:
    return token_info


@router.get("/test_jwtauth", tags=[Tags.TECH_TAG,])
async def get_test_jwt_auth(user=Depends(auth_depends.login_required)):
    return user


@router.get(
    "/user_by_token", tags=[Tags.TECH_TAG,],
    status_code=status.HTTP_200_OK,
    description=f"Get information from token of any type",
)
async def get_user_info_from_any_token(token: str = Depends(oauth2_scheme)):
    try:
        return service.get_current_user(
            token_cred=token,
            need_token_type_validation=False
        )
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.msg)


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
