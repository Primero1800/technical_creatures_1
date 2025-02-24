import os
from dotenv import load_dotenv

from typing import Callable, Dict, Any
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

load_dotenv()


def create_app(docs_url, redoc_url) -> FastAPI:
    app = FastAPI(
        docs_url=docs_url,
        redoc_url=redoc_url,
    )
    return app




def get_custom_openapi(subject: FastAPI) -> Callable[[], Dict[str, Any]]:
    def custom_openapi() -> Dict[str, Any]:
        if subject.openapi_schema:
            return subject.openapi_schema
        openapi_schema = get_openapi(
            title=os.getenv('APP_TITLE'),
            version=os.getenv('APP_VERSION'),
            description=os.getenv('APP_DESCRIPTION'),
            routes=subject.routes,
        )
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            },
            # "BasicAuth": {
            #     "type": "http",
            #     "scheme": "basic"
            # },
        }

        openapi_schema["security"] = [
            {"BearerAuth": []},
            # {"BasicAuth": []}
        ]

        subject.openapi_schema = openapi_schema
        return subject.openapi_schema

    return custom_openapi
