import os

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html, get_redoc_html
from starlette import status

from dotenv import load_dotenv

load_dotenv()

class Tags:
    AUTH_TAG = os.getenv('AUTH_TAG')
    TECH_TAG = os.getenv('TECH_TAG')
    USER_TAG = os.getenv('USER_TAG')
    CREATURE_TAG = os.getenv('CREATURE_TAG')
    EXPLORER_TAG = os.getenv('EXPLORER_TAG')
    ROOT_TAG = os.getenv('ROOT_TAG')
    SWAGGER_TAG = os.getenv('SWAGGER_TAG')


async def get_routes(application: FastAPI, path=True, tags=True, methods=True, ):
    routes_info = []
    for route in application.routes:
        route_dict = {}
        if path:
            route_dict['path'] = route.path
        if tags:
            route_dict['tags'] = route.tags if hasattr(route, "tags") else []
        if methods:
            route_dict['methods'] = route.methods
        routes_info.append(route_dict)
    return routes_info


def delete_router_tag(application: FastAPI):
    for route in application.routes:
        if hasattr(route, "tags"):
            if isinstance(route.tags, list) and len(route.tags) > 1:
                del route.tags[0]


def config_swagger(app: FastAPI, app_title='Unknown application'):
    @app.get('/docs', status_code=status.HTTP_200_OK, include_in_schema=False)
    @app.get('/docs', status_code=status.HTTP_200_OK, tags=[Tags.SWAGGER_TAG])
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app_title + ' Swagger UI',
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        )


    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()


    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
        )
