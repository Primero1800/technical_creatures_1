import os
from pathlib import Path

from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from pydantic.v1 import BaseSettings
from src.model.AuthJWT import AuthJWT

from dotenv import load_dotenv
load_dotenv()


BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT(
        private_key=BASE_DIR / "config" / "certs" / "jwt-private.pem",
        public_key=BASE_DIR / "config" / "certs" / "jwt-public.pem",
        algorithm="RS256",
        token_type_field=os.getenv('TOKEN_TYPE_FIELD'),
        access_token_expire_minutes=float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')),
        refresh_token_expire_minutes=float(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')),
        access_token_type=os.getenv('ACCESS_TOKEN_TYPE'),
        refresh_token_type=os.getenv('REFRESH_TOKEN_TYPE'),
    )


HTTP_BEARER = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

settings = Settings()