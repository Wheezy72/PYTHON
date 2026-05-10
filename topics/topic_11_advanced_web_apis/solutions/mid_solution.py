"""Mid solution for Topic 11."""
from topics.topic_11_advanced_web_apis.concepts.pagination import paginate

def collect_pages(items, page_size):
    return tuple(paginate(items, page_size))
