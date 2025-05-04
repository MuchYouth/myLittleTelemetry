import requests

PROMETHEUS_URL = "http://localhost:9090"  # Prometheus 서버 주소

def extract_metrics():
    # 쿼리 정의
    queries = {
        "request_count": 'sum(http_requests_total)',
        "avg_response_time": 'avg(http_request_duration_seconds)',
        "error_rate": 'sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))'
    }

    results = {}

    for key, query in queries.items():
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": query})
        data = response.json()
        try:
            value = float(data["data"]["result"][0]["value"][1])
            results[key] = value
        except (IndexError, KeyError):
            results[key] = None  # 혹시 값이 없으면 None 처리

    return results

