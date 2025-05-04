import json

def load_data(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def flatten_traces(traces):
    """traces 배열 내에 있는 중첩된 리스트들을 펼쳐서 dict만 추출"""
    flat = []
    for i, item in enumerate(traces):
        if isinstance(item, dict):
            flat.append(item)
        elif isinstance(item, list):
            flat.extend([span for span in item if isinstance(span, dict)])
        else:
            print(f"[WARN] Skipping trace[{i}] - unsupported type: {type(item)}")
    return flat

def preprocess(traces, logs, metrics):
    vectors = []
    edges = []
    labels = []

    flat_traces = flatten_traces(traces)

    for trace in flat_traces:
        duration = trace.get("duration", 0)
        service = trace.get("localEndpoint", {}).get("serviceName", "unknown")

        # 벡터: [duration, 1]
        vectors.append([duration, 1])
        labels.append("trace")

        # 엣지: 단순히 (service, service) → 이후 traceId 기반 흐름 분석 확장 가능
        edges.append((service, service))

    for i, log in enumerate(logs):
        if not isinstance(log, dict):
            print(f"[WARN] Skipping log[{i}] - not a dict")
            continue

        message = log.get("message", "")
        vectors.append([len(message), 1])
        labels.append("log")

    if isinstance(metrics, dict):
        vectors.append([
            metrics.get("request_count", 0),
            metrics.get("error_rate", 0)
        ])
        labels.append("metric")

    return vectors, edges, labels

if __name__ == "__main__":
    data = load_data("../data_shell_script/telemetry_data.json")

    if isinstance(data, list):
        traces = data
        logs = []
        metrics = {}
        print("[INFO] telemetry_data.json: Detected raw list of traces.")
    else:
        traces = data.get("traces", [])
        logs = data.get("logs", [])
        metrics = data.get("metrics", {})
        print("[INFO] telemetry_data.json: Detected wrapped format with traces/logs/metrics.")

    vectors, edges, labels = preprocess(traces, logs, metrics)

    result = {
        "vectors": vectors,
        "edges": edges,
        "labels": labels
    }

    with open("result.json", "w") as f:
        json.dump(result, f)

    print(f"[✓] Saved preprocessed result to result.json")

