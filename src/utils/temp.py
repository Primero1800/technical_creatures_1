from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request


class MyOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        print('HELLO FROM INSIDE OAUTH2')
        print(request.headers)
        return await super().__call__(request)

