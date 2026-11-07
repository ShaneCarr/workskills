---
name: design-review-comprehensive
description: Run independent architecture, failure-mode, and simplification challenges against an important design, then synthesize one evidence-based recommendation.
license: MIT
---

# Review an important design independently

Freeze one design revision and shared requirement brief. Use the runtime's independent-agent
capability when available:

1. one investigator maps current code and constraints;
2. one designer proposes or defends the solution;
3. one independent challenger examines boundaries, failure modes, lifecycle, and operations;
4. one simplifier looks for a smaller design and unnecessary abstraction; and
5. a coordinator verifies decisive evidence and synthesizes the recommendation.

Do not let independent reviewers see prior findings during their first pass. Different perspectives
may use the same strong model; multiple providers are optional and require authorization.

Each finding needs a violated requirement or invariant, concrete evidence, triggering conditions,
impact, and minimal correction. Reviewers must attempt to disprove their strongest concern.

The synthesis deduplicates equivalent findings, rejects speculation, preserves meaningful
disagreement, and compares the strongest alternative. Model agreement is not proof. If independent
execution is unavailable, run a transparent single-reviewer fallback and label it accurately.
