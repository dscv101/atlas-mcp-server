---
type: "always_apply"
---

07-memory

Purpose
Provide guidance on writing memory‑efficient Python 3.13 so that AI‑generated code scales well in production.

Rules
	1.	Data structures – Choose the smallest suitable collection (array, deque, bisect) before list.
	2.	Streaming – Process large files/streams lazily (yield from, iter_chunks); avoid loading all into memory.
	3.	Slots – Use data classes with slots=True or regular classes with __slots__ to reduce per‑instance overhead.
	4.	Immutable over mutable – Prefer tuples, types.MappingProxyType, and frozen dataclasses for shared data.
	5.	Memory profiling – Use memory‑profiler in CI for large modules; fail if regression >5 %.
	6.	Garbage collection – Explicitly break reference cycles; use contextlib.ExitStack for many contexts.
	7.	Vectorization – Use numpy or pyarrow for numeric workloads; avoid Python loops.
	8.	Cache wisely – Use functools.cache/lru_cache(maxsize=…) with eviction strategy; document cache lifetime.
	9.	Chunked concurrency – For async generators, limit concurrency via asyncio.Semaphore.
	10.	Monitor – Emit Prometheus metrics for RSS, heap usage; set alerts at 75 % of container limit.
