---
name: code-review-fast
description: Review a bounded diff with one strong reviewer and report only actionable correctness, regression, security, or maintainability defects.
license: MIT
---

# Run a fast code review

Establish the exact base and head, applicable requirements, and changed behavior. Read enough
surrounding code and tests to understand call sites and invariants; do not review only isolated
patch lines.

Prioritize defects that can change behavior, lose data, weaken security, hide failure, break
compatibility, or make the change untestable. Ignore style preferences already covered by tools.

For every finding provide the source location, triggering conditions, concrete impact, evidence,
and smallest practical correction. Verify that the issue is introduced or exposed by the target
change. Do not invent findings to fill a quota.

Return a concise ordered list. If no actionable defect is supported, say what was checked and that
none was found.
