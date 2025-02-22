import os
from datetime import timedelta

from fastapi import HTTPException, Depends
from fastapi.security.utils import get_authorization_scheme_param
from starlette import status
from starlette.requests import Request

from src.errors import Missing
from src.service import user as service_user


def unauthed(detail="Incorrect username or password"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_token_from_request(request: Request):
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        unauthed(
            detail="Not authenticated"
        )
    return param


def generate_token_for_user(username: str, password: str):
    try:
        user = service_user.auth_user(username, password)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    if not user:
        unauthed()
    expires = timedelta(minutes=float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = service_user.create_access_token(
        data={
            "sub": user.name,
        },
        expires=expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def login_required(token: str = Depends(get_token_from_request)) -> dict:
    try:

        user_dict = service_user.get_current_user(token)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! USER_DICT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', user_dict)
        user = user_dict['user']
    except KeyError:
        unauthed(
            detail="Not authenticated",
        )
    return user
