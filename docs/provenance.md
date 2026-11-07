# Source provenance and selection

Research was performed on 2026-11-06 against immutable commits. The platform's skill text and code
are original MIT-licensed work. No upstream `SKILL.md`, agent prompt, or plugin file is redistributed.
Upstream sources informed capability selection and review structure.

The same reviewed commits are machine-readable in `updates.json`. `update_platform.py upstreams`
can stage newer allowlisted revisions and report source, license, and diff changes without adopting
or installing them.

| Source | Reviewed commit/version | License | Selection |
| --- | --- | --- | --- |
| [obra/superpowers](https://github.com/obra/superpowers/commit/22f0b463e7a5e579904dd6211a520321035526f7) | `22f0b463e7a5e579904dd6211a520321035526f7`, 7.0.2 | MIT | Brainstorming, planning, TDD, systematic debugging, review handoff, and verification concepts |
| [mattpocock/skills](https://github.com/mattpocock/skills/commit/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d) | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`, 1.3.2 | MIT | Modular specification, design, debugging, TDD, triage, and standards/spec review axes |
| [anthropics/skills](https://github.com/anthropics/skills/commit/2c5958ecac7cee2b583967a2c4981d0f4a75c579) | `2c5958ecac7cee2b583967a2c4981d0f4a75c579` | Per-skill; many Apache-2.0 | Format/evaluation examples only; not selected as the core engineering workflow |
| [Anthropic PR Review Toolkit](https://github.com/anthropics/claude-plugins-official/tree/0412be76f50ab4f4f8abff3753efa9269fbbca5b/plugins/pr-review-toolkit) | `0412be76f50ab4f4f8abff3753efa9269fbbca5b`, 1.0.1 | Apache-2.0 | Specialized test, silent-failure, type, correctness, and simplification review perspectives |
| [openai/skills](https://github.com/openai/skills/commit/49f948faa9258a0c61caceaf225e179651397431) | `49f948faa9258a0c61caceaf225e179651397431` | Per-skill | Historical examples only; repository is deprecated |
| [openai/plugins](https://github.com/openai/plugins/commit/d420d13051bffe4543ed39e30fa46b87148e47dd) | `d420d13051bffe4543ed39e30fa46b87148e47dd` | Plugin-specific | Current Codex plugin packaging authority |
| [Essential-kit/skills](https://github.com/Essential-kit/skills/commit/bbe82cd177cdd183e14ebb68a6d437a3af355b9b) | `bbe82cd177cdd183e14ebb68a6d437a3af355b9b` | MIT | Scaling-review idea reviewed; content not adopted because it substantially derives from Matt Pocock and has weaker maintenance |
| [agentskills/agentskills](https://github.com/agentskills/agentskills/commit/83021e2be457a9b6679148719c1f6074f0ad975e) | `83021e2be457a9b6679148719c1f6074f0ad975e` | Apache-2.0 code; CC-BY-4.0 docs | Neutral Agent Skills format and validation rules |
| [microsoft/azure-devops-mcp](https://github.com/microsoft/azure-devops-mcp/commit/7f2a6b9fae78903682f4c6328cab17986f3f1cc5) | `7f2a6b9fae78903682f4c6328cab17986f3f1cc5`, 2.11.0 | MIT | Official Azure DevOps integration and permission-boundary guidance |

## Compatibility conclusions

- Agent Skills are portable instruction packages, but runtime capabilities are not interchangeable.
  Subagents, tool permissions, hooks, plugins, and MCP configuration remain runtime-specific.
- Superpowers and Matt Pocock provide native marketplace/plugin paths for several agents. This
  platform instead uses original, smaller skills to avoid duplicate installation and rigid coupling.
- Anthropic's PR toolkit is a Claude Code command plus six agents, not a set of portable
  `SKILL.md` files.
- Current Codex distribution uses plugins with `.codex-plugin/plugin.json`; this repository includes
  that manifest. The deprecated `openai/skills` install model is not used.
- The neutral Agent Skills specification requires matching lowercase directory/name fields and
  descriptions; all packaged skills are checked locally against those core constraints.

## Official distribution notes

| Source | Current official path |
| --- | --- |
| Superpowers | Runtime-specific marketplace/plugin instructions for Claude Code, Codex, GitHub Copilot, Cursor, Gemini, Qwen, and others; each harness has a distinct installation |
| Matt Pocock skills | Claude, Codex, and GitHub Copilot plugins/marketplaces; `npx skills@latest` for copied editable skills; do not install both forms |
| Anthropic skills | Claude Code marketplace plugins, Claude.ai custom upload, or Claude API skills |
| PR Review Toolkit | `/plugin install pr-review-toolkit@claude-plugins-official` in Claude Code |
| OpenAI skills | Deprecated; use `openai/plugins` and current Codex plugin guidance |
| OpenAI plugins | `.codex-plugin/plugin.json` plus the current personal or repository marketplace |
| Essential-kit | `npx skills add Essential-kit/skills`, requiring Node.js 22.20+; several workflows also require authenticated `gh` |
| Azure DevOps MCP | Hosted remote HTTP server first; local `npx -y @azure-devops/mcp {organization}` requires Node.js 20+ |

## License policy

Because no upstream content is copied, upstream license notices are not bundled as redistributed
source. If a future version imports or modifies upstream files, it must add the applicable license,
copyright, modification, and NOTICE material before publication.
