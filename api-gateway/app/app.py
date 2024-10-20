from fastapi import FastAPI, HTTPException, Request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.propagate import inject, extract

import httpx

app = FastAPI()

# Base URLs of the microservices
AUTH_SERVICE_URL = "http://localhost:8001"
VEHICLE_SERVICE_URL = "http://localhost:8002"
BOOKING_SERVICE_URL = "http://localhost:8003"
POST_SALE_SERVICE_URL = "http://localhost:8004"
ROADSIDE_ASSISTANCE_URL = "http://localhost:8005"
CUSTOMER_FEEDBACK_URL = "http://localhost:8006"
CUSTOMER_SERVICE_URL = "http://localhost:8007"

# ===========================
# OpenTelemetry and Jaeger Setup
# ===========================
def configure_opentelemetry():
    resource = Resource(attributes={
        "service.name": "fastapi-service",
        "service.version": "1.0.0"
    })

    trace.set_tracer_provider(TracerProvider(resource=resource))

    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )

    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    console_exporter = ConsoleSpanExporter()
    trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(console_exporter))

configure_opentelemetry()

FastAPIInstrumentor.instrument_app(app)

# Function to handle requests and forward them to the appropriate service
async def forward_request(service_url: str, request: Request):
    async with httpx.AsyncClient() as client:
        headers = dict(request.headers)

        # Inject the trace context into the headers (adds traceparent for propagation)
        inject(headers)

        # Forward the request to the downstream service
        response = await client.request(
            method=request.method,
            url=service_url + request.url.path,
            headers=headers,
            json=await request.json() if request.method in ["POST", "PUT"] else None,
            params=request.query_params if request.method == "GET" else None,
        )
        return response.json()

# Auth Service APIs
@app.post("/auth/register")
async def register_user(request: Request):
    return await forward_request(AUTH_SERVICE_URL, request)

@app.post("/auth/token")
async def login_for_access_token(request: Request):
    return await forward_request(AUTH_SERVICE_URL, request)

# Customer Service APIs
@app.get("/customers")
async def get_all_customers(request: Request):
    return await forward_request(CUSTOMER_SERVICE_URL, request)

@app.post("/customers")
async def create_customer(request: Request):
    return await forward_request(CUSTOMER_SERVICE_URL, request)

# Vehicle Service APIs
@app.get("/vehicles")
async def get_vehicles(request: Request):
    return await forward_request(VEHICLE_SERVICE_URL, request)

@app.get("/vehicles/{vehicle_id}")
async def get_vehicle_by_id(vehicle_id: str, request: Request):
    return await forward_request(f"{VEHICLE_SERVICE_URL}/vehicles/{vehicle_id}", request)

# Booking Service APIs
@app.get("/testdrives")
async def get_test_drives(request: Request):
    return await forward_request(BOOKING_SERVICE_URL, request)

# Post-Sale Service APIs
@app.post("/service/schedule")
async def schedule_service(request: Request):
    return await forward_request(POST_SALE_SERVICE_URL, request)

@app.get("/service/history")
async def get_service_history(request: Request):
    return await forward_request(POST_SALE_SERVICE_URL, request)

# Roadside Assistance Service APIs
@app.post("/rsa/request")
async def request_roadside_assistance(request: Request):
    return await forward_request(ROADSIDE_ASSISTANCE_URL, request)

@app.get("/rsa/status/{requestId}")
async def get_roadside_status(requestId: str, request: Request):
    return await forward_request(f"{ROADSIDE_ASSISTANCE_URL}/rsa/status/{requestId}", request)

# Customer Feedback Service APIs
@app.post("/feedback/submit")
async def submit_feedback(request: Request):
    return await forward_request(CUSTOMER_FEEDBACK_URL, request)

@app.get("/feedback/{id}")
async def get_feedback_by_id(id: str, request: Request):
    return await forward_request(f"{CUSTOMER_FEEDBACK_URL}/feedback/{id}", request)
