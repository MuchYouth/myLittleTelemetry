import yaml
import sys
import os

# 기본적으로 추가할 서비스 정의
EXTRA_SERVICES = {
    "otel-collector": {
        "image": "otel/opentelemetry-collector-contrib:latest",
        "container_name": "otel-collector",
        "volumes": ["./otel-collector-config.yaml:/etc/otelcol-contrib/config.yaml"],
        "command": ["--config=/etc/otelcol-contrib/config.yaml"],
        "ports": [
            "4317:4317",  # OTLP gRPC
            "4318:4318",  # OTLP HTTP
            "8889:8889",  # Prometheus metrics
        ],
        "networks": ["otel-net"],
    },
    "zipkin": {
        "image": "openzipkin/zipkin",
        "container_name": "zipkin",
        "ports": ["9411:9411"],
        "networks": ["otel-net"],
    },
    "prometheus": {
        "image": "prom/prometheus",
        "container_name": "prometheus",
        "volumes": ["./prometheus.yml:/etc/prometheus/prometheus.yml"],
        "ports": ["9090:9090"],
        "networks": ["otel-net"],
    },
    "elasticsearch": {
        "image": "docker.elastic.co/elasticsearch/elasticsearch:7.17.10",
        "container_name": "elasticsearch",
        "environment": ["discovery.type=single-node","xpack.security.enabled=false",
            "ES_JAVA_OPTS=-Xms512m -Xmx512m"],
        "ports": ["9200:9200"],
        "networks": ["otel-net"],
    },
}

# 커맨드라인 인자 받기
if len(sys.argv) != 2:
    print("사용법: python3 test.py <입력파일명>")
    sys.exit(1)

input_file = sys.argv[1]

# 입력 파일 존재 여부 확인
if not os.path.exists(input_file):
    print(f"파일이 존재하지 않습니다: {input_file}")
    sys.exit(1)

input_file = sys.argv[1]

# 입력 파일 존재 여부 확인
if not os.path.exists(input_file):
    print(f"파일이 존재하지 않습니다: {input_file}")
    sys.exit(1)

# 출력 파일 이름 자동 생성
base, ext = os.path.splitext(input_file)
output_file = f"{base}_after{ext}"

# 읽기
with open(input_file, 'r') as f:
    data = yaml.safe_load(f)

services = data.get('services', {})

# 모든 기존 서비스들에 depends_on과 networks 추가
for service_name, service in services.items():
    if service_name == 'otel-collector':
        continue  # otel-collector 본인은 제외

    if 'depends_on' in service:
        if isinstance(service['depends_on'], list):
            if 'otel-collector' not in service['depends_on']:
                service['depends_on'].append('otel-collector')
    else:
        service['depends_on'] = ['otel-collector']

    if 'networks' not in service:
        service['networks'] = ['otel-net']

# otel-collector, zipkin, prometheus, elasticsearch 추가
for extra_service, extra_def in EXTRA_SERVICES.items():
    if extra_service not in services:
        services[extra_service] = extra_def

# networks 블록 추가
if 'networks' not in data:
    data['networks'] = {'otel-net': {}}

# 저장
with open(output_file, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False)

print(f"변환 완료: {output_file}")
