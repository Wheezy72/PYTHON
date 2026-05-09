# Defensive Pipeline Errors

Failure mode: ingestion code accepts invalid events or malformed stage output and continues until a later stage fails with a misleading exception.

SentinelFlow example: a collector sends a list instead of an event dictionary. If the boundary does not reject it, later code may behave incorrectly while checking fields like `level` or `latency_ms`.

Defensive pattern: reject non-dict events immediately with `ValidationError`, require transformers to return dictionaries, use `ValidationError` for bad event data, use `PipelineError` for bad stages or signatures, and avoid mutating inputs so rejected events remain inspectable.

Complexity impact: type checks are O(1). Required-field checks are O(f). Copying an event dictionary to preserve input state is O(k) time and O(k) space.
