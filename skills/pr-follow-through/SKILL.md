---
name: pr-follow-through
description: Carry an existing pull request through verified review fixes, merge-conflict resolution, targeted validation, and focused re-review without merging unless separately authorized.
license: MIT
---

# Follow through on an existing pull request

Use this only when the user has delegated changes to an existing pull request. Establish the exact
pull request, intended target branch, allowed scope, and current head before editing.

1. Read actionable review findings, failing checks, and target-branch conflicts.
2. Verify each finding against the current code. Fix confirmed in-scope defects; explain or defer
   unsupported findings rather than changing behavior merely to satisfy a comment.
3. Resolve conflicts against the intended target branch while preserving both sides' required
   behavior. Do not resolve by discarding one side wholesale.
4. Run the smallest affected tests and checks. If the resolution or fix materially changes reviewed
   behavior, run a focused re-review of that delta.
5. Recheck the pull request head, CI, and unresolved comments before reporting readiness.

Code review itself is read-only. This skill supplies the separately delegated write phase. Updating
the existing pull request does not authorize changing its scope, retargeting it, approving it, or
merging it. Merge only after explicit user authorization for that pull request and candidate head.
