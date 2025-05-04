## 📘 README.md — Telemetry-based Microservice Analysis System

### 🧠 프로젝트 개요

본 시스템은 외부 사용자가 운영 중인 FastAPI 기반 마이크로서비스 애플리케이션에서 **tracing, logging, metric telemetry** 데이터를 수집한 후, 이를 기반으로 다음의 **세 가지 분석**을 자동 수행합니다:

1. **Isolation Forest 기반 이상 서비스 흐름 탐지**
2. **Graph Embedding (Node2Vec) 기반 서비스 간 의연성 분석**
3. **KMeans 기반 서비스 흐름 클러스터링**

사용자는 다른 필요 없이 `docker-compose.yml`만 제공하면, 본 시스템이 이를 실행해 데이터를 수집하고 JSON 기반 리포트를 생성합니다.

---

### ⚙️ 시스템 구조

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

### 📦 구성 요소

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

### 🚀 실행 순서

#### 1. 사용자 Docker Compose 실행 및 수집

```bash
bash collect_telemetry.sh  # default TRACE_COUNT=1000
```

→ `telemetry_data.json` 자동 생성

#### 2. 분석 파이프라인 실행

```bash
python run_analysis.py  # 내부적으로 preprocessing → 이상치 탐지 → 클러스터링 실행
```

→ 결과는 `visual/` 폴더 및 `result/analysis.json`에 저장

---

### 📊 생성 리포트 예시

* `anomaly_detect_plot.png` : 이상 흐름 시각화
* `dependency_graph.png` : 서비스 간 호출 관계 시각화 (Node2Vec)
* `cluster_result.png` : KMeans를 통한 서비스 흐름 그룹화
* `analysis.json` : 분석 결과 요약 (이상치 인덱스, 의존성 매트릭스, 클러스터 ID)

---

### 📊 사용된 기술 스택

* **Observability**: OpenTelemetry, Zipkin, Prometheus, Elasticsearch
* **ML/분석**: Scikit-learn, NetworkX, Node2Vec, Matplotlib, PCA
* **Backend**: FastAPI (서비스 구조 전제)
* **Container**: Docker, Docker Compose

---

### 🔐 할 수 목표

* 사용자별 리포트 자동 전송 기능 추가
* 실시간 스트리밍 기반 이상 탐지 (Kafka 연계)
* Flow Replay 기능 (이상 흐름 재현)

---

### 👤 개발자

* Designed by: \[답변자 이름 or 팀명]
* Contact: \[전자메일/LinkedIn]
