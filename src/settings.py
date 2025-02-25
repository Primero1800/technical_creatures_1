from pathlib import Path

from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from pydantic.v1 import BaseSettings
from src.model.AuthJWT import AuthJWT


BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT(
        private_key=BASE_DIR / "config" / "certs" / "jwt-private.pem",
        public_key=BASE_DIR / "config" / "certs" / "jwt-public.pem",
        algorithm="RS256",
    )


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# HTTP_BEARER = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

settings = Settings()