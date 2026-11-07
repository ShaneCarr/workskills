---
name: review-spec-compliance
description: Check an implementation against its approved work item, requirements, acceptance criteria, and explicit non-goals.
license: MIT
---

# Review specification compliance

Identify the authoritative requirement set and exact implementation revision. Map each acceptance
criterion and invariant to source and verification evidence. Distinguish missing behavior from a
different but valid implementation.

Find omitted cases, behavior outside scope, weakened guarantees, incompatible defaults, and tests
that prove only a proxy. Cite both the requirement and code. Do not treat proposal text or current
behavior as approved authority unless the repository says it is.

Report a compact compliance matrix, then only material gaps. Mark untestable or ambiguous criteria
as requirement issues rather than code defects.
