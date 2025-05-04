from fastapi import FastAPI, Request, HTTPException
import logging
import sys
import random
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.zipkin.proto.http import ZipkinExporter
from opentelemetry import trace
from opentelemetry.trace import get_current_span

# --- 서비스 이름 설정 ---
service_name = "user-service"

# --- 트레이서 프로바이더 설정 ---
resource = Resource(attributes={"service.name": service_name})
provider = TracerProvider(resource=resource)

otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

zipkin_exporter = ZipkinExporter(endpoint="http://zipkin:9411/api/v2/spans")
provider.add_span_processor(BatchSpanProcessor(zipkin_exporter))

trace.set_tracer_provider(provider)

# --- FastAPI 앱 생성 ---
app = FastAPI()

# --- OpenTelemetry 자동 계측 ---
FastAPIInstrumentor.instrument_app(app)

# --- Prometheus 메트릭 노출 (/metrics) ---
Instrumentator().instrument(app).expose(app)

# --- 로깅 설정 ---
logger = logging.getLogger(service_name)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", '
    '"service": "' + service_name + '", "trace_id": "%(trace_id)s", "user_id": "%(user_id)s"}'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# --- trace_id를 함께 기록하는 로깅 함수 ---
def log_request(endpoint: str, request: Request):
    span = get_current_span()
    trace_id = format(span.get_span_context().trace_id, '032x') if span else "unknown"
    logger.info(f"Accessed {endpoint}", extra={"trace_id": trace_id, "user_id": "user-123"})

# --- 엔드포인트들 (랜덤 실패 추가) ---

@app.get("/hello")
async def hello(request: Request):
    span = get_current_span()
    trace_id = format(span.get_span_context().trace_id, '032x') if span else "unknown"
    if random.random() < 0.1:  # 10% 확률로 /hello 실패
        logger.error("Failed to access /hello", extra={"trace_id": trace_id, "user_id": "user-123"})
        raise HTTPException(status_code=500, detail="Hello service error")
    log_request("/hello", request)
    return {"message": f"Hello from {service_name}"}

@app.get("/profile")
async def profile(request: Request):
    span = get_current_span()
    trace_id = format(span.get_span_context().trace_id, '032x') if span else "unknown"
    if random.random() < 0.1:  # 10% 확률로 /profile 실패
        logger.error("Failed to access /profile", extra={"trace_id": trace_id, "user_id": "user-123"})
        raise HTTPException(status_code=404, detail="Profile not found")
    log_request("/profile", request)
    return {"user": {"id": "user-123", "name": "Alice"}}

@app.get("/signup")
async def signup(request: Request):
    span = get_current_span()
    trace_id = format(span.get_span_context().trace_id, '032x') if span else "unknown"
    if random.random() < 0.15:  # 15% 확률로 /signup 실패
        logger.error("Signup failed", extra={"trace_id": trace_id, "user_id": "user-123"})
        raise HTTPException(status_code=400, detail="Signup failed")
    log_request("/signup", request)
    return {"status": "signup successful"}

