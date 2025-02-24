import json
import os

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import  FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from starlette import status

from src.config.app_config import create_app, get_custom_openapi
from src.config.swagger_config import config_swagger, Tags, get_routes, delete_router_tag
from src.auth import basic
from src.web import explorer, creature, user

from src.utils.utils import init_otel
from dotenv import load_dotenv

load_dotenv()

init_otel()
RequestsInstrumentor().instrument()

APP_TITLE = os.getenv('APP_TITLE')

app = create_app(
    docs_url=None,
    redoc_url=None,
)

app.openapi = get_custom_openapi(app)

app.include_router(user.router, tags=[Tags.USER_TAG,])
app.include_router(creature.router, tags=[Tags.CREATURE_TAG,])
app.include_router(explorer.router, tags=[Tags.EXPLORER_TAG,])
delete_router_tag(app)


FastAPIInstrumentor.instrument_app(app)
tracer = trace.get_tracer(__name__)


@app.get('/', tags=[Tags.ROOT_TAG,])
def top():
    return 'top here'


@app.get("/echo/{thing}", tags=[Tags.TECH_TAG,])
def echo(thing):
    return ' '.join([thing for _ in range(3)])


@app.get("/test", tags=[Tags.TECH_TAG])
def test_endpoint():
    return {"message": "Hello from test!"}


@app.get("/routes", tags=[Tags.TECH_TAG,])
async def get_routes_endpoint():
    return await get_routes(
        application=app,
    )


@app.get("/test_who", status_code=status.HTTP_200_OK, include_in_schema=False)
@app.get("/test_who/", status_code=status.HTTP_200_OK, tags=[Tags.TECH_TAG,])
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


config_swagger(app, APP_TITLE)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)