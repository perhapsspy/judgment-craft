from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidatePluginTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.fixture = Path(self.temp_dir.name) / "repo"
        ignore = shutil.ignore_patterns(".git", "__pycache__", "*.pyc")
        shutil.copytree(REPO_ROOT, self.fixture, ignore=ignore)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.fixture / "scripts" / "validate_plugin.py"), *args],
            cwd=self.fixture,
            text=True,
            capture_output=True,
            check=False,
        )

    def manifest(self) -> dict[str, object]:
        path = self.fixture / "plugins" / "judgment-craft" / ".codex-plugin" / "plugin.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def write_manifest(self, data: dict[str, object]) -> None:
        path = self.fixture / "plugins" / "judgment-craft" / ".codex-plugin" / "plugin.json"
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def test_committed_repository_passes(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validation passed.", result.stdout)

    def test_extra_and_missing_skill_rejected(self) -> None:
        skills = self.fixture / "plugins" / "judgment-craft" / "skills"
        shutil.move(skills / "practical-judgment", skills / "practical-judgment.bak")
        (skills / "extra-skill").mkdir()
        result = self.run_validator()
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing skill directories: practical-judgment", result.stderr)
        self.assertIn("unexpected skill directories: extra-skill, practical-judgment.bak", result.stderr)

    def test_frontmatter_name_mismatch_rejected(self) -> None:
        path = self.fixture / "plugins" / "judgment-craft" / "skills" / "practical-judgment" / "SKILL.md"
        text = path.read_text(encoding="utf-8").replace("name: practical-judgment", "name: wrong-name")
        path.write_text(text, encoding="utf-8")
        result = self.run_validator()
        self.assertEqual(result.returncode, 1)
        self.assertIn("SKILL.md frontmatter name must match directory", result.stderr)

    def test_missing_agent_metadata_rejected(self) -> None:
        path = self.fixture / "plugins" / "judgment-craft" / "skills" / "calibrate-judgment" / "agents" / "openai.yaml"
        path.write_text(
            'interface:\n  display_name: "Calibrate Judgment"\n  default_prompt: "Use $calibrate-judgment."\n',
            encoding="utf-8",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 1)
        self.assertIn("calibrate-judgment: agents/openai.yaml interface.short_description missing", result.stderr)

    def test_starter_prompts_missing_a_skill_rejected(self) -> None:
        data = self.manifest()
        interface = data["interface"]
        assert isinstance(interface, dict)
        interface["defaultPrompt"] = ["Use $practical-judgment.", "Use $calibrate-judgment."]
        self.write_manifest(data)
        result = self.run_validator()
        self.assertEqual(result.returncode, 1)
        self.assertIn("manifest interface.defaultPrompt must reference $friction-distillation", result.stderr)

    def test_invalid_and_mismatched_release_tag_rejected(self) -> None:
        invalid = self.run_validator("--release-tag", "v0.1.0+build")
        self.assertEqual(invalid.returncode, 1)
        self.assertIn("must not include build metadata", invalid.stderr)

        prerelease = self.run_validator("--release-tag", "v0.1.0-rc.1")
        self.assertEqual(prerelease.returncode, 1)
        self.assertIn("must be vX.Y.Z", prerelease.stderr)

        mismatched = self.run_validator("--release-tag", "v0.1.1")
        self.assertEqual(mismatched.returncode, 1)
        self.assertIn("does not match manifest version 0.1.0", mismatched.stderr)

    def test_broken_and_escaping_relative_markdown_link_rejected(self) -> None:
        readme = self.fixture / "README.md"
        readme.write_text(
            readme.read_text(encoding="utf-8")
            + "\n[broken](docs/MISSING.md)\n[escape](../outside.md)\n",
            encoding="utf-8",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 1)
        self.assertIn("markdown link target missing: docs/MISSING.md", result.stderr)
        self.assertIn("markdown link escapes repo: ../outside.md", result.stderr)

    def test_cli_aggregates_errors_and_exits_1(self) -> None:
        data = self.manifest()
        data["name"] = "wrong"
        data["hooks"] = {}
        self.write_manifest(data)
        result = self.run_validator("--release-tag", "v9.9.9")
        self.assertEqual(result.returncode, 1)
        self.assertIn("manifest name must be exactly 'judgment-craft'", result.stderr)
        self.assertIn("manifest must not define hooks", result.stderr)
        self.assertIn("--release-tag v9.9.9 does not match manifest version 0.1.0", result.stderr)


if __name__ == "__main__":
    unittest.main()
