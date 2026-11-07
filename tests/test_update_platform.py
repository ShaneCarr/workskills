from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPDATER = ROOT / "tools" / "update_platform.py"


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    result = run(["git", *args], cwd)
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return result


def bare_git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return git(repo.parent, "-c", "safe.bareRepository=all", "--git-dir", str(repo), *args)


def write_package(repo: Path, version: str, validation_passes: bool = True) -> None:
    (repo / "tools").mkdir(exist_ok=True)
    (repo / "VERSION").write_text(version + "\n", encoding="utf-8")
    (repo / "validate.py").write_text(
        "raise SystemExit(0)\n" if validation_passes else "raise SystemExit(1)\n",
        encoding="utf-8",
    )
    (repo / "tools" / "skillsctl.py").write_text(
        """
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--target")
parser.add_argument("--state-dir")
parser.add_argument("command")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
state = Path(args.state_dir)
state.mkdir(parents=True, exist_ok=True)
(state / "installed.txt").write_text((root / "VERSION").read_text(), encoding="utf-8")
""".lstrip(),
        encoding="utf-8",
    )
    (repo / "updates.json").write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "platform": {
                    "remote": "origin",
                    "ref": "@current",
                    "validation": [[sys.executable, "validate.py"]],
                },
                "upstreams": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )


class UpdatePlatformTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def create_package_repositories(self) -> tuple[Path, Path, Path]:
        remote = self.root / "package-remote.git"
        seed = self.root / "package-seed"
        work = self.root / "package-work"
        git(self.root, "init", "--bare", str(remote))
        git(self.root, "init", "-b", "main", str(seed))
        git(seed, "config", "user.name", "Test User")
        git(seed, "config", "user.email", "test@example.com")
        write_package(seed, "v1")
        git(seed, "add", ".")
        git(seed, "commit", "-m", "v1")
        git(seed, "remote", "add", "origin", str(remote))
        git(seed, "push", "-u", "origin", "main")
        bare_git(remote, "symbolic-ref", "HEAD", "refs/heads/main")
        git(self.root, "clone", str(remote), str(work))
        return remote, seed, work

    def run_package_update(self, work: Path, state: Path) -> subprocess.CompletedProcess:
        return run(
            [
                sys.executable,
                str(UPDATER),
                "package",
                "--root",
                str(work),
                "--state-dir",
                str(state),
            ],
            self.root,
        )

    def test_noop_package_update_refreshes_installation(self) -> None:
        _, _, work = self.create_package_repositories()
        state = self.root / "state"
        result = self.run_package_update(work, state)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "current")
        self.assertEqual((state / "installed.txt").read_text(encoding="utf-8"), "v1\n")

    def test_dirty_package_update_stops_before_installation(self) -> None:
        _, _, work = self.create_package_repositories()
        state = self.root / "state"
        (work / "dirty.txt").write_text("local edit\n", encoding="utf-8")
        result = self.run_package_update(work, state)
        self.assertEqual(result.returncode, 2)
        self.assertIn("uncommitted changes", result.stderr)
        self.assertFalse((state / "installed.txt").exists())

    def test_diverged_package_update_stops(self) -> None:
        _, seed, work = self.create_package_repositories()
        git(work, "config", "user.name", "Test User")
        git(work, "config", "user.email", "test@example.com")
        (work / "local.txt").write_text("local\n", encoding="utf-8")
        git(work, "add", ".")
        git(work, "commit", "-m", "local")
        (seed / "remote.txt").write_text("remote\n", encoding="utf-8")
        git(seed, "add", ".")
        git(seed, "commit", "-m", "remote")
        git(seed, "push")
        result = self.run_package_update(work, self.root / "state")
        self.assertEqual(result.returncode, 2)
        self.assertIn("diverged", result.stderr)

    def test_failed_validation_preserves_head_and_installed_content(self) -> None:
        _, seed, work = self.create_package_repositories()
        state = self.root / "state"
        self.assertEqual(self.run_package_update(work, state).returncode, 0)
        old_head = git(work, "rev-parse", "HEAD").stdout.strip()

        write_package(seed, "v2", validation_passes=False)
        candidate_config = json.loads((seed / "updates.json").read_text(encoding="utf-8"))
        candidate_config["platform"]["validation"] = []
        (seed / "updates.json").write_text(
            json.dumps(candidate_config) + "\n",
            encoding="utf-8",
        )
        git(seed, "add", ".")
        git(seed, "commit", "-m", "invalid v2")
        git(seed, "push")

        result = self.run_package_update(work, state)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Validation failed", result.stderr)
        self.assertEqual(git(work, "rev-parse", "HEAD").stdout.strip(), old_head)
        self.assertEqual((state / "installed.txt").read_text(encoding="utf-8"), "v1\n")

    def test_upstream_newer_revision_is_fetched_and_reported(self) -> None:
        remote = self.root / "upstream.git"
        seed = self.root / "upstream-seed"
        config_root = self.root / "config"
        config_root.mkdir()
        git(self.root, "init", "--bare", str(remote))
        git(self.root, "init", "-b", "main", str(seed))
        git(seed, "config", "user.name", "Test User")
        git(seed, "config", "user.email", "test@example.com")
        (seed / "LICENSE").write_text("license v1\n", encoding="utf-8")
        git(seed, "add", ".")
        git(seed, "commit", "-m", "v1")
        pinned = git(seed, "rev-parse", "HEAD").stdout.strip()
        git(seed, "remote", "add", "origin", str(remote))
        git(seed, "push", "-u", "origin", "main")
        bare_git(remote, "symbolic-ref", "HEAD", "refs/heads/main")
        (seed / "SKILL.md").write_text("new skill\n", encoding="utf-8")
        (seed / "LICENSE").write_text("license v2\n", encoding="utf-8")
        git(seed, "add", ".")
        git(seed, "commit", "-m", "v2")
        latest = git(seed, "rev-parse", "HEAD").stdout.strip()
        git(seed, "push")

        (config_root / "updates.json").write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "platform": {"remote": "origin", "ref": "@current", "validation": []},
                    "upstreams": [
                        {
                            "name": "fixture",
                            "url": str(remote),
                            "pinnedCommit": pinned,
                            "license": "Fixture",
                            "kind": "reviewed-source",
                            "adoption": "Fixture only.",
                        }
                    ],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        cache = self.root / "cache"
        report = self.root / "report.json"
        result = run(
            [
                sys.executable,
                str(UPDATER),
                "upstreams",
                "--root",
                str(config_root),
                "--cache-dir",
                str(cache),
                "--report",
                str(report),
            ],
            self.root,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        source = json.loads(report.read_text(encoding="utf-8"))["sources"][0]
        self.assertEqual(source["status"], "newer-revision-available")
        self.assertEqual(source["relationToPin"], "descendant")
        self.assertEqual(source["stagedCommit"], latest)
        self.assertIn("LICENSE", source["licenseFilesChanged"])
        self.assertFalse(source["automaticAdoption"])


if __name__ == "__main__":
    unittest.main()
