import json

import httpx
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasicCredentials
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import  FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from starlette import status

from src.auth import basic
from src.web import explorer, creature

from src.utils import init_otel


init_otel()
RequestsInstrumentor().instrument()

app = FastAPI()
app.include_router(explorer.router)
app.include_router(creature.router)

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
            'http://webapp_auth/who',
            auth=(creds.username, creds.password)
        )
        return {
            'status_code': response.status_code,
            'headers': response.headers,
            'content': json.loads(response.text)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)