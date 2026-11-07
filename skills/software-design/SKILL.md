---
name: software-design
description: Explore an existing codebase and produce a simple, evidence-grounded software design with interfaces, data flow, alternatives, and meaningful trade-offs.
license: MIT
---

# Design software proportionately

Trace the current system before proposing new abstractions. Identify relevant modules, ownership,
data flow, interfaces, persistence, configuration, failure handling, tests, and deployment
boundaries. Cite source where it constrains the design.

Define the required behavior and invariants, then propose the smallest coherent change. Describe:

- components and responsibilities;
- public interfaces and data contracts;
- primary and failure-path flow;
- state, lifecycle, migrations, and rollback;
- security, privacy, observability, and operational impact;
- compatibility and staged delivery; and
- verification strategy.

Compare at least one credible alternative, including extending the existing pattern or making no
change. Evaluate complexity, coupling, failure modes, migration cost, and reversibility rather than
listing generic pros and cons.

Avoid speculative frameworks, premature generalization, and abstractions with only one foreseeable
use. For important decisions invoke an independent design review; for routine local changes, a
brief self-check is enough.
