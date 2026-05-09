"""Advanced solution for Topic 04."""
from topics.topic_04_advanced_oop.concepts.composition import EventService
from topics.topic_04_advanced_oop.dsa.processor_pipeline import ProcessorPipeline
from topics.topic_04_advanced_oop.dsa.stores import InMemoryEventStore

def run_oop_ingestion(events, processors):
    store = InMemoryEventStore()
    pipeline = ProcessorPipeline(processors)
    service = EventService(store, [type("PipelineAdapter", (), {"process": staticmethod(pipeline.run)})()])
    accepted = [service.ingest(event) for event in events]
    return {"events": tuple(accepted), "store": store, "by_source": store.by_source(), "processor_count": len(pipeline)}
