import json
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def load_and_vectorize(path):
    with open(path) as f:
        data = json.load(f)

    vectors = []
    labels = []

    for trace in data.get("traces", []):
        duration = trace.get("duration", 0) or 0
        attr_count = len(trace.get("attributes", {}))
        vectors.append([duration, attr_count])
        labels.append("trace")

    for log in data.get("logs", []):
        message_length = len(log.get("message", "") or "")
        vectors.append([message_length, 1])
        labels.append("log")

    m = data.get("metrics", {})
    if m:
        request_count = m.get("request_count", 0) or 0
        error_rate = m.get("error_rate", 0) or 0
        vectors.append([request_count, error_rate])
        labels.append("metric")

    return np.array(vectors), labels

def visualize(vectors, output_path="visualization_result.png"):
    if vectors.size == 0:
        print("[ERROR] No vector data available.")
        return

    vectors = np.nan_to_num(vectors)  # NaN 방지

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(vectors)

    plt.figure(figsize=(8, 6))
    plt.scatter(X_scaled[:, 0], X_scaled[:, 1], alpha=0.8)
    plt.title("Service Flow Data Visualization")
    plt.xlabel("Feature 1 (scaled)")
    plt.ylabel("Feature 2 (scaled)")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path)
    print(f"[INFO] Visualization saved as '{output_path}'")
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualize_clusters.py <path_to_report.json>")
    else:
        input_path = sys.argv[1]
        output_filename = "visualization_result.png"  # 저장될 파일명

        vectors, labels = load_and_vectorize(input_path)
        visualize(vectors, output_path=output_filename)

