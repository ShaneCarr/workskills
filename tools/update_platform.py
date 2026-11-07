#!/usr/bin/env python3
"""Safely update the curated package or stage reviewed upstream revisions."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_NAME = "updates.json"
DEFAULT_CACHE = Path.home() / ".engineering-skills-platform" / "upstreams"
SOURCE_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class UpdateError(RuntimeError):
    pass


def run(
    command: list[str],
    *,
    cwd: Path,
    check: bool = True,
    capture: bool = True,
) -> subprocess.CompletedProcess:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=capture,
        text=True,
    )
    if check and result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise UpdateError(f"{' '.join(command)} failed: {detail}")
    return result


def load_config(root: Path) -> dict:
    path = root / CONFIG_NAME
    if not path.is_file():
        raise UpdateError(f"Missing update configuration: {path}")
    config = json.loads(path.read_text(encoding="utf-8"))
    if config.get("schemaVersion") != 1:
        raise UpdateError("Unsupported update configuration schema.")
    return config


def git_output(root: Path, *args: str) -> str:
    return run(["git", *args], cwd=root).stdout.strip()


def bare_git(cache: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return run(
        ["git", "-c", "safe.bareRepository=all", *args],
        cwd=cache,
        check=check,
    )


def bare_git_output(cache: Path, *args: str) -> str:
    return bare_git(cache, *args).stdout.strip()


def ensure_clean_repo(root: Path) -> None:
    if git_output(root, "status", "--porcelain"):
        raise UpdateError("Package repository has uncommitted changes; update stopped.")


def current_branch(root: Path) -> str:
    branch = git_output(root, "branch", "--show-current")
    if not branch:
        raise UpdateError("Package repository is detached; update stopped.")
    return branch


def run_validations(staged_root: Path, commands: list[list[str]]) -> None:
    for command in commands:
        if not command or not all(isinstance(part, str) and part for part in command):
            raise UpdateError("Invalid validation command in update configuration.")
        resolved = [sys.executable if part == "{python}" else part for part in command]
        result = run(resolved, cwd=staged_root, check=False)
        if result.returncode:
            output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
            raise UpdateError(f"Validation failed: {' '.join(resolved)}\n{output}")


def refresh_install(root: Path, args: argparse.Namespace) -> None:
    command = [
        sys.executable,
        str(root / "tools" / "skillsctl.py"),
        "--target",
        args.target,
        "--state-dir",
        args.state_dir,
        "install",
    ]
    result = run(command, cwd=root, check=False, capture=False)
    if result.returncode:
        raise UpdateError("Validated package updated, but managed installation refresh failed.")


def update_package(root: Path, args: argparse.Namespace) -> dict:
    config = load_config(root)["platform"]
    ensure_clean_repo(root)
    branch = current_branch(root)
    remote = config["remote"]
    configured_ref = config["ref"]
    ref = branch if configured_ref == "@current" else configured_ref

    run(["git", "fetch", "--no-tags", remote, ref], cwd=root)
    remote_sha = git_output(root, "rev-parse", "FETCH_HEAD")
    local_sha = git_output(root, "rev-parse", "HEAD")

    if local_sha == remote_sha:
        refresh_install(root, args)
        return {"status": "current", "commit": local_sha, "ref": ref}

    ancestor = run(
        ["git", "merge-base", "--is-ancestor", local_sha, remote_sha],
        cwd=root,
        check=False,
    )
    if ancestor.returncode:
        raise UpdateError("Local package history diverged from the reviewed remote ref.")

    staging_parent = Path(tempfile.mkdtemp(prefix="engineering-skills-update-"))
    staged_root = staging_parent / "package"
    try:
        run(["git", "worktree", "add", "--detach", str(staged_root), remote_sha], cwd=root)
        run_validations(staged_root, config["validation"])
        run(["git", "merge", "--ff-only", remote_sha], cwd=root)
    finally:
        run(["git", "worktree", "remove", "--force", str(staged_root)], cwd=root, check=False)
        shutil.rmtree(staging_parent, ignore_errors=True)

    refresh_install(root, args)
    return {"status": "updated", "from": local_sha, "to": remote_sha, "ref": ref}


def ensure_bare_cache(cache: Path, source: dict) -> None:
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "init", "--bare", str(cache)], cwd=cache.parent)
        bare_git(cache, "remote", "add", "origin", source["url"])
        return
    if not (cache / "HEAD").exists():
        raise UpdateError(f"Upstream cache is not a bare Git repository: {cache}")
    existing = bare_git_output(cache, "remote", "get-url", "origin")
    if existing != source["url"]:
        raise UpdateError(f"Upstream cache URL mismatch for {source['name']}.")


def stage_source(cache_root: Path, source: dict) -> dict:
    if not SOURCE_NAME.fullmatch(source["name"]):
        raise UpdateError(f"Invalid allowlisted source name: {source['name']!r}")
    cache = cache_root / f"{source['name']}.git"
    ensure_bare_cache(cache, source)
    bare_git(
        cache,
        "fetch",
        "--force",
        "--prune",
        "--no-tags",
        "origin",
        "HEAD:refs/staged/latest",
    )
    latest = bare_git_output(cache, "rev-parse", "refs/staged/latest")
    pinned = source["pinnedCommit"]
    if bare_git(cache, "cat-file", "-e", f"{pinned}^{{commit}}", check=False).returncode:
        bare_git(cache, "fetch", "--no-tags", "origin", pinned)

    if latest == pinned:
        status = "current"
        relation = "same"
    elif not bare_git(cache, "merge-base", "--is-ancestor", pinned, latest, check=False).returncode:
        status = "newer-revision-available"
        relation = "descendant"
    else:
        status = "history-diverged"
        relation = "not-descendant"
    diff_stat = ""
    license_changes: list[str] = []
    if status != "current":
        diff_stat = bare_git_output(cache, "diff", "--stat", "--summary", pinned, latest)
        changed = bare_git_output(cache, "diff", "--name-only", pinned, latest)
        license_changes = [
            path
            for path in changed.splitlines()
            if any(token in Path(path).name.upper() for token in ("LICENSE", "COPYING", "NOTICE"))
        ]
    return {
        "name": source["name"],
        "url": source["url"],
        "kind": source["kind"],
        "license": source["license"],
        "pinnedCommit": pinned,
        "stagedCommit": latest,
        "status": status,
        "relationToPin": relation,
        "licenseFilesChanged": license_changes,
        "diffStat": diff_stat,
        "adoption": source["adoption"],
        "cache": str(cache),
        "automaticAdoption": False,
    }


def stage_upstreams(root: Path, args: argparse.Namespace) -> dict:
    config = load_config(root)
    cache_root = Path(args.cache_dir).expanduser().resolve()
    allowed = {source["name"]: source for source in config["upstreams"]}
    selected = args.source or list(allowed)
    unknown = sorted(set(selected) - set(allowed))
    if unknown:
        raise UpdateError(f"Source is not allowlisted: {', '.join(unknown)}")

    reports = [stage_source(cache_root, allowed[name]) for name in selected]
    report = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "note": (
            "Fetched revisions are staged for review only. They do not update native plugins or "
            "replace the curated portable skills."
        ),
        "sources": reports,
    }
    report_path = Path(args.report).expanduser().resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    package = subparsers.add_parser("package", help="Validate, fast-forward, and refresh this package.")
    package.add_argument("--root", default=str(ROOT))
    package.add_argument("--target", choices=("copilot-user", "repo"), default="copilot-user")
    package.add_argument(
        "--state-dir",
        default=str(Path.home() / ".engineering-skills-platform"),
    )

    upstreams = subparsers.add_parser(
        "upstreams",
        help="Fetch allowlisted upstream revisions into an isolated review cache.",
    )
    upstreams.add_argument("--root", default=str(ROOT))
    upstreams.add_argument("--cache-dir", default=str(DEFAULT_CACHE))
    upstreams.add_argument(
        "--report",
        default=str(DEFAULT_CACHE / "update-report.json"),
    )
    upstreams.add_argument("--source", action="append")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        if args.command == "package":
            result = update_package(root, args)
        else:
            result = stage_upstreams(root, args)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError, UpdateError) as error:
        print(f"Update stopped: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
