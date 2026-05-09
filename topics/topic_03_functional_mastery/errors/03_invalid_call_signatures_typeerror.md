# Invalid Call Signatures and TypeError

Failure mode: a pipeline expects unary stages but receives a non-callable object or a function that requires additional arguments. Python raises `TypeError`, often far from the pipeline construction site.

SentinelFlow example: a transformer defined as `transform(event, route)` is placed in a pipeline that calls every stage with only the event. A raw `TypeError` does not clearly identify the broken stage contract.

Defensive pattern: check `callable()` before running stages, keep stages unary by using closures or partial application for configuration, and wrap signature `TypeError` exceptions in a domain-specific `PipelineError`.

Complexity impact: validating `s` stages costs O(s). Defensive call wrapping adds O(1) overhead per stage. The asymptotic behavior stays the same while diagnostics become much clearer.
