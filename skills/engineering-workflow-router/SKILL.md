---
name: engineering-workflow-router
description: Select the smallest engineering workflow that matches task size, risk, uncertainty, and available tools without forcing every task through every skill.
license: MIT
---

# Route engineering work

Start by identifying the requested outcome, affected system, change size, uncertainty, production
impact, security or privacy sensitivity, performance or concurrency sensitivity, and whether source
may leave the current environment. Discover available tools and models; do not assume every runtime
supports subagents, MCP, local models, or hosted providers.

## Select a proportionate workflow

| Situation | Workflow |
| --- | --- |
| Small understood bug | implement, targeted verification, `code-review-fast` |
| Unclear bug | `systematic-debugging`, implement, targeted verification |
| Normal feature | `requirements-clarification`, design only if needed, implement, fast review |
| Large feature | requirements, `software-design`, independent design challenge, work items, comprehensive review |
| Architecture change | codebase investigation, design proposal, comprehensive design review, synthesis |
| Normal PR | `code-review-fast` |
| Important production PR | `review-suite`; add independent models only when authorized and useful |
| Address verified PR findings or conflicts | `pr-follow-through`, targeted verification, focused re-review |
| Security-sensitive change | `review-security` plus correctness and test-quality review |
| Performance/concurrency change | `review-performance-concurrency` plus correctness review |
| Test infrastructure change | `review-test-quality` plus regression analysis |
| Work item refinement | `work-item-planning` |
| Formal bounded specification | `specification-authoring` |
| New or unclear issue | `issue-triage`, then debugging or planning as evidence warrants |
| Test strategy | `test-planning` |
| Implementation against a ticket | `review-spec-compliance` plus correctness review |

Use the deterministic helper when a runtime cannot route skills itself:

`python tools/route_task.py "<task>" --size small|medium|large [--production-impact]`

## Review mode

- **Fast:** one strong reviewer checks the whole diff for actionable defects.
- **Comprehensive:** independent specialized passes for correctness, specification compliance,
  silent failures, tests, security, performance/concurrency, types/interfaces, and simplification.
- **Independent multi-model:** different authorized model/provider adapters inspect the same frozen
  target without seeing one another's findings, followed by evidence-based reconciliation.

Choose independent multi-model review only for high-impact, architecturally significant, unusually
complex, or disputed work. Prefer one strong reviewer to several weak or redundant reviewers.
Never send proprietary code outside its approved boundary without explicit authorization.

Review skills are read-only unless the user separately delegates implementation. After delegated
fixes or conflict resolution, rerun affected checks and review materially changed code. Resolving a
merge conflict is not permission to merge the pull request; merge remains a separate explicit
authorization.

## Finish

State the selected workflow and why in one or two sentences. Invoke only the needed skills. If a
tool or integration is unavailable, use the portable parts and report the missing capability
plainly; do not simulate a real integration or model run.
