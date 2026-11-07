# Research and environment record

## Upstream files inspected

| Source | Representative files checked |
| --- | --- |
| Superpowers | `README.md`, `LICENSE`, `package.json`, `skills/brainstorming/SKILL.md`, `writing-plans`, `test-driven-development`, `systematic-debugging`, `requesting-code-review` |
| Matt Pocock skills | `README.md`, `LICENSE`, `package.json`, `skills/engineering/codebase-design/SKILL.md`, `to-spec`, `code-review`, `diagnosing-bugs`, `tdd` |
| Anthropic skills | `README.md`, per-skill licenses, `frontend-design/SKILL.md`, `doc-coauthoring`, `webapp-testing`, `skill-creator` |
| PR Review Toolkit | plugin manifest, README, license, `/review-pr` command, and six agent definitions |
| OpenAI skills/plugins | deprecated skills README, representative goal/GitHub/Playwright/creator/installer skills, current plugin README, manifest specification, sample plugin and marketplace |
| Essential-kit | `README.md`, `LICENSE`, and design/debugging/TDD/spec/review skills compared with upstream Matt Pocock versions |
| Agent Skills | `docs/specification.mdx`, README, and license declarations |
| Azure DevOps MCP | `README.md`, `package.json`, `docs/GETTINGSTARTED.md`, `docs/TOOLSET.md`, tool annotations, domain registration, OAuth/auth source, and current remote-server Microsoft Learn page |

Exact commits and links are in [provenance](provenance.md).

## Reference implementation checks

- Inspected local and remote branch trees and immutable heads before writing.
- Confirmed `main` contains no platform files and preserved two existing skill branches.
- Read the existing portable planning and repeatable feature-delivery skills as prior art without
  modifying their branches.
- Inspected configuration structure by key/name only; no credential values were printed or copied.
- Verified the package with Git, Python, and a GitHub Copilot skill runtime. Other runtimes remain
  explicitly runtime-specific rather than inferred from file presence.

## What was not inspected or changed

- No tokens, PATs, secrets, or credential payloads were read.
- No proprietary repository content was sent to an external model or web service.
- No global model, MCP, authentication, provider, or application setting was changed.
- No upstream installer or arbitrary repository script was executed.
