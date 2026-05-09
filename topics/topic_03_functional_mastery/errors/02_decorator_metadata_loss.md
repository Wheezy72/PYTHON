# Decorator Metadata Loss

Failure mode: a decorator returns a wrapper without `functools.wraps`. Logs, tracebacks, tests, and introspection then see a generic name like `wrapper` instead of the original SentinelFlow stage.

SentinelFlow example: an audited validation stage appears in monitoring as `wrapper`, hiding whether field validation, level validation, or routing failed.

Defensive pattern: use `functools.wraps(func)` on every wrapper. Test `__name__`, `__doc__`, and `__wrapped__`. Store audit metadata explicitly on the wrapper rather than replacing function identity.

Complexity impact: `wraps` performs O(1) metadata copying for normal functions. Each wrapper call adds O(1) overhead and one extra stack frame. A small audit metadata dictionary uses O(1) space.
