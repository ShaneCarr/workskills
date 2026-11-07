# Validation record

## Executed on the development machine

| Check | Result | Evidence level |
| --- | --- | --- |
| Skill metadata and directory validation | 27 skills valid | Static package validation |
| Installer preview | Correctly listed additions without writing | Local runtime |
| Managed skill installation | Packaged skills installed and post-install hashes reported unchanged | Isolated/local filesystem runtime |
| Managed skill upgrade | Changed managed skills identified as upgrades and reinstalled without `--replace` | Isolated/local filesystem runtime |
| Install, status, rollback, and uninstall | Passed in isolated temporary directories | Local runtime |
| Existing skill conflict backup and restore | Passed | Local runtime |
| Modified installed content protection | Uninstall refused deletion as designed | Local runtime |
| Workflow routing scenarios | Six representative scenarios passed | Deterministic local runtime |
| Review finding reconciliation | Deduplication, explicit code-verification gate, and speculative-finding rejection passed | Synthetic reports |
| Ollama HTTP execution adapter | Request/response and model listing passed | Fixture HTTP server |
| Package update no-op | Refreshed the managed install from a current clean synthetic clone | Synthetic Git repository |
| Dirty/diverged update protection | Update stopped before installation | Synthetic Git repositories |
| Candidate validation failure | Preserved the previous Git head and installed content | Synthetic Git repository |
| Upstream update staging | Detected/fetched a newer revision and reported license changes | Synthetic Git repository |
| Python compilation | Passed | Local runtime |
| Git whitespace validation | Passed | Static repository validation |
| Allowlisted upstream staging | All nine reviewed pins matched fetched remote `HEAD` on 2026-11-06 | Live public Git fetch |

Run all repository tests:

```powershell
python -m unittest discover -s tests -v
python tools\validate_skills.py
python -m compileall -q tools adapters tests
git diff --check
```

## Representative workflows

The test suite covers:

1. small bug fix routing;
2. moderately complex feature routing;
3. important design decision routing;
4. work item decomposition routing;
5. standard pull request review routing; and
6. comprehensive independent-review reconciliation.

These are deterministic fixture tests. They prove routing, installation safety, adapter protocol,
and reconciliation behavior; they do not prove the quality of an external model.

## Integration qualification

- **Copilot:** skill installation and runtime loading were exercised during reference validation.
  Newly added skills may require a new session or application reload before they appear in an
  already-running runtime catalog.
- **Ollama:** the real adapter is fixture-tested; no live model quality claim is included.
- **Azure DevOps MCP:** templates are static and inactive; no credentials, permissions, or live
  operations are part of repository validation.
- **Codex:** current plugin packaging is statically validated; runtime activation is not claimed.

## Unsupported or intentionally untested

- Real multi-provider model review was not run because no proprietary code sharing or new paid
  usage was authorized for validation.
- macOS and Linux commands were not executed on this Windows host.
- Azure DevOps read and write operations were not authenticated or executed.
- Skill discovery after a Copilot application reload is not represented by file-presence tests.
