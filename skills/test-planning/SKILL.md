---
name: test-planning
description: Build a risk-based test plan that maps requirements and failure modes to the smallest effective test boundaries.
license: MIT
---

# Plan tests by risk

Map requirements, invariants, interfaces, failure modes, and rollout risks to tests. Choose the
lowest stable boundary that can distinguish correct from incorrect behavior.

Cover relevant positive, negative, boundary, compatibility, migration, authorization, concurrency,
recovery, and observability cases. Do not include categories unrelated to the change.

For each test state the behavior, setup, stimulus, expected result, boundary, and why the test is
needed. Identify what remains manual, fixture-only, integration-dependent, or unsupported. Avoid
duplicating the implementation in test logic.
