# Function Composition

Function composition combines small functions into a larger function. SentinelFlow uses composition to express the path from raw ingress data to validated, normalized, enriched output.

`compose(f, g)(x)` runs right-to-left as `f(g(x))`. `pipe(x, f, g)` runs left-to-right and often reads better for event ingestion: validate, normalize, route, enrich.

Underlying structures include tuples of function references, call stack frames for each stage, and intermediate event dictionaries returned by pure transformers.

Complexity: applying `s` stages is O(s) plus stage work. If each transformer copies an event with `k` keys, `s` copying stages can cost O(s * k) time and allocate O(k) per stage. Defensive composition should reject non-callable stages and wrap invalid signatures in clear `PipelineError` exceptions.
