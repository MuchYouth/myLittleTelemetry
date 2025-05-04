#!/bin/bash

# 반복 횟수 (데이터 수집량 조절)
ITERATIONS=500

echo "[INFO] Generating traffic to microservices..."

for i in $(seq 1 $ITERATIONS); do
  curl -s http://localhost:8001/user-service/hello > /dev/null
  curl -s http://localhost:8001/user-service/profile > /dev/null
  curl -s http://localhost:8005/notification-service/email > /dev/null

  curl -s http://localhost:8001/user-service/signup > /dev/null
  curl -s http://localhost:8002/order-service/create > /dev/null
  curl -s http://localhost:8003/inventory-service/stock > /dev/null

  curl -s http://localhost:8004/payment-service/pay > /dev/null
  curl -s http://localhost:8003/inventory-service/update > /dev/null
done

echo "[INFO] Done generating traffic."

