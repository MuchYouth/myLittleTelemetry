from fastapi import FastAPI, Request
from fastapi import HTTPException
import random
import logging
import sys
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
service_name = "order-service"  # 서비스마다 이름 변경해야 함

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

# --- 엔드포인트 수정본 ---

@app.get("/create")
async def create_order(request: Request):
    span = get_current_span()
    trace_id = format(span.get_span_context().trace_id, '032x') if span else "unknown"
    if random.random() < 0.1:  # 10% 확률로 주문 생성 실패
        logger.error("Order creation failed", extra={"trace_id": trace_id, "user_id": "user-123"})
        raise HTTPException(status_code=500, detail="Order creation failed")
    log_request("/create", request)
    return {"order_id": "order-001"}

@app.get("/update")
async def update_order(request: Request):
    span = get_current_span()
    trace_id = format(span.get_span_context().trace_id, '032x') if span else "unknown"
    if random.random() < 0.2:  # 20% 확률로 주문 업데이트 실패
        logger.error("Order update failed", extra={"trace_id": trace_id, "user_id": "user-123"})
        raise HTTPException(status_code=500, detail="Order update failed")
    log_request("/update", request)
    return {"order_id": "order-001", "status": "updated"}


