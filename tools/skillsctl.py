#!/usr/bin/env python3
"""Install and manage the portable engineering skills collection."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "skills"
PLATFORM = json.loads((ROOT / "platform.json").read_text(encoding="utf-8"))
DEFAULT_STATE_DIR = Path.home() / ".engineering-skills-platform"
TARGETS = {
    "copilot-user": Path.home() / ".copilot" / "skills",
    "repo": Path.cwd() / ".github" / "skills",
}


def hash_tree(path: Path) -> str:
    digest = hashlib.sha256()
    if not path.exists():
        return "missing"
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(item.relative_to(path).as_posix().encode())
        digest.update(b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def package_skills() -> list[Path]:
    if not PACKAGE_DIR.is_dir():
        raise SystemExit(f"Package directory is missing: {PACKAGE_DIR}")
    skills = sorted(path for path in PACKAGE_DIR.iterdir() if (path / "SKILL.md").is_file())
    if not skills:
        raise SystemExit(f"No skills found in {PACKAGE_DIR}")
    return skills


def resolve_destination(args: argparse.Namespace) -> Path:
    if args.destination:
        return Path(args.destination).expanduser().resolve()
    return TARGETS[args.target].expanduser().resolve()


def state_path(state_dir: Path) -> Path:
    return state_dir / "state.json"


def load_state(state_dir: Path) -> dict:
    path = state_path(state_dir)
    if not path.exists():
        return {"schemaVersion": 1, "transactions": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state_dir: Path, state: dict) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_path(state_dir)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def managed_hashes(state: dict, destination: Path) -> dict[str, str]:
    hashes = {}
    for transaction in active_transactions(state, destination):
        for entry in transaction["entries"]:
            hashes[entry["skill"]] = entry["installedHash"]
    return hashes


def inventory(destination: Path, state: dict | None = None) -> list[dict[str, str]]:
    managed = managed_hashes(state, destination) if state else {}
    result = []
    for source in package_skills():
        target = destination / source.name
        source_hash = hash_tree(source)
        target_hash = hash_tree(target)
        if target_hash == "missing":
            action = "add"
        elif target_hash == source_hash:
            action = "unchanged"
        elif managed.get(source.name) == target_hash:
            action = "upgrade"
        else:
            action = "replace-with-backup"
        result.append(
            {
                "skill": source.name,
                "action": action,
                "sourceHash": source_hash,
                "targetHash": target_hash,
            }
        )
    return result


def print_inventory(destination: Path, rows: list[dict[str, str]]) -> None:
    print(f"Destination: {destination}")
    for row in rows:
        print(f"{row['action']:20} {row['skill']}")


def copy_atomic(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{target.name}-", dir=target.parent))
    try:
        shutil.copytree(source, temporary / target.name)
        if target.exists():
            shutil.rmtree(target)
        os.replace(temporary / target.name, target)
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def command_plan(args: argparse.Namespace) -> int:
    destination = resolve_destination(args)
    state_dir = Path(args.state_dir).expanduser().resolve()
    print_inventory(destination, inventory(destination, load_state(state_dir)))
    return 0


def command_install(args: argparse.Namespace) -> int:
    destination = resolve_destination(args)
    state_dir = Path(args.state_dir).expanduser().resolve()
    state = load_state(state_dir)
    rows = inventory(destination, state)
    changed = [row for row in rows if row["action"] != "unchanged"]
    print_inventory(destination, rows)
    if not changed:
        print("No changes required.")
        return 0
    conflicts = [row["skill"] for row in changed if row["action"] == "replace-with-backup"]
    if conflicts and not args.replace:
        print("Install stopped to protect unmanaged existing content.", file=sys.stderr)
        print("Preview the backup replacements below, then rerun with --replace:", file=sys.stderr)
        for skill in conflicts:
            print(f"- {skill}", file=sys.stderr)
        return 2

    transaction_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_root = state_dir / "backups" / transaction_id
    entries = []
    try:
        for row in changed:
            source = PACKAGE_DIR / row["skill"]
            target = destination / row["skill"]
            backup = None
            if target.exists():
                backup = backup_root / row["skill"]
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(target, backup)
            entry = {
                **row,
                "destination": str(target),
                "backup": str(backup) if backup else None,
                "installedHash": "pending",
            }
            entries.append(entry)
            copy_atomic(source, target)
            entry["installedHash"] = hash_tree(target)
    except Exception:
        revert_transaction({"entries": entries}, allow_modified=True)
        raise

    state["transactions"].append(
        {
            "id": transaction_id,
            "packageVersion": PLATFORM["version"],
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "destination": str(destination),
            "entries": entries,
            "active": True,
        }
    )
    save_state(state_dir, state)
    print(f"Installed {len(entries)} skill(s). Transaction: {transaction_id}")
    return 0


def active_transactions(state: dict, destination: Path) -> list[dict]:
    return [
        tx
        for tx in state["transactions"]
        if tx.get("active") and Path(tx["destination"]).resolve() == destination
    ]


def revert_transaction(transaction: dict, *, allow_modified: bool) -> list[str]:
    entries = list(reversed(transaction["entries"]))
    conflicts = []
    for entry in entries:
        target = Path(entry["destination"])
        current_hash = hash_tree(target)
        if current_hash not in ("missing", entry["installedHash"]) and not allow_modified:
            conflicts.append(f"{target}: modified after installation")
    if conflicts:
        return conflicts
    for entry in entries:
        target = Path(entry["destination"])
        backup = Path(entry["backup"]) if entry["backup"] else None
        if target.exists():
            shutil.rmtree(target)
        if backup and backup.exists():
            shutil.copytree(backup, target)
    return conflicts


def command_rollback(args: argparse.Namespace) -> int:
    destination = resolve_destination(args)
    state_dir = Path(args.state_dir).expanduser().resolve()
    state = load_state(state_dir)
    candidates = active_transactions(state, destination)
    if args.transaction:
        candidates = [tx for tx in candidates if tx["id"] == args.transaction]
    if not candidates:
        print("No active matching transaction.")
        return 0
    transaction = candidates[-1]
    conflicts = revert_transaction(transaction, allow_modified=args.force)
    if conflicts:
        print("Rollback stopped to protect modified content:", file=sys.stderr)
        for conflict in conflicts:
            print(f"- {conflict}", file=sys.stderr)
        return 2
    transaction["active"] = False
    transaction["revertedAt"] = datetime.now(timezone.utc).isoformat()
    save_state(state_dir, state)
    print(f"Rolled back transaction {transaction['id']}.")
    return 0


def command_uninstall(args: argparse.Namespace) -> int:
    destination = resolve_destination(args)
    state_dir = Path(args.state_dir).expanduser().resolve()
    state = load_state(state_dir)
    transactions = active_transactions(state, destination)
    if not transactions:
        print("No active installation recorded.")
        return 0
    for transaction in reversed(transactions):
        conflicts = revert_transaction(transaction, allow_modified=args.force)
        if conflicts:
            print("Uninstall stopped to protect modified content:", file=sys.stderr)
            for conflict in conflicts:
                print(f"- {conflict}", file=sys.stderr)
            return 2
        transaction["active"] = False
        transaction["revertedAt"] = datetime.now(timezone.utc).isoformat()
        save_state(state_dir, state)
    print(f"Uninstalled {len(transactions)} transaction(s).")
    return 0


def command_status(args: argparse.Namespace) -> int:
    destination = resolve_destination(args)
    state_dir = Path(args.state_dir).expanduser().resolve()
    state = load_state(state_dir)
    print_inventory(destination, inventory(destination, state))
    transactions = active_transactions(state, destination)
    print(f"Active transactions: {len(transactions)}")
    for transaction in transactions:
        print(f"- {transaction['id']} ({transaction['createdAt']})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=TARGETS, default="copilot-user")
    parser.add_argument("--destination", help="Override the target directory.")
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR))
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("plan").set_defaults(handler=command_plan)
    install = subparsers.add_parser("install")
    install.add_argument(
        "--replace",
        action="store_true",
        help="Replace unmanaged conflicting skill directories after backing them up.",
    )
    install.set_defaults(handler=command_install)
    subparsers.add_parser("status").set_defaults(handler=command_status)
    rollback = subparsers.add_parser("rollback")
    rollback.add_argument("--transaction")
    rollback.add_argument("--force", action="store_true")
    rollback.set_defaults(handler=command_rollback)
    uninstall = subparsers.add_parser("uninstall")
    uninstall.add_argument("--force", action="store_true")
    uninstall.set_defaults(handler=command_uninstall)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
