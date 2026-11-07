# Updating the platform and tracked sources

There are two deliberately separate update operations.

## Update this curated package and local installation

From a clean clone on the published branch or tag:

```powershell
python tools\update_platform.py package
```

On macOS or Linux:

```bash
python3 tools/update_platform.py package
```

This command:

1. refuses a dirty, detached, or diverged package repository;
2. fetches the configured reviewed Git ref (`origin` and the current branch by default);
3. checks out the candidate in an isolated worktree;
4. runs the candidate's tests, skill validation, and Python compilation;
5. fast-forwards only after validation succeeds; and
6. refreshes the managed Copilot skill installation through `skillsctl.py`.

The existing installation remains intact when candidate validation fails. Installation conflicts,
local post-install edits, backups, and rollback history retain the protections documented in
[deployment](deployment.md).

## Check and stage newer upstream revisions

```powershell
python tools\update_platform.py upstreams
```

This fetches every source allowlisted in `updates.json` into the isolated cache under
`~/.engineering-skills-platform/upstreams` and writes `update-report.json`. Use `--source
superpowers` to check only Superpowers, or `--cache-dir` and `--report` to override those paths.

The report includes the reviewed pin, staged remote commit, source kind, license, changed license
files, history relationship, diff statistics, and the current adoption note. A rewritten or
non-descendant upstream history is reported as `history-diverged`, not as a normal update. A changed
upstream requires human review:

1. inspect the staged diff and license changes;
2. decide whether the curated behavior should change;
3. update original portable skills or runtime packaging deliberately;
4. update the reviewed pin and provenance;
5. rerun validation; and
6. publish a normal reviewed package update.

Fetching is **not installation or adoption**. It does not execute upstream scripts, replace curated
skills, update a native Claude/Codex/Copilot plugin, or assert compatibility. Native plugins must be
updated through their verified runtime-specific mechanism when intentionally installed. This
package updates only its own portable skills and packaged Codex manifest; runtime activation remains
separate.

## Home-machine routine

```powershell
git status --short
python tools\update_platform.py package
python tools\update_platform.py upstreams
```

Run the upstream check when evaluating new source releases; the package update is the routine way
to pull an already reviewed and published platform revision to another machine.
