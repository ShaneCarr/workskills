# Usage guide

Use `engineering-workflow-router` when the right workflow is unclear. It chooses the smallest useful
set of capabilities and explains why.

## Common requests

| Request | Primary capability |
| --- | --- |
| "Turn this discussion into concise work items." | `work-item-planning` |
| "Write a bounded specification from these approved decisions." | `specification-authoring` |
| "Triage this issue without assuming a root cause." | `issue-triage` |
| "Clarify the acceptance boundary before implementation." | `requirements-clarification` |
| "Explore the architecture and propose the simplest design." | `software-design` |
| "Challenge this architecture and propose a simpler alternative." | `design-review-lightweight` or `design-review-comprehensive` |
| "Review this PR." | `code-review-fast` |
| "Fix verified review findings and resolve this PR's conflicts, but do not merge." | `pr-follow-through` |
| "Review this PR for silent failures and test gaps." | `review-silent-failures` + `review-test-quality` |
| "Run a comprehensive review of this production change." | `review-suite` |
| "Run an independent multi-model review of this public fixture." | `independent-multi-model-review` |
| "Debug this regression from the first incorrect state." | `systematic-debugging` |
| "Verify this implementation before completion." | `verification-before-completion` |
| "Create a risk-based test plan for this feature." | `test-planning` |
| "Review the implementation against its work item." | `review-spec-compliance` + `implementation-review` |

## Review modes

**Fast review** uses one strong reviewer across the whole diff. It is the default for ordinary pull
requests and small fixes.

**Comprehensive review** runs only the relevant specialized reviewers. Correctness, specification
compliance, silent failures, and tests are common; security, performance/concurrency, types, and
simplification are added when the change exposes those risks.

**Independent multi-model review** is for important, complex, disputed, or high-impact work. The
target revision is frozen, reviewers work independently, and reconciliation verifies every finding
against code. Agreement is useful metadata, not proof.

Do not send proprietary source to a hosted or remote model without explicit authorization. A local
Ollama endpoint still needs an installed model and enough hardware; a `SKILL.md` file does not make
Ollama an agent.

All review skills are read-only. Use `pr-follow-through` only after delegating edits to an existing
pull request. It can fix verified findings, resolve target-branch conflicts, run affected checks,
and trigger focused re-review. Conflict resolution does not authorize approval or merge.

## Handling disagreement

Compare the invariant each reviewer believes is violated, the triggering conditions, and the cited
source. Reproduce or inspect the decisive path. Narrow or reject findings unsupported by code.
Preserve genuine trade-offs for a human decision instead of counting reviewer votes.

## Local model example

List models from a local Ollama server:

```powershell
python adapters\ollama_review.py --list-models
```

Review a public, synthetic, or explicitly authorized file:

```powershell
python adapters\ollama_review.py --model <installed-model> --input <file>
```

Remote Ollama hosts are rejected unless `--allow-remote` is passed deliberately.

## Azure DevOps

The skills produce provider-neutral plans when Azure DevOps is unavailable. When the official MCP
server is configured, begin with read-only discovery and preview any work-item, pull-request, or
comment mutation. See [Azure DevOps MCP integration](azure-devops-mcp.md).
