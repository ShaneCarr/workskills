---
name: review-performance-concurrency
description: Review changed code for algorithmic cost, blocking work, fan-out, resource growth, races, deadlocks, ordering, and cancellation defects.
license: MIT
---

# Review performance and concurrency

Identify expected load, latency or throughput goals, shared state, scheduling model, resource
limits, and lifecycle. Trace hot paths and concurrency boundaries rather than inferring performance
from syntax.

Check algorithmic complexity, repeated I/O, unbounded collections or tasks, cache behavior,
serialization, lock order, atomicity, race windows, cancellation, timeout, retry amplification,
backpressure, and cleanup.

Every finding needs the triggering workload or interleaving, affected resource or invariant,
expected impact, and evidence. Recommend measurement when impact is uncertain. Do not call a
micro-optimization a defect without a relevant threshold.
