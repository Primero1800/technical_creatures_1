from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import  FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)