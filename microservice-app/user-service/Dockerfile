FROM python:3.10-slim

# 시스템 패키지 설치 (필요 시)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리
WORKDIR /app

# 필요 파일 복사
COPY . .

# pip 업그레이드 + 패키지 설치
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 포트 노출
EXPOSE 8000

# 실행 명령
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



