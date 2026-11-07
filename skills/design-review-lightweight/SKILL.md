---
name: design-review-lightweight
description: Challenge a bounded software design for requirement fit, integration risks, and unnecessary complexity without creating a heavyweight review process.
license: MIT
---

# Review a design lightly

Read the proposal, requirements, and the narrow source paths it changes. Check whether the design:

- satisfies the required behavior and failure cases;
- fits current ownership and module boundaries;
- preserves compatibility and rollback;
- introduces unnecessary concepts or configuration;
- has a plausible verification plan; and
- leaves consequential assumptions unstated.

Report only material findings. For each, cite the affected decision and evidence, explain the
failure or cost, and give the smallest correction. End with proceed, revise, or a specific unresolved
decision. Do not restate the whole design.
