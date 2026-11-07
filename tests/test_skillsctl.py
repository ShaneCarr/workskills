from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "skillsctl.py"


def run_tool(destination: Path, state: Path, command: str, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--destination",
            str(destination),
            "--state-dir",
            str(state),
            command,
            *extra,
        ],
        check=False,
        capture_output=True,
        text=True,
    )


class SkillsControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_install_status_rollback_round_trip(self) -> None:
        destination = self.root / "skills"
        state = self.root / "state"

        planned = run_tool(destination, state, "plan")
        self.assertEqual(planned.returncode, 0)
        self.assertIn("add", planned.stdout)

        installed = run_tool(destination, state, "install")
        self.assertEqual(installed.returncode, 0)
        self.assertTrue((destination / "engineering-workflow-router" / "SKILL.md").is_file())

        status = run_tool(destination, state, "status")
        self.assertEqual(status.returncode, 0)
        self.assertIn("Active transactions: 1", status.stdout)

        rolled_back = run_tool(destination, state, "rollback")
        self.assertEqual(rolled_back.returncode, 0)
        self.assertFalse((destination / "engineering-workflow-router").exists())

    def test_install_preserves_and_restores_existing_skill(self) -> None:
        destination = self.root / "skills"
        state = self.root / "state"
        existing = destination / "engineering-workflow-router"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("user content\n", encoding="utf-8")

        protected = run_tool(destination, state, "install")
        self.assertEqual(protected.returncode, 2)
        self.assertIn("protect unmanaged existing content", protected.stderr)
        self.assertEqual(
            run_tool(destination, state, "install", "--replace").returncode,
            0,
        )
        self.assertNotIn("user content", (existing / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual(run_tool(destination, state, "uninstall").returncode, 0)
        self.assertEqual((existing / "SKILL.md").read_text(encoding="utf-8"), "user content\n")

    def test_uninstall_refuses_modified_installed_content(self) -> None:
        destination = self.root / "skills"
        state = self.root / "state"
        self.assertEqual(run_tool(destination, state, "install").returncode, 0)
        skill = destination / "engineering-workflow-router" / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\nlocal edit\n", encoding="utf-8")

        result = run_tool(destination, state, "uninstall")
        self.assertEqual(result.returncode, 2)
        self.assertIn("modified after installation", result.stderr)
        self.assertTrue(skill.exists())

    def test_state_contains_no_package_file_contents(self) -> None:
        destination = self.root / "skills"
        state = self.root / "state"
        self.assertEqual(run_tool(destination, state, "install").returncode, 0)
        data = json.loads((state / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schemaVersion"], 1)
        self.assertTrue(data["transactions"][0]["entries"])


if __name__ == "__main__":
    unittest.main()
