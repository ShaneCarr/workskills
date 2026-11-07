---
name: systematic-debugging
description: Reproduce a defect, narrow it with evidence, identify the earliest incorrect state, and verify a root-cause fix.
license: MIT
---

# Debug systematically

Capture the exact symptom, environment, revision, inputs, expected result, and reproducibility.
Separate observed facts from hypotheses. Create the smallest reliable reproduction before changing
code when feasible.

Trace backward from the visible failure to the earliest incorrect state. Compare working and
failing cases, inspect boundaries, and add focused diagnostics or tests. Change one hypothesis at a
time.

Fix the root cause rather than suppressing the signal. Preserve useful assertions and safety
checks. Verify the reproduction, relevant regression tests, and adjacent behavior. State any
remaining untested hypothesis plainly.
