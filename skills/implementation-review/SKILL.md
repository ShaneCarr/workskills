---
name: implementation-review
description: Review completed implementation against the approved design, repository patterns, operational needs, and verification plan before submission.
license: MIT
---

# Review implementation completeness

Compare the final diff with requirements and design decisions. Confirm every relevant surface is
wired: callers, interfaces, configuration, persistence, lifecycle, error handling, observability,
tests, documentation, rollout, and rollback.

Find deviations that alter behavior or leave the design incomplete. A simpler implementation is
acceptable when it preserves requirements; document meaningful intentional deviations instead of
demanding literal design conformance.

Run the applicable specialized review skills for exposed risks, then use
`verification-before-completion` before submission.
