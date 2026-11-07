---
name: test-driven-development
description: Implement behavior through a focused failing test, the smallest complete change, and refactoring under passing tests.
license: MIT
---

# Develop with focused tests

Understand the required behavior and choose the narrowest stable test boundary. First reproduce the
missing behavior or defect with a test that fails for the expected reason. Avoid mocking away the
logic under test.

Implement the smallest complete production change that satisfies the behavior, including relevant
failure handling. Run the focused test, then refactor while it remains green. Run the affected
suite and static checks afterward.

Do not force test-first work when the task is exploratory, documentation-only, or requires a
prototype to discover the interface. In those cases, time-box exploration and add durable tests
once behavior is known.
