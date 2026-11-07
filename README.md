# Portable engineering skills platform

A curated, version-controlled collection of small engineering skills for planning, design, review,
debugging, and verification. It keeps portable instructions separate from runtime adapters and
machine settings, so the same repository can be deployed to multiple machines without copying
credentials or changing global model configuration.

## Start here

Preview before installing:

```powershell
python tools\skillsctl.py --target copilot-user plan
```

Install, inspect, and safely undo:

```powershell
python tools\skillsctl.py --target copilot-user install
python tools\skillsctl.py --target copilot-user status
python tools\skillsctl.py --target copilot-user rollback
```

After cloning the package on another machine, pull a reviewed package update and refresh the managed
installation with:

```powershell
python tools\update_platform.py package
```

Check and safely stage newer revisions of all allowlisted upstream sources, including Superpowers:

```powershell
python tools\update_platform.py upstreams
```

Upstream staging produces a source/license/diff report; it does not install native plugins or
automatically rewrite the curated skills. See [updating](docs/updating.md).

On macOS or Linux, use the same commands with `/` path separators. Python 3.10 or newer is the only
installer dependency.

The package provides 27 independently invocable skills. Start with
`engineering-workflow-router`; it selects a fast workflow for routine work and specialized or
independent reviews only when risk justifies them.

## Use review skills in GitHub Copilot

In a Copilot session, name the skill in the request. This is the most reliable explicit invocation
and still lets Copilot load the repository, pull request, and requirements context:

```text
Use the code-review-fast skill to review this PR. Report only actionable defects.
```

```text
Use the review-suite skill to run a targeted comprehensive review of this production PR.
Include correctness, specification compliance, silent failures, and test quality.
Add security, performance/concurrency, or type/interface review only if the diff exposes that risk.
Deduplicate and verify every finding against the code.
```

```text
Use review-silent-failures and review-test-quality to review this PR for hidden error paths,
misleading success, missing propagation, and regression gaps.
```

Choose the mode by risk:

- **Fast (`code-review-fast`):** normal PRs, small fixes, and low-risk follow-ups.
- **Targeted comprehensive (`review-suite`):** production changes, linked PR sets, migrations,
  shared libraries, or changes with meaningful CI/operational scope. Review each frozen PR revision
  separately and preserve the foundational PR's behavior and dependent-CI scope while checking
  dependent PRs.
- **Independent models (`independent-multi-model-review`):** only for unusually important,
  disputed, or architecturally significant changes after explicitly authorizing the models,
  providers, cost, and source-sharing boundary. It is not the default for ordinary PR review.

For several related PRs, avoid one blended review. Review each PR against its own base/head and work
item, then perform one final cross-PR pass for dependency, ordering, duplicated changes, and gaps.

Review skills are read-only. When you want Copilot to act on the result, delegate that separately:

```text
Use pr-follow-through on this existing PR. Fix verified in-scope findings, resolve target-branch
conflicts while preserving both intended behaviors, run affected checks, and re-review material
changes. Do not merge without my separate approval.
```

## What is and is not included

- **Included:** portable `SKILL.md` instructions, deterministic routing, reversible deployment,
  review reconciliation, and an actual Ollama HTTP adapter.
- **Packaged but not activated:** an Azure DevOps MCP least-privilege template and hosted-model
  review guidance. Authentication and provider permission remain machine-local decisions.
- **Not included:** credentials, proprietary source, machine-specific paths, copied upstream skill
  content, paid provider calls, or changes to global model settings.

See [the inventory](docs/inventory.md), [usage guide](docs/usage.md),
[multi-machine deployment and rollback](docs/deployment.md),
[safe package and upstream updates](docs/updating.md),
[review and design policies](docs/policies.md),
[source provenance](docs/provenance.md), [Azure DevOps integration](docs/azure-devops-mcp.md), and
[validation results](docs/validation.md). The [research record](docs/research-record.md) lists the
files and local capabilities actually checked.
