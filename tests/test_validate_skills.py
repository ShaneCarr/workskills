import json
import unittest
from pathlib import Path

from tools.validate_skills import validate


ROOT = Path(__file__).resolve().parents[1]


class ValidateSkillsTests(unittest.TestCase):
    def test_skill_package_is_valid(self) -> None:
        self.assertEqual(validate(), [])

    def test_platform_manifest_matches_skill_directories(self) -> None:
        manifest = json.loads((ROOT / "platform.json").read_text(encoding="utf-8"))
        directories = sorted(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(manifest["skills"], directories)

    def test_codex_plugin_manifest_points_to_portable_skills(self) -> None:
        plugin = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        platform = json.loads((ROOT / "platform.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["version"], platform["version"])
        self.assertEqual(plugin["skills"], "./skills/")
        self.assertEqual(plugin["license"], "MIT")

    def test_update_allowlist_has_unique_pinned_sources(self) -> None:
        updates = json.loads((ROOT / "updates.json").read_text(encoding="utf-8"))
        sources = updates["upstreams"]
        names = [source["name"] for source in sources]
        self.assertEqual(len(names), len(set(names)))
        self.assertIn("superpowers", names)
        for source in sources:
            self.assertRegex(source["pinnedCommit"], r"^[0-9a-f]{40}$")
            self.assertTrue(source["url"].endswith(".git"))
            self.assertFalse(source.get("automaticAdoption", False))


if __name__ == "__main__":
    unittest.main()
