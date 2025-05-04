# 10초 대기 후 시작
# 최대 3번까지 재시도 (extract_* 함수가 빈 결과를 반환하거나 에러가 나면 재시도)
import json
import time
from zipkin_extractor import extract_zipkin
from elasticsearch_extractor import extract_logs
from prometheus_extractor import extract_metrics

def wait_for_data(seconds=10):
    print(f"[INFO] Waiting {seconds} seconds to allow data to accumulate...")
    time.sleep(seconds)

def retry_extract(func, name, retries=3, delay=3):
    for attempt in range(retries):
        try:
            data = func()
            if data:
                print(f"[INFO] Successfully fetched {name} data on attempt {attempt + 1}")
                return data
            else:
                print(f"[WARN] No {name} data on attempt {attempt + 1}, retrying...")
        except Exception as e:
            print(f"[ERROR] Failed to fetch {name} on attempt {attempt + 1}: {e}")
        time.sleep(delay)
    print(f"[ERROR] All retries failed for {name}. Returning empty.")
    return [] if name != "metrics" else {}

def export_to_json():
    wait_for_data()

    traces = retry_extract(extract_zipkin, "traces")
    logs = retry_extract(extract_logs, "logs")
    metrics = retry_extract(extract_metrics, "metrics")

    data = {
        "traces": traces,
        "logs": logs,
        "metrics": metrics
    }

    with open("report.json", "w") as f:
        json.dump(data, f, indent=2)
    print("[INFO] Export complete: report.json created.")

if __name__ == "__main__":
    export_to_json()
