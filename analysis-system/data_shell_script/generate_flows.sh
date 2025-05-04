#!/bin/bash

# TraceId를 하나 생성 (16진수 32자리)
trace_id=$(uuidgen | tr '[:upper:]' '[:lower:]' | sed 's/-//g')

# SpanId 생성 함수 (16자리만 잘라쓰기)
generate_span_id() {
  echo $(uuidgen | tr '[:upper:]' '[:lower:]' | sed 's/-//g' | cut -c1-16)
}

echo "Using TraceId: $trace_id"

# 사용자 조회 + 알림
for i in {1..200}; do
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8001/hello > /dev/null
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8001/profile > /dev/null
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8005/email > /dev/null
done

# 주문 처리 플로우
for i in {1..200}; do
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8001/signup > /dev/null
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8002/create > /dev/null
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8003/stock > /dev/null
done

# 결제 성공 플로우
for i in {1..200}; do
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8001/hello > /dev/null
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8004/pay > /dev/null
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8002/create > /dev/null
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8003/update > /dev/null
done

# 실패 플로우
for i in {1..200}; do
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8004/refund > /dev/null
done

# 알림 전용 요청
for i in {1..200}; do
  curl -s -H "X-B3-TraceId:$trace_id" -H "X-B3-SpanId:$(generate_span_id)" http://localhost:8005/sms > /dev/null
done

