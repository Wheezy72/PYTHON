"""Entry solution for Topic 11."""
from topics.topic_11_advanced_web_apis.concepts.rest_requests import build_url, build_headers

def build_event_request(base, event_id, token=None):
    return {"url": build_url(base, f"events/{event_id}"), "headers": build_headers(token)}
