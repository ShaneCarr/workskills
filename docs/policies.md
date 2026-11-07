# Engineering review and design policies

## Review selection

Use one strong reviewer for ordinary changes. Add specialists only for risks present in the change.
Use a comprehensive suite for large or production-critical work. Use different models or providers
only when independent perspective is worth the cost and the source-sharing boundary is authorized.

Every reported defect needs a source location, triggering conditions, concrete impact, evidence,
and a minimal correction. Reconciliation removes duplicates and rejects findings that are
speculative, unrelated to the target revision, or unsupported by code.

Review is read-only. A user can separately delegate `pr-follow-through` to fix verified findings,
resolve conflicts, run targeted validation, and re-review material changes. Conflict resolution and
PR updates never imply approval to merge; merge requires separate explicit authorization.

## Design review

Lightweight design review checks requirement fit, integration boundaries, failure behavior,
compatibility, verification, and unnecessary complexity.

Comprehensive design review freezes one proposal and uses independent perspectives:

1. investigate the existing code and constraints;
2. propose or defend a solution;
3. challenge architecture, lifecycle, and failure modes;
4. seek a materially simpler alternative; and
5. verify evidence and synthesize one recommendation.

Do not use the comprehensive process for trivial changes. A different model is optional; reviewer
independence and evidence matter more than provider count.

## Model and cost policy

Prefer the strongest available reviewer appropriate to the task. Local models are useful when they
can reliably handle the context and language. Escalate to hosted models for high complexity or
important independent review, subject to authorization and cost. Never treat prompt rendering,
fixtures, mocks, or repeated calls to one model as a real multi-model review.
