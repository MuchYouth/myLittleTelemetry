#!/bin/bash

TRACE_COUNT=600  # 원하는 트레이스 수량 (500~1000)
ZIPKIN_API="http://localhost:9411/api/v2/traces"
ELASTICSEARCH_API="http://localhost:9200/logs*/_search"
PROMETHEUS_API="http://localhost:9090/api/v1/query"
OUTPUT="telemetry_data.json"

mkdir -p collected
echo "[INFO] Sending requests to generate traces..."

for i in $(seq 1 $TRACE_COUNT); do
  TRACE_ID=$(uuidgen | tr '[:upper:]' '[:lower:]' | tr -d '-')

  # Custom traceparent header (OpenTelemetry-compatible)
  curl -s -H "traceparent: 00-$TRACE_ID-0000000000000001-01" \
       http://localhost:8001/user-service/hello > /dev/null
  curl -s -H "traceparent: 00-$TRACE_ID-0000000000000002-01" \
       http://localhost:8002/order-service/create > /dev/null
  curl -s -H "traceparent: 00-$TRACE_ID-0000000000000003-01" \
       http://localhost:8003/inventory-service/stock > /dev/null
done

echo "[INFO] Waiting for traces to flush to Zipkin/Elasticsearch..."
sleep 10

echo "[INFO] Fetching trace data from Zipkin..."
curl -s "$ZIPKIN_API?limit=600" > collected/trace_data.json

echo "[INFO] Fetching logs from Elasticsearch..."
curl -s -X GET "$ELASTICSEARCH_API" -H 'Content-Type: application/json' \
  -d '{
        "size": 600,
        "_source": ["@timestamp", "message", "log.level", "service.name"]
      }' > collected/log_data.json

echo "[INFO] Fetching metrics from Prometheus..."
curl -s -G "$PROMETHEUS_API" \
     --data-urlencode 'query=sum(rate(http_server_requests_total[1m])) by (service)' \
     > collected/metrics_data.json

# 통합 JSON 파일로 저장
echo "[INFO] Aggregating to $OUTPUT..."
jq -n \
  --slurpfile traces collected/trace_data.json \
  --slurpfile logs collected/log_data.json \
  --slurpfile metrics collected/metrics_data.json \
  '{traces: $traces[0], logs: $logs[0].hits.hits, metrics: $metrics[0].data.result}' > "$OUTPUT"

echo "[DONE] Saved all data to $OUTPUT"

