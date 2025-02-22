from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer


def create_app(docs_url, redoc_url) -> FastAPI:
    app = FastAPI(
        docs_url=docs_url,
        redoc_url=redoc_url,
    )
    return app


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
