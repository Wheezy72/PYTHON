# Python Mastery: Internals to Systems Architecture

A professional-grade learning repository for mastering Python from runtime internals through advanced system design. The curriculum is intentionally modular: every topic has isolated theory, errors, data-structure work, labs, solutions, and tests.

## Repository standards

1. **No cramming** — no topic should collapse into a single mega-file. Each topic uses `concepts/` with separate files for major sub-topics.
2. **Integrated DSA** — data structures and algorithms are treated as language features. Every concept must explain its underlying data structure and Big O behavior.
3. **Error-first design** — each topic has an `errors/` folder for relevant exceptions, failure modes, and defensive coding patterns.
4. **Test-driven learning** — every topic has a `tests/test_suite.py` file. Tests should validate behavior with `unittest` or `pytest`.
5. **Strict solution separation** — challenge prompts live in `lab/`; correct implementations live only in `solutions/`. Do not place solutions in challenge files.

## Incremental project proposal: SentinelFlow

**SentinelFlow** is a modular event-ingestion and monitoring platform built incrementally across all 15 topics. It starts as a small in-memory event model and grows into a production-style system with streaming, concurrency, networking, web APIs, a professional CLI, security controls, and deployment optimization.

By the end of the roadmap, SentinelFlow will support:

- structured event models and memory-aware data handling;
- indexed in-memory storage using lists, dictionaries, sets, queues, heaps, and caches;
- functional transformation pipelines with decorators and composable validators;
- extensible OOP architecture with interfaces, mixins, composition, and plugin-like components;
- lazy event streaming through iterators and generators;
- safe resource management through context managers;
- threaded, multiprocessing, and asyncio ingestion paths;
- durable file and binary stream persistence;
- TCP/UDP socket ingestion protocols;
- outbound and inbound REST API integrations;
- subprocess and OS-level operational hooks;
- a polished CLI for operators;
- security features for hashing, sanitization, and secret handling;
- profiling, bytecode inspection, packaging, and deployment-readiness checks.

### Why this project fits the curriculum

SentinelFlow is practical enough to resemble real backend tooling but bounded enough to implement topic by topic. It naturally exercises Python internals, DSA, OOP, async, sockets, IO, subprocesses, CLI architecture, security, and performance without feeling like disconnected exercises.

## Roadmap and project milestones

| Topic | Focus | SentinelFlow milestone |
| --- | --- | --- |
| 01 | Memory & Primitives | Define immutable and mutable event primitives; inspect identity, references, interning, and memory cost. |
| 02 | Linear DSA & Error Architecture | Build in-memory event indexes with lists, dicts, sets, and queues; add error taxonomy for invalid events. |
| 03 | Functional Mastery | Create decorator-based validation and transformation pipelines for events. |
| 04 | Advanced OOP | Introduce event processors, storage interfaces, mixins, ABCs, and composition-based services. |
| 05 | Iterator Protocol & Generators | Stream events lazily from generators and iterator-backed pipelines. |
| 06 | Context Managers | Manage event sessions, locks, files, and transactional cleanup with custom context managers. |
| 07 | Concurrency 1 | Add threaded and multiprocessing ingestion workers; compare GIL effects for CPU-bound and I/O-bound work. |
| 08 | Concurrency 2 | Add asyncio ingestion, async queues, cancellation handling, and event-loop-aware processors. |
| 09 | File Systems & Streams | Persist and replay events from JSON, JSONL, binary files, and buffered streams. |
| 10 | Network Sockets & Protocols | Implement TCP/UDP event ingestion with framing, parsing, timeouts, and protocol errors. |
| 11 | Advanced Web APIs | Add HTTPX-based API clients, REST endpoint integrations, retries, pagination, and rate limiting. |
| 12 | OS Interaction & Subprocesses | Add operational commands that call safe subprocesses, read environment config, and handle signals. |
| 13 | CLI Architecture | Build a professional `sentinelflow` CLI with subcommands, config, logging, and testable command handlers. |
| 14 | Security Operations | Add event sanitization, hashing, secret handling, cryptographic signing, and secure validation boundaries. |
| 15 | Deployment & Optimization | Profile hot paths, inspect bytecode, package the tool, and document deployment/optimization practices. |

## Required topic structure

Every topic follows this layout:

```text
topics/
  topic_NN_topic_slug/
    concepts/
    errors/
    dsa/
    lab/
    solutions/
    tests/
      test_suite.py
    README.md
```

### Folder responsibilities

- `concepts/` contains focused explanations and examples for individual sub-topics.
- `errors/` documents topic-specific exceptions, failure modes, and defensive coding techniques.
- `dsa/` contains data structure and algorithm implementations connected to the topic.
- `lab/` contains exactly three challenge prompts when a topic is implemented: entry, mid, and advanced. These files must not include solutions.
- `solutions/` contains correct challenge implementations only.
- `tests/` contains automated validation for concepts, DSA implementations, and lab solutions.
- `README.md` explains theory, complexity analysis, project milestone, and learning outcomes for the topic.

## Complexity standard

Every implementation should document:

- **Time complexity** — best, average, and worst case where relevant.
- **Space complexity** — auxiliary memory and total memory when useful.
- **Underlying structure** — list array storage, hash table behavior, linked structure, heap invariant, queue discipline, coroutine scheduling model, socket buffer, file buffer, or other mechanism.
- **Tradeoffs** — what the implementation optimizes for and what it sacrifices.

## Testing standard

Each topic should eventually include tests for:

1. core concept behavior;
2. DSA implementation correctness;
3. expected error handling and defensive behavior;
4. all three solution levels;
5. at least one integration-style smoke test using realistic SentinelFlow data.

Tests must not import or execute code from `lab/` as if it were a solution. Tests should validate the corresponding implementation in `solutions/` or reusable modules from `concepts/` and `dsa/`.

## Development sequence

The repository should be built incrementally. Topic 01 establishes the project vocabulary and runtime model. Each later topic extends SentinelFlow rather than creating an unrelated mini-project.

Recommended workflow per topic:

1. Write concept modules.
2. Add error deep dives and defensive patterns.
3. Implement relevant DSA modules.
4. Write three lab challenge prompts without solutions.
5. Add separate solutions.
6. Add and run tests.
7. Update the topic README with complexity analysis and the SentinelFlow milestone.

## Current status

This repository currently contains the approved curriculum scaffold. Topic implementations will begin after the project proposal is approved, starting with Topic 01: Memory & Primitives.
