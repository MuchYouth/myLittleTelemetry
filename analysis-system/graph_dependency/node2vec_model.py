import json
import networkx as nx
from node2vec import Node2Vec
import matplotlib.pyplot as plt

# 1. 전처리된 엣지 로딩
with open("../preprocessing/result.json") as f:
    result = json.load(f)

edges = result["edges"]

# 2. 그래프 구성
G = nx.DiGraph()
G.add_edges_from(edges)

# 3. Node2Vec 임베딩
node2vec = Node2Vec(G, dimensions=16, walk_length=10, num_walks=100, workers=1)
model = node2vec.fit(window=5, min_count=1)

print("[✓] Service Embeddings:")
for node in G.nodes:
    embedding = model.wv[node]
    print(f"{node}: {embedding.tolist()}")

# 4. 그래프 시각화
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)  # 노드 위치 자동 배치

# 노드와 엣지 시각화
nx.draw_networkx_nodes(G, pos, node_size=700, node_color="skyblue", edgecolors="black")
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=15)
nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

plt.title("Service Dependency Graph")
plt.axis("off")
plt.tight_layout()
plt.savefig("./visual/dependency_graph.png")
print("[✓] Saved dependency graph to dependency_graph.png")

