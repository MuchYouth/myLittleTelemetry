import json
import sys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def load_and_vectorize(path):
    with open(path) as f:
        data = json.load(f)

    vectors = []
    labels = []

    for trace in data.get("traces", []):
        duration = trace.get("duration", 0)
        attr_count = len(trace.get("attributes", {}))
        vectors.append([duration, attr_count])
        labels.append("trace")

    for log in data.get("logs", []):
        vectors.append([len(log.get("message", "")), 1])
        labels.append("log")

    m = data.get("metrics", {})
    if m:
        vectors.append([m.get("request_count", 0), m.get("error_rate", 0)])
        labels.append("metric")

    return vectors, labels

def visualize(vectors):
    if not vectors:
        print("[ERROR] No vector data available.")
        return

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(vectors)
    model = KMeans(n_clusters=3, random_state=42)
    preds = model.fit_predict(X_scaled)

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=preds, cmap='viridis', alpha=0.8)
    plt.title("KMeans Clustering of Service Flow Data")
    plt.xlabel("Feature 1 (scaled)")
    plt.ylabel("Feature 2 (scaled)")
    plt.grid(True)
    plt.colorbar(scatter, label="Cluster")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualize_clusters.py <path_to_report.json>")
    else:
        vectors, labels = load_and_vectorize(sys.argv[1])
        visualize(vectors)