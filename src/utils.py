import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

from dotenv import load_dotenv
load_dotenv()

def init_otel():
    JAEGER_COLLECTOR_ENDPOINT = os.getenv('JAEGER_COLLECTOR_ENDPOINT', '0.0.0.0')
    JAEGER_COLLECTOR_PORT = os.getenv('JAEGER_COLLECTOR_PORT', 4318)
    resource = Resource(attributes={
        'service.name': '1_creatures_service',
        'os-version': '1.0.2',
        'cluster': 'A',
        'datacentre': 'BNE',
    })
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=f"http://{JAEGER_COLLECTOR_ENDPOINT}:{JAEGER_COLLECTOR_PORT}/v1/traces"))
    provider.add_span_processor(span_processor=processor)

    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer('1_creatures.tracer')


def get_db_connection():
    return '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_NAME')
    )