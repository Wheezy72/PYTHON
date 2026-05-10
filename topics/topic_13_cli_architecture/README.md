# Topic 13: CLI Architecture

This topic extends SentinelFlow with production-oriented Python systems skills while preserving the repository rules: modular concepts, explicit error handling, integrated DSA, separated labs, separated solutions, and automated tests.

## SentinelFlow milestone

Build a professional sentinelflow CLI with subcommands, config, logging, and testable handlers.

## Complexity overview

| Operation | Time | Space | Backing structure |
| --- | ---: | ---: | --- |
| Validate one record/request | O(f) | O(f) | Dictionary fields |
| Build an index or summary | O(n) | O(k) | Hash table / list |
| Stream or pipeline n items | O(n * c) | O(1) to O(n) | Iterator/list depending on output |
| Encode/decode payload | O(b) | O(b) | Bytes buffer |

## Learning outcomes

- Connect the topic's Python API to SentinelFlow's event-processing architecture.
- Explain time and space complexity instead of treating APIs as magic.
- Handle failures explicitly with small defensive helpers.
- Keep exercises and reference implementations physically separated.

## Module guide

- `concepts/` contains focused theory-backed helper modules.
- `errors/` contains defensive failure-mode modules.
- `dsa/` contains reusable structures used by the solutions.
- `lab/` contains prompt-only challenge files.
- `solutions/` contains importable reference implementations.
- `tests/test_suite.py` validates the slice.

## Running tests

```bash
python -m unittest discover -s topics/topic_13_cli_architecture/tests -p 'test_suite.py'
```
