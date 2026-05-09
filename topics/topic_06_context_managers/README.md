# Topic 06: Context Managers

Topic 06 gives SentinelFlow deterministic resource management through the context manager protocol, `contextlib`, ExitStack, transactional buffers, and explicit exception behavior.

## SentinelFlow milestone

Manage event sessions, locks, files, and transactional cleanup with custom context managers.

## Complexity overview

| Operation | Time | Space | Structure |
| --- | ---: | ---: | --- |
| Enter or exit one manager | O(1) | O(1) | Object protocol |
| Commit n buffered events | O(n) | O(n) | List buffer |
| ExitStack cleanup | O(k) | O(k) | Stack of callbacks |
| Transaction rollback | O(1) | O(n) retained buffer | List clear |

## Tests

```bash
python -m unittest discover -s topics/topic_06_context_managers/tests -p 'test_suite.py'
```
