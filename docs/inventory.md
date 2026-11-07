# Platform inventory

Platform version: `0.2.0`.

## Portable skills

| Area | Skills |
| --- | --- |
| Routing | `engineering-workflow-router` |
| Planning | `requirements-clarification`, `specification-authoring`, `work-item-planning`, `issue-triage`, `test-planning`, `risk-assessment` |
| Design | `software-design`, `design-review-lightweight`, `design-review-comprehensive` |
| Review orchestration | `code-review-fast`, `review-suite`, `independent-multi-model-review`, `implementation-review` |
| Specialized review | `review-spec-compliance`, `review-silent-failures`, `review-test-quality`, `review-security`, `review-performance-concurrency`, `review-type-interface`, `review-simplification` |
| Execution | `test-driven-development`, `systematic-debugging`, `root-cause-analysis`, `verification-before-completion`, `pr-description`, `pr-follow-through` |

## Runtime-specific packages and tools

- `.codex-plugin/plugin.json`: current Codex plugin package metadata; packaged, not live-tested.
- `adapters/ollama_review.py`: real Ollama HTTP execution adapter with local-host default and an
  explicit remote-host authorization flag.
- `tools/skillsctl.py`: preview, install, status, rollback, and uninstall with hashes and backups.
- `tools/update_platform.py`: validated package fast-forward/install refresh plus isolated upstream
  source staging and update reports.
- `tools/route_task.py`: deterministic low-overhead workflow selection.
- `tools/reconcile_reviews.py`: evidence gate, deduplication, and independent-review aggregation.
- `integrations/azure-devops-mcp/`: inactive official remote-server templates.

## Portable package boundaries

- Installation changes only the selected skill destination and the updater's own state/cache.
- Copilot, Codex, model, authentication, MCP, and provider settings are not changed.
- Codex plugin activation, live Ollama model use, Azure DevOps authentication, and hosted
  multi-provider review require separate runtime-specific setup and authorization.

## Upgrade and rollback

The installer records each deployment as a transaction. Managed upgrades are recognized by hash.
Unmanaged conflicts require `--replace`; post-install local edits block rollback/uninstall unless an
explicit `--force` is used. See [deployment](deployment.md).

## Recommended next improvements

1. Validate the Codex plugin in an available Codex runtime.
2. Run the Ollama adapter against an installed local Qwen model using only a public fixture first.
3. Configure the Azure DevOps remote read-only template after identity and project scope approval.
4. Add runtime-specific adapter packages only when they provide real execution capability rather
   than duplicate instruction files.
