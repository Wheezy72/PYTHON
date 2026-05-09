"""Mid solution for Topic 04."""
from topics.topic_04_advanced_oop.dsa.processor_registry import ProcessorRegistry
from topics.topic_04_advanced_oop.dsa.stores import InMemoryEventStore

def configure_registry(processors):
    registry = ProcessorRegistry()
    for name, processor in processors.items():
        registry.register(name, processor)
    return registry

def build_store(events=()):
    store = InMemoryEventStore()
    for event in events:
        store.add(event)
    return store
