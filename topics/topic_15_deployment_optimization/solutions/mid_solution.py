"""Mid solution for Topic 15."""
from topics.topic_15_deployment_optimization.concepts.caching import normalized_source

def normalize_sources(sources):
    return tuple(normalized_source(source) for source in sources)
