import os
from dotenv import load_dotenv

from typing import Callable, Dict, Any
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.config.swagger_config import Tags

load_dotenv()


def create_app(docs_url, redoc_url) -> FastAPI:
    app = FastAPI(
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_tags=tags_metadata,
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

        subject.openapi_schema = openapi_schema
        return subject.openapi_schema

    return custom_openapi


# ???????????????????????????????????????????????????????????????????????
tags_metadata = [
        {
            "name": Tags.USER_TAG,
            "description": Tags.USER_TAG_DESCRIPTION,
        },
        {
            "name": Tags.TECH_TAG,
            "description": Tags.TECH_TAG_DESCRIPTION,
        },
        {
            "name": Tags.AUTH_TAG,
            "description": Tags.AUTH_TAG_DESCRIPTION,
        },
        {
            "name": Tags.EXPLORER_TAG,
            "description": Tags.EXPLORER_TAG_DESCRIPTION,
        },
        {
            "name": Tags.CREATURE_TAG,
            "description": Tags.CREATURE_TAG_DESCRIPTION,
        },
        {
            "name": Tags.ROOT_TAG,
            "description": Tags.ROOT_TAG_DESCRIPTION,
        },
        {
            "name": Tags.SWAGGER_TAG,
            "description": Tags.SWAGGER_TAG_DESCRIPTION,
        },
    ]
