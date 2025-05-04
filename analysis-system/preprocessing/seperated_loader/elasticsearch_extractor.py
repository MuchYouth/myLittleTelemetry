# elasticsearch_extractor.py
from elasticsearch import Elasticsearch

def extract_logs():
    es = Elasticsearch("http://localhost:9200")
    res = es.search(index="*", size=5, body={"query": {"match_all": {}}})
    logs = []
    for hit in res["hits"]["hits"]:
        src = hit["_source"]
        logs.append({
            "time": src.get("time"),
            "level": src.get("level"),
            "message": src.get("message"),
            "service": src.get("service"),
            "trace_id": src.get("trace_id"),
            "user_id": src.get("user_id")
        })
    return logs

if __name__ == "__main__":
    from pprint import pprint
    pprint(extract_logs())
