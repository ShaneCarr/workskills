# Deployment, upgrade, and rollback

The installer copies only directories under `skills/`. Runtime adapters and documentation stay in
the repository. State and backups are kept outside the skill destination in
`~/.engineering-skills-platform` by default.

## Deploy on another machine

```powershell
gh repo clone <owner>/<repository>
Set-Location <repository>
git switch <published-branch-or-tag>
python tools\skillsctl.py --target copilot-user plan
python tools\skillsctl.py --target copilot-user install
```

On macOS or Linux:

```bash
gh repo clone <owner>/<repository>
cd <repository>
git switch <published-branch-or-tag>
python3 tools/skillsctl.py --target copilot-user plan
python3 tools/skillsctl.py --target copilot-user install
```

`plan` reports `add`, `unchanged`, `upgrade`, or `replace-with-backup` for every skill. An unmanaged
conflict stops installation. After reviewing it, rerun `install --replace` to snapshot and replace
that directory. Recorded managed upgrades do not need this flag.

## Upgrade

```powershell
python tools\update_platform.py package
```

The updater stages and validates the remote candidate before fast-forwarding and refreshing the
managed installation. Every changed installation creates a transaction. No-change installs do not
create one. See [updating](updating.md) for upstream source checks.

## Roll back or uninstall

```powershell
python tools\skillsctl.py --target copilot-user status
python tools\skillsctl.py --target copilot-user rollback
python tools\skillsctl.py --target copilot-user uninstall
```

Rollback reverts the latest active transaction. Uninstall reverts all active transactions in
reverse order. Both refuse to remove skill content changed after installation. `--force` exists for
an intentional override, but preview and copy local edits first.

## Other destinations

- `--target repo` installs into the current repository's `.github/skills`.
- `--destination <path>` supports another runtime or a test directory.
- Codex uses the packaged `.codex-plugin/plugin.json` and current plugin/marketplace mechanism,
  rather than an assumed personal skill-copy directory. This was packaged but not live-installed
  because Codex was unavailable on the development host.

The installer never edits MCP configuration, provider credentials, model selection, or arbitrary
files outside the selected skill directories and its own state directory.

Start a new Copilot session (or reload the application when required by the runtime) after adding a
new skill. `status` proves installed content and hashes; it does not prove that an already-running
session refreshed its skill catalog.
