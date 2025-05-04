## 텔레메트리 메트릭 기반 마이크로서비스 배치전략 분석시스템

### 프로젝트 개요

외부 사용자가 운영 중인 docker-compose.yml 파일을 가져와 **tracing, logging, metric telemetry** 데이터를 수집한 후, 이를 기반으로 머신러닝 분석 진행

1. **Isolation Forest 기반 이상 서비스 흐름 탐지**
2. **Graph Embedding (Node2Vec) 기반 서비스 간 의연성 분석**
3. **KMeans 기반 서비스 흐름 클러스터링**

---

### 시스템 구조

```
[사용자 Docker Compose 환경]
    ↓
[Our Analyzer System]
  ├─ docker-compose 실행
  ├─ 다양한 트래픽 시나리오 자동 생성 (100가지 흐름)
  ├─ Telemetry 수집: Zipkin, Prometheus, Elasticsearch
  └─ 분석 파이프라인 (Python)
       ├─ 전처리 (벡터화)
       ├─ 이상치 탐지 (Isolation Forest)
       ├─ 의연성 추출 (Trace Graph + Node2Vec)
       └─ 클러스터링 (KMeans)
```

---

### 구성 요소

| 구성 요소                                 | 설명                                      |
| ------------------------------------- | --------------------------------------- |
| `data_collector/collect_telemetry.sh` | 100가지 흐름의 트래픽 자동 생성 및 telemetry 수집 스크립트 |
| `telemetry_data.json`                 | 수집된 trace, log, metric 데이터를 통합한 JSON 파일 |
| `preprocessing/common_loader.py`      | 수집된 데이터를 벡터화 및 flatten 처리               |
| `anomaly/isolation_forest.py`         | 이상치 탐지를 위한 Isolation Forest 분석          |
| `graph/node2vec_analysis.py`          | 서비스 호출 그래프 기반 Node2Vec 임베딩              |
| `cluster/kmeans_clustering.py`        | KMeans를 통한 기능적 흐름 클러스터링                 |
| `visual/`                             | 분석 결과 시각화 이미지 저장 경로                     |

---

### Tech Stacks

* **Observability**: OpenTelemetry, Zipkin, Prometheus, Elasticsearch
* **ML/분석**: Scikit-learn, NetworkX, Node2Vec, Matplotlib, PCA
* **Backend**: FastAPI (서비스 구조 전제)
* **Container**: Docker, Docker Compose

---

* Developed by: MyLittleTelemetry
