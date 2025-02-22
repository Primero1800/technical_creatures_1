from fastapi import HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from starlette import status
from starlette.requests import Request


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
