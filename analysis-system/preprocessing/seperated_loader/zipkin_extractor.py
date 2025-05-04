# zipkin_extractor.py
import requests

def extract_zipkin():
    response = requests.get("http://localhost:9411/api/v2/traces?limit=5")
    traces = []
    for trace in response.json():
        for span in trace:
            traces.append({
                "trace_id": span.get("traceId"),
                "span_id": span.get("id"),
                "service_name": span.get("localEndpoint", {}).get("serviceName"),
                "endpoint": span.get("name"),
                "duration": span.get("duration"),
                "attributes": span.get("tags", {})
            })
    return traces

if __name__ == "__main__":
    from pprint import pprint
    pprint(extract_zipkin())
