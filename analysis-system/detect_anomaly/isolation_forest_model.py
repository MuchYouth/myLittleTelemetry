import json
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 데이터 로딩
with open("../preprocessing/result.json") as f:
    result = json.load(f)

X = np.array(result["vectors"])

# 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 이상치 탐지 모델
model = IsolationForest(contamination=0.1, random_state=42)
preds = model.fit_predict(X_scaled)

# 분리
normal = X_scaled[preds == 1]
anomalies = X_scaled[preds == -1]

# 시각화
plt.figure(figsize=(12, 7))

# 정상 데이터 (파란 점, 투명)
plt.scatter(normal[:, 0], normal[:, 1], 
            c='skyblue', edgecolors='k', s=40, alpha=0.3, label='Normal')

# 이상치 데이터 (붉은 별, 굵은 테두리)
plt.scatter(anomalies[:, 0], anomalies[:, 1], 
            c='red', s=100, marker='*', edgecolors='black', linewidths=1.2, label='Anomaly')

# 각 이상치에 번호 주석 (선택사항)
for i, (x, y) in enumerate(anomalies):
    plt.text(x, y, f"{i}", fontsize=8, color='black', ha='center', va='center',
             bbox=dict(facecolor='white', edgecolor='gray', alpha=0.6, boxstyle='round,pad=0.2'))

# 제목, 라벨, 그리드
plt.title("🔍 Isolation Forest - Anomaly Detection", fontsize=15, weight='bold')
plt.xlabel("Feature 1 (scaled)")
plt.ylabel("Feature 2 (scaled)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("./visual/anomaly_detect_enhanced.png")
print("[✓] Saved enhanced anomaly detection plot to anomaly_detect_enhanced.png")

