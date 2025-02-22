import json
import os

import httpx
from fastapi import Depends, HTTPException, FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasicCredentials
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import  FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from starlette import status

from src.app_config import create_app, get_custom_openapi
from src.auth import basic
from src.web import explorer, creature, user

from src.utils import init_otel


init_otel()
RequestsInstrumentor().instrument()

APP_TITLE = os.getenv('APP_TITLE')

app = create_app(
    docs_url=None,
    redoc_url=None,
)

app.openapi = get_custom_openapi(app)


app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

FastAPIInstrumentor.instrument_app(app)
tracer = trace.get_tracer(__name__)


@app.get('/')
def top():
    return 'top here'


@app.get("/echo/{thing}")
def echo(thing):
    return ' '.join([thing for _ in range(3)])


@app.get("/test")
def test_endpoint():
    return {"message": "Hello from test!"}


@app.get("/test_who", status_code=status.HTTP_200_OK, include_in_schema=False)
@app.get("/test_who/", status_code=status.HTTP_200_OK)
def test_endpoint(creds: HTTPBasicCredentials = Depends(basic)):
    with httpx.Client() as client:
        response = client.get(
            'http://webapp_auth:8000/who',
            auth=(creds.username, creds.password)
        )
        if response.status_code == 200:
            return {
                'status_code': response.status_code,
                'headers': response.headers,
                'content': json.loads(response.text)
            }
        else:
            raise HTTPException(status_code=response.status_code, detail=json.loads(response.text)['detail'])


@app.get('/docs', status_code=status.HTTP_200_OK, include_in_schema=False)
@app.get('/docs', status_code=status.HTTP_200_OK)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=APP_TITLE + ' Swagger UI',
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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)