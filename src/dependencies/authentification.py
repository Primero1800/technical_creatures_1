from fastapi import HTTPException, Depends
from fastapi.security.utils import get_authorization_scheme_param
from starlette import status
from starlette.requests import Request

from src.service import user as service_user


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


async def login_required(token: str = Depends(get_token_from_request)) -> dict:
    try:

        user_dict = service_user.get_current_user(token)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! USER_DICT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', user_dict)
        user = user_dict['user']
    except KeyError:
        await unauthed(
            detail="Not authenticated",
        )
    return user
