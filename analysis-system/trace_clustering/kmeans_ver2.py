import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from collections import defaultdict

def load_data(json_path="../preprocessing/report.json"):
    with open(json_path) as f:
        data = json.load(f)
    return data

def vectorize_traces_and_metrics(data):
    vectors = []
    for trace in data.get("traces", []):
        duration = trace.get("duration", 0) or 0
        attr_count = len(trace.get("attributes", {}))
        vectors.append([duration, attr_count])

    m = data.get("metrics", {})
    if m:
        request_count = m.get("request_count", 0) or 0
        error_rate = m.get("error_rate", 0) or 0
        vectors.append([request_count, error_rate])

    return vectors

def vectorize_logs(data):
    log_messages = [log.get("message", "") for log in data.get("logs", []) if log.get("message")]
    if log_messages:
        vectorizer = TfidfVectorizer(max_features=100)
        log_vectors = vectorizer.fit_transform(log_messages).toarray()
        return log_vectors, log_messages
    return [], []

def cluster_data(vectors, k=3):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(vectors)
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(X_scaled)
    return model, X_scaled

def evaluate(model, X):
    print(f"[INFO] Inertia: {model.inertia_}")
    print(f"[INFO] Cluster centers: {model.cluster_centers_}")

def visualize_clusters(X_scaled, model, title, save_path):
    if X_scaled.shape[1] > 2:
        # 고차원일 경우 PCA로 2D로 축소
        pca = PCA(n_components=2)
        X_reduced = pca.fit_transform(X_scaled)
    else:
        X_reduced = X_scaled

    plt.figure(figsize=(8, 6))
    labels = model.labels_
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=labels, cmap='viridis', alpha=0.6)
    plt.scatter(np.mean(X_reduced[:, 0]), np.mean(X_reduced[:, 1]),
                c='red', marker='X', s=200, label='Approximate Center')
    plt.title(title)
    plt.xlabel("Component 1")
    plt.ylabel("Component 2")
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()
    print(f"[INFO] Cluster plot saved as {save_path}")

def show_cluster_messages(model, messages):
    cluster_map = defaultdict(list)
    for idx, label in enumerate(model.labels_):
        cluster_map[label].append(messages[idx])

    print("\n[INFO] Representative messages by cluster:")
    for cluster_id, msgs in cluster_map.items():
        print(f"\nCluster {cluster_id} (total {len(msgs)} messages):")
        for m in msgs[:3]:  # 각 클러스터에서 3개까지만 출력
            print(f"- {m}")

if __name__ == "__main__":
    data = load_data()

    # 1. traces + metrics 벡터화 및 클러스터링
    X_traces = np.array(vectorize_traces_and_metrics(data))
    X_traces = np.nan_to_num(X_traces)
    if X_traces.size == 0:
        print("[ERROR] No trace/metric data available for clustering.")
    else:
        model_traces, X_traces_scaled = cluster_data(X_traces)
        evaluate(model_traces, X_traces_scaled)
        visualize_clusters(X_traces_scaled, model_traces, "Traces/Metrics Clustering", "traces_cluster_plot.png")

    # 2. logs 의미기반 임베딩(TF-IDF) 및 클러스터링
    X_logs, log_messages = vectorize_logs(data)
    if len(X_logs) == 0:
        print("[ERROR] No log messages available for clustering.")
    else:
        model_logs, X_logs_scaled = cluster_data(X_logs)
        evaluate(model_logs, X_logs_scaled)
        visualize_clusters(X_logs_scaled, model_logs, "Logs Clustering (TF-IDF + PCA)", "./visual/logs_cluster_plot.png")
        show_cluster_messages(model_logs, log_messages)

