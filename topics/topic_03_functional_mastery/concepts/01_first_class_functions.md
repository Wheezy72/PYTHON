# First-Class Functions

In Python, functions are first-class values: SentinelFlow can assign validators to variables, store predicates in lists, map route names to handlers in dictionaries, and pass transformers into pipeline runners. The ingestion engine only needs a callable contract; each stage owns its validation or transformation details.

SentinelFlow example: a route can keep ordered stages such as `require_fields`, `normalize_level`, and `add_route`. The route runner traverses the stage list and calls each function with the current event.

Underlying data structures include function objects, tuples/lists of stage references, dictionaries mapping names to callables, and call stack frames created for each invocation.

Complexity: passing a function reference is O(1) time and O(1) space. Traversing `s` stages is O(s) plus stage work. Storing `s` stage references uses O(s) space. This keeps pipeline orchestration cheap while allowing each event stage to stay independently testable.
