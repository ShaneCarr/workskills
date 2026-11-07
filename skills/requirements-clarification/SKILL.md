---
name: requirements-clarification
description: Clarify engineering requirements, authority, invariants, edge cases, and acceptance boundaries before design or implementation.
license: MIT
---

# Clarify requirements

Read repository instructions and authoritative requirements before inferring behavior from code.
Separate approved requirements, current implementation, proposals, and assumptions.

Produce the smallest useful clarification:

1. desired user or system outcome;
2. in-scope and out-of-scope behavior;
3. actors, triggers, inputs, outputs, and failure behavior;
4. compatibility, security, privacy, lifecycle, and operational constraints;
5. observable acceptance criteria; and
6. unresolved decisions that materially affect the solution.

Prefer examples and counterexamples over abstract wording. Do not invent product policy to remove
ambiguity. If a decision is reversible and low risk, state a reasonable assumption and proceed. If
it affects contracts, data loss, access, cost, or external behavior, surface the decision.

Stop when implementation and verification can proceed without materially different interpretations.
