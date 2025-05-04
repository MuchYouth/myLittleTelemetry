#!/bin/bash

# SpanId 생성 함수
generate_span_id() {
  echo $(uuidgen | tr '[:upper:]' '[:lower:]' | sed 's/-//g' | cut -c1-16)
}

# 엔드포인트 목록
endpoints=(
  "hello"
  "signup"
  "pay"
  "refund"
  "email"
  "sms"
)

# 500개 Trace를 생성
for i in {1..500}; do
  # 매 요청마다 새로운 Trace 생성
  trace_id=$(uuidgen | tr '[:upper:]' '[:lower:]' | sed 's/-//g')
  root_span_id=$(generate_span_id)
  parent_span_id=$root_span_id

  # 엔드포인트 중 하나를 랜덤 선택
  endpoint=${endpoints[$RANDOM % ${#endpoints[@]}]}

  # 요청 보내기
  child_span_id=$(generate_span_id)
  response_code=$(curl -s -o /dev/null -w "%{http_code}" \
       -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8001/$endpoint)

  echo "[Trace $i] Sent request to /$endpoint - Response Code: $response_code"
done

