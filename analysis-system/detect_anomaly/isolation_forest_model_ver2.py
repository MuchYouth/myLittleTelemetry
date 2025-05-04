import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 1. 데이터 로딩 (result.json 형식: {"vectors": [[x1, y1], [x2, y2], ...]})
with open("../preprocessing/result.json") as f:
    result = json.load(f)

X = np.array(result["vectors"])

# 2. 표준화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. PCA 적용 (특성이 2개 이상일 경우)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print(pca.explained_variance_ratio_)

# 4. Isolation Forest with 낮은 contamination 비율
model = IsolationForest(contamination=0.02, random_state=42)
model.fit(X_pca)
preds = model.predict(X_pca)
scores = model.decision_function(X_pca)

# 5. 이상치 인덱스 및 점수 정렬
anomaly_indices = np.where(preds == -1)[0]
anomaly_scores = scores[anomaly_indices]

# 상위 N개 이상치만 선택
top_n = 20
top_indices = anomaly_indices[np.argsort(anomaly_scores)[:top_n]]
top_anomalies = X_pca[top_indices]
top_scores = anomaly_scores[np.argsort(anomaly_scores)[:top_n]]

# 6. 시각화
plt.figure(figsize=(12, 7))

# 전체 데이터 (희미하게 표시)
plt.scatter(X_pca[:, 0], X_pca[:, 1], c='lightblue', s=30, alpha=0.2, label='Normal')

# 상위 이상치 (강조)
plt.scatter(top_anomalies[:, 0], top_anomalies[:, 1], c='red', s=100,
            edgecolors='black', marker='*', label='Top Anomalies')

# 이상치에 anomaly score 텍스트로 표시
for i, (x, y) in enumerate(top_anomalies):
    plt.text(x, y, f"{top_scores[i]:.2f}", fontsize=8, ha='center', va='center',
             bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'))

# 그래프 설정
plt.title("Improved Anomaly Detection with Isolation Forest + PCA", fontsize=14)
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.ylim(-1, 1)  # y축 범위 제한
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("./visual/improved_anomaly_plot.png")
print("[✓] Saved enhanced anomaly detection plot to improved_anomaly_plot.png")

