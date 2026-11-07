---
name: verification-before-completion
description: Verify the exact requested outcome before claiming completion, distinguishing static checks, fixtures, mocks, and live integrations.
license: MIT
---

# Verify before completion

Restate the measurable outcome and choose the smallest checks that prove it. Run relevant tests,
type checks, lint, builds, and direct reproductions. Escalate to broader suites only when risk or
failures justify it.

For integrations, distinguish:

- file or configuration presence;
- static validation;
- fixture or mocked execution;
- local runtime execution;
- authenticated live integration; and
- production-like end-to-end validation.

Do not call one level proof of another. Record commands, results, environment limits, and
unsupported capabilities. Fix failures caused by the change before reporting completion.
