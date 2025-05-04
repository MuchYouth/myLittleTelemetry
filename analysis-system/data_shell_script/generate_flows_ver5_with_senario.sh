#!/bin/bash

TRACE_COUNT=1000  # 총 트레이스 수
ZIPKIN_API="http://localhost:9411/api/v2/traces"
ELASTICSEARCH_API="http://localhost:9200/logs*/_search"
PROMETHEUS_API="http://localhost:9090/api/v1/query"
OUTPUT="telemetry_data.json"

mkdir -p collected
echo "[INFO] Sending 100 diverse service flow requests..."

REPEAT=$((TRACE_COUNT / 100))  # 각 흐름을 몇 번 반복할지

# 서비스-엔드포인트 매핑
declare -A SERVICE_ENDPOINTS
SERVICE_ENDPOINTS["user-service"]="hello profile signup"
SERVICE_ENDPOINTS["payment-service"]="pay refund status"
SERVICE_ENDPOINTS["order-service"]="create update"
SERVICE_ENDPOINTS["notification-service"]="email sms push"
SERVICE_ENDPOINTS["inventory-service"]="stock check update"

# 포트 매핑
declare -A SERVICE_PORTS
SERVICE_PORTS["user-service"]=8001
SERVICE_PORTS["order-service"]=8002
SERVICE_PORTS["inventory-service"]=8003
SERVICE_PORTS["payment-service"]=8004
SERVICE_PORTS["notification-service"]=8005

# 100가지 호출 흐름 구성
for flow in $(seq 1 100); do
  for r in $(seq 1 $REPEAT); do
    tid=$(uuidgen | tr '[:upper:]' '[:lower:]' | tr -d '-')

    # 각 흐름은 3~6개의 서비스 호출 포함
    STEP_COUNT=$((3 + RANDOM % 4))
    STEP=1

    # 호출할 서비스 목록 무작위 샘플링
    services=("user-service" "order-service" "inventory-service" "payment-service" "notification-service")
    for s in $(shuf -e "${services[@]}" | head -n $STEP_COUNT); do
      # 해당 서비스의 엔드포인트 중 하나 무작위 선택
      ep_list=(${SERVICE_ENDPOINTS[$s]})
      ep=${ep_list[$RANDOM % ${#ep_list[@]}]}
      port=${SERVICE_PORTS[$s]}

      # 요청 실행
      curl -s -H "traceparent: 00-$tid-$STEP-01" "http://localhost:$port/$s/$ep" > /dev/null
      STEP=$((STEP + 1))
    done
  done
done

echo "[INFO] Waiting for traces to flush to Zipkin/Elasticsearch..."
sleep 10

# Trace 수집
echo "[INFO] Fetching traces from Zipkin..."
curl -s "$ZIPKIN_API?limit=$TRACE_COUNT" > collected/trace_data.json

# Log 수집
echo "[INFO] Fetching logs from Elasticsearch..."
curl -s -X GET "$ELASTICSEARCH_API" -H 'Content-Type: application/json' \
  -d '{
        "size": 1000,
        "_source": ["@timestamp", "message", "log.level", "service.name"]
      }' > collected/log_data.json

# Metric 수집
echo "[INFO] Fetching metrics from Prometheus..."
curl -s -G "$PROMETHEUS_API" \
     --data-urlencode 'query=sum(rate(http_server_requests_total[1m])) by (service)' \
     > collected/metrics_data.json

# 통합 저장
echo "[INFO] Aggregating to $OUTPUT..."
jq -n \
  --slurpfile traces collected/trace_data.json \
  --slurpfile logs collected/log_data.json \
  --slurpfile metrics collected/metrics_data.json \
  '{traces: $traces[0], logs: $logs[0].hits.hits, metrics: $metrics[0].data.result}' > "$OUTPUT"

echo "[✓] Saved telemetry data to $OUTPUT"

