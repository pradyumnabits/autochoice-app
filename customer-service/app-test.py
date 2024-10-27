import os
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# FastAPI app initialization
app = FastAPI()

# ===========================
# OpenTelemetry and Jaeger Setup
# ===========================
def configure_opentelemetry():
    # Define a resource describing the service
    resource = Resource(attributes={
        "service.name": "fastapi-service",
        "service.version": "1.0.0"
    })

    # Set up the tracer provider with resource details
    trace.set_tracer_provider(TracerProvider(resource=resource))

    # Create a JaegerExporter instance to send traces to Jaeger
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",  # Jaeger agent hostname
        agent_port=6831,              # Jaeger agent port
    )

    # Add BatchSpanProcessor to batch and export spans
    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    # Optional: Console exporter for debugging
    console_exporter = ConsoleSpanExporter()
    trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(console_exporter))

# Call OpenTelemetry configuration before app initialization
configure_opentelemetry()

# Instrument FastAPI app to capture traces
FastAPIInstrumentor.instrument_app(app)

# ===========================
# Sample Endpoint
# ===========================
@app.get("/customers")
async def say_hello():
    return {"message": "Hello, world!"}

# ===========================
# Other code (database, endpoints, etc.)
# ===========================
# Add your database and other logic here, as shown in your previous FastAPI setup.
