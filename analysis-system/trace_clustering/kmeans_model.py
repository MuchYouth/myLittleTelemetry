import json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

def load_data(json_path="report.json"):
    with open(json_path) as f:
        data = json.load(f)
    return data

def vectorize(data):
    vectors = []
    for trace in data.get("traces", []):
        duration = trace.get("duration", 0) or 0
        attr_count = len(trace.get("attributes", {}))
        vectors.append([duration, attr_count])
    for log in data.get("logs", []):
        message_length = len(log.get("message", "") or "")
        vectors.append([message_length, 1])
    m = data.get("metrics", {})
    if m:
        request_count = m.get("request_count", 0) or 0
        error_rate = m.get("error_rate", 0) or 0
        vectors.append([request_count, error_rate])
    return vectors

def cluster_data(vectors, k=3):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(vectors)
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(X_scaled)
    return model, X_scaled

def evaluate(model, X):
    print(f"[INFO] Inertia: {model.inertia_}")
    print(f"[INFO] Cluster centers: {model.cluster_centers_}")

if __name__ == "__main__":
    data = load_data()
    X = np.array(vectorize(data))
    X = np.nan_to_num(X)  # <-- NaN 방지
    if X.size == 0:
        print("[ERROR] No data available for clustering.")
    else:
        model, X_scaled = cluster_data(X)
        evaluate(model, X_scaled)

