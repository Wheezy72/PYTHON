"""Advanced solution for Topic 07."""
from topics.topic_07_concurrency_threading_multiprocessing.dsa.threaded_ingestion import ingest_threaded
from topics.topic_07_concurrency_threading_multiprocessing.errors.worker_failures import collect_worker_result

def _normalize_batch(records):
    return ingest_threaded(records)

def run_concurrent_ingestion(events, max_workers=4):
    records = tuple(events)
    try:
        accepted = ingest_threaded(records, max_workers=max_workers)
        return {"events": accepted, "errors": tuple(), "count": len(accepted)}
    except (KeyError, TypeError, ValueError):
        pass
    results = tuple(collect_worker_result(lambda e: ingest_threaded((e,), max_workers=max_workers)[0], e) for e in records)
    accepted = tuple(item["value"] for item in results if item["ok"])
    errors = tuple(item for item in results if not item["ok"])
    return {"events": accepted, "errors": errors, "count": len(accepted)}
