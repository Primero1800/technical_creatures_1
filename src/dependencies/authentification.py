import os
from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException, Depends, Form
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param
from starlette import status
from starlette.requests import Request

from src.model.AuthJWT import TokenInfo
from src.utils.errors import Missing
from src.service import user as service_user
from src.settings import settings, oauth2_scheme


async def unauthed(detail="Incorrect username or password"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_token_from_request(request: Request):
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        await unauthed(
            detail="Not authenticated"
        )
    return param


async def generate_token_for_user(username: str = Form(), password: str = Form()):
    try:
        user = service_user.auth_user(username, password)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    if not user:
        await unauthed()
    access_token = service_user.create_access_token(
        data={"sub": user.name},
        expires=timedelta(minutes=settings.auth_jwt.access_token_expire_minutes),
    )
    refresh_token = service_user.create_access_token(
        data={'sub': user.name},
        expires=timedelta(minutes=settings.auth_jwt.refresh_token_expire_minutes),
        token_type=settings.auth_jwt.refresh_token_type,
    )
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def login_required(
        # token: HTTPAuthorizationCredentials | str = Depends(HTTP_BEARER)
        token: str = Depends(oauth2_scheme)
) -> dict:
    try:
        user_dict = service_user.get_current_user(token)
        user = user_dict['user']
    except KeyError:
        await unauthed(
            detail=f"Not authenticated",
        )
    except jwt.PyJWTError as error:
        await unauthed(
            detail=f"Not authenticated, {error}",
        )
    return user
