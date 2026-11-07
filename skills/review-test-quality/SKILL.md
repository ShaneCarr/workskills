---
name: review-test-quality
description: Review whether tests cover changed behavior, meaningful negative paths, and regressions without rewarding line count or brittle implementation coupling.
license: MIT
---

# Review test quality

Map changed behavior and risks to existing and new tests. Check positive, negative, boundary,
failure, concurrency, migration, and compatibility cases only where relevant.

Identify tests that pass without exercising the changed path, assert the wrong outcome, mock away
the behavior under review, depend on timing, duplicate implementation logic, or leave critical
failure paths untested.

Prefer the smallest stable test at the correct boundary. Treat coverage percentages as supporting
data, not proof. Report only gaps likely to permit a real regression, with the behavior the missing
test must distinguish.
