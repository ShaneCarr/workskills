---
name: review-suite
description: Orchestrate independent specialized code reviews, verify and deduplicate their findings, and produce one concise comprehensive review.
license: MIT
---

# Run a comprehensive review suite

Freeze the target revision, requirements, and allowed data boundary. Run specialized reviewers
independently and in parallel when the runtime supports it:

- general correctness;
- `review-spec-compliance`;
- `review-silent-failures`;
- `review-test-quality`;
- `review-security` when the change crosses a security boundary;
- `review-performance-concurrency` when load or concurrency is relevant;
- `review-type-interface` for contract changes; and
- `review-simplification`.

Do not invoke irrelevant reviewers merely to reach a fixed count. Each reviewer reports only
actionable findings with source evidence, trigger, impact, and minimal correction.

Reconcile after all first passes:

1. group equivalent findings;
2. verify each against the actual code and target revision;
3. reject speculative or pre-existing unrelated issues;
4. distinguish confirmed defects from concerns needing measurement;
5. note independent rediscovery without treating votes as proof; and
6. rank by concrete impact and confidence.

Return one concise review, not concatenated reports. If independent agents are unavailable, run the
same checks sequentially and label the execution mode accurately.

This skill is read-only. Do not edit code, resolve conflicts, post comments, approve, or merge merely
because findings were produced. If the user delegates remediation, hand confirmed findings to
`pr-follow-through`, then run targeted verification and a focused re-review of material changes.
