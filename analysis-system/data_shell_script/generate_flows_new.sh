#!/bin/bash

# TraceId를 하나 생성 (32자리 16진수)
trace_id=$(uuidgen | tr '[:upper:]' '[:lower:]' | sed 's/-//g')

# SpanId 생성 함수 (16자리만 잘라쓰기)
generate_span_id() {
  echo $(uuidgen | tr '[:upper:]' '[:lower:]' | sed 's/-//g' | cut -c1-16)
}

# 사용자 흐름 (Root Span 생성)
root_span_id=$(generate_span_id)
echo "Using TraceId: $trace_id"
echo "Root SpanId: $root_span_id"

# 사용자 조회 + 알림
parent_span_id=$root_span_id
for i in {1..200}; do
  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8001/hello > /dev/null
  parent_span_id=$child_span_id

  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8001/profile > /dev/null
  parent_span_id=$child_span_id

  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8005/email > /dev/null
  parent_span_id=$child_span_id
done

# 주문 처리 플로우
parent_span_id=$root_span_id
for i in {1..200}; do
  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8001/signup > /dev/null
  parent_span_id=$child_span_id

  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8002/create > /dev/null
  parent_span_id=$child_span_id

  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8003/stock > /dev/null
  parent_span_id=$child_span_id
done

# 결제 성공 플로우
parent_span_id=$root_span_id
for i in {1..200}; do
  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8001/hello > /dev/null
  parent_span_id=$child_span_id

  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8004/pay > /dev/null
  parent_span_id=$child_span_id

  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8002/create > /dev/null
  parent_span_id=$child_span_id

  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8003/update > /dev/null
  parent_span_id=$child_span_id
done

# 실패 플로우
parent_span_id=$root_span_id
for i in {1..200}; do
  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8004/refund > /dev/null
  parent_span_id=$child_span_id
done

# 알림 전용 요청
parent_span_id=$root_span_id
for i in {1..200}; do
  child_span_id=$(generate_span_id)
  curl -s -H "X-B3-TraceId:$trace_id" \
       -H "X-B3-SpanId:$child_span_id" \
       -H "X-B3-ParentSpanId:$parent_span_id" \
       http://localhost:8005/sms > /dev/null
  parent_span_id=$child_span_id
done

