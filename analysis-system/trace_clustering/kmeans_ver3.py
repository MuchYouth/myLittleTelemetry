import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 전처리된 벡터 데이터 로드
with open("../preprocessing/result.json") as f:
    result = json.load(f)

X = np.array(result["vectors"])
X_scaled = StandardScaler().fit_transform(X)

# 클러스터링
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X_scaled)
centroids = kmeans.cluster_centers_

# 시각화
plt.figure(figsize=(10, 6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap='viridis', s=60, alpha=0.7, edgecolors='k')
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=250, marker='*', label='Centroids')

# 군집 레이블 텍스트 표시
for i, (x, y) in enumerate(centroids):
    plt.text(x, y, f'Cluster {i}', fontsize=12, fontweight='bold', ha='center', va='center',
             color='white', bbox=dict(facecolor='black', alpha=0.6, boxstyle='round,pad=0.4'))

plt.title("Service Flow Clustering with KMeans", fontsize=14)
plt.xlabel("Feature 1 (scaled)")
plt.ylabel("Feature 2 (scaled)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("./visual/cluster_result_star.png")
print("[✓] Clustering result saved as cluster_result.png")

