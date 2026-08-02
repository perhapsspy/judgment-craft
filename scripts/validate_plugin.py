#!/usr/bin/env python3
"""Validate the canonical Judgment Craft plugin package."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


EXPECTED_SKILLS = {
    "judgment-craft",
    "judgment-repair",
}
REQUIRED_AGENT_FIELDS = ("display_name", "short_description", "default_prompt")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$")
RELEASE_TAG_RE = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
LOCAL_MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
IGNORED_LINK_PREFIXES = ("http://", "https://", "mailto:", "#")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-tag", help="Release tag to compare with the manifest version.")
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[1]
    validator = Validator(repo_root)
    validator.run(args.release_tag)
    return validator.report()


class Validator:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.plugin_root = repo_root / "plugins" / "judgment-craft"
        self.manifest_path = self.plugin_root / ".codex-plugin" / "plugin.json"
        self.errors: list[str] = []
        self.manifest: dict[str, object] = {}

    def run(self, release_tag: str | None) -> None:
        self._load_manifest()
        self._validate_manifest()
        self._validate_skills()
        self._validate_markdown_links()
        self._validate_changelogs()
        self._validate_release_tag(release_tag)
        self._validate_no_plugin_symlinks()

    def report(self) -> int:
        if not self.errors:
            print("Validation passed.")
            return 0
        for error in self.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    def _add(self, message: str) -> None:
        self.errors.append(message)

    def _load_manifest(self) -> None:
        if not self.manifest_path.is_file():
            self._add("manifest missing: plugins/judgment-craft/.codex-plugin/plugin.json")
            return
        try:
            data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            self._add(f"manifest JSON invalid: {exc}")
            return
        if not isinstance(data, dict):
            self._add("manifest root must be an object")
            return
        self.manifest = data

    def _validate_manifest(self) -> None:
        manifest = self.manifest
        if not manifest:
            return

        if manifest.get("name") != "judgment-craft":
            self._add("manifest name must be exactly 'judgment-craft'")

        version = manifest.get("version")
        if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
            self._add("manifest version must be strict SemVer without build metadata")

        description = manifest.get("description")
        if not isinstance(description, str) or not description.strip():
            self._add("manifest description must be a nonempty string")

        if manifest.get("skills") != "./skills/":
            self._add("manifest skills must be exactly './skills/'")

        if manifest.get("license") != "MIT":
            self._add("manifest license must be MIT")

        repository = manifest.get("repository")
        if not isinstance(repository, str) or not repository.startswith("https://"):
            self._add("manifest repository must be an https URL")

        for forbidden in ("hooks", "apps", "mcpServers"):
            if forbidden in manifest:
                self._add(f"manifest must not define {forbidden}")

        skills_path = manifest.get("skills")
        if isinstance(skills_path, str):
            resolved = (self.plugin_root / skills_path).resolve()
            try:
                resolved.relative_to(self.plugin_root.resolve())
            except ValueError:
                self._add("manifest skills path escapes plugin root")
            if not resolved.is_dir():
                self._add("manifest skills path does not exist")

        interface = manifest.get("interface")
        if not isinstance(interface, dict):
            self._add("manifest interface must be an object")
            return

        for field in ("displayName", "shortDescription", "developerName", "category"):
            value = interface.get(field)
            if not isinstance(value, str) or not value.strip():
                self._add(f"manifest interface.{field} must be a nonempty string")

        prompts = interface.get("defaultPrompt")
        if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
            self._add("manifest interface.defaultPrompt must contain 1 to 3 strings")
            prompt_texts: list[str] = []
        else:
            prompt_texts = []
            for idx, prompt in enumerate(prompts, start=1):
                if not isinstance(prompt, str) or not prompt.strip():
                    self._add(f"manifest interface.defaultPrompt item {idx} must be a nonempty string")
                elif "$" not in prompt:
                    self._add(f"manifest interface.defaultPrompt item {idx} must reference a skill token")
                if isinstance(prompt, str):
                    prompt_texts.append(prompt)

        combined = "\n".join(prompt_texts)
        for skill in sorted(EXPECTED_SKILLS):
            token = f"${skill}"
            if not has_skill_token(combined, skill):
                self._add(f"manifest interface.defaultPrompt must reference {token}")

    def _validate_skills(self) -> None:
        skills_root = self.plugin_root / "skills"
        if not skills_root.is_dir():
            self._add("skills directory missing")
            return

        actual = {path.name for path in skills_root.iterdir() if path.is_dir()}
        missing = sorted(EXPECTED_SKILLS - actual)
        extra = sorted(actual - EXPECTED_SKILLS)
        if missing:
            self._add(f"missing skill directories: {', '.join(missing)}")
        if extra:
            self._add(f"unexpected skill directories: {', '.join(extra)}")

        for skill_name in sorted(EXPECTED_SKILLS):
            skill_dir = skills_root / skill_name
            if not skill_dir.is_dir():
                continue
            self._validate_skill_markdown(skill_dir, skill_name)
            self._validate_agent_metadata(skill_dir, skill_name)

    def _validate_skill_markdown(self, skill_dir: Path, skill_name: str) -> None:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            self._add(f"{skill_name}: SKILL.md missing")
            return
        frontmatter = parse_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
        if frontmatter is None:
            self._add(f"{skill_name}: SKILL.md frontmatter missing")
            return
        if frontmatter.get("name") != skill_name:
            self._add(f"{skill_name}: SKILL.md frontmatter name must match directory")
        description = frontmatter.get("description")
        if not isinstance(description, str) or not description.strip():
            self._add(f"{skill_name}: SKILL.md frontmatter description must be nonempty text")

    def _validate_agent_metadata(self, skill_dir: Path, skill_name: str) -> None:
        agent_path = skill_dir / "agents" / "openai.yaml"
        if not agent_path.is_file():
            self._add(f"{skill_name}: agents/openai.yaml missing")
            return
        data = parse_simple_yaml(agent_path.read_text(encoding="utf-8", errors="replace"))
        interface = data.get("interface")
        if not isinstance(interface, dict):
            self._add(f"{skill_name}: agents/openai.yaml interface missing")
            return
        for field in REQUIRED_AGENT_FIELDS:
            value = interface.get(field)
            if not isinstance(value, str) or not value.strip():
                self._add(f"{skill_name}: agents/openai.yaml interface.{field} missing")
        default_prompt = interface.get("default_prompt")
        token = f"${skill_name}"
        if isinstance(default_prompt, str) and not has_skill_token(default_prompt, skill_name):
            self._add(f"{skill_name}: agents/openai.yaml default_prompt must reference {token}")

    def _validate_markdown_links(self) -> None:
        for path in tracked_or_current_markdown_files(self.repo_root):
            text = path.read_text(encoding="utf-8", errors="replace")
            for raw_target in LOCAL_MD_LINK_RE.findall(text):
                target = raw_target.strip()
                if not target or target.startswith(IGNORED_LINK_PREFIXES):
                    continue
                target = target.split("#", 1)[0].strip()
                if not target:
                    continue
                if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                    continue
                if target.startswith("<") and target.endswith(">"):
                    target = target[1:-1]
                target_path = (path.parent / target).resolve()
                try:
                    target_path.relative_to(self.repo_root.resolve())
                except ValueError:
                    self._add(f"{display_path(path, self.repo_root)}: markdown link escapes repo: {raw_target}")
                    continue
                if not target_path.exists():
                    self._add(f"{display_path(path, self.repo_root)}: markdown link target missing: {raw_target}")

    def _validate_changelogs(self) -> None:
        version = self.manifest.get("version")
        if not isinstance(version, str):
            return
        for changelog_name in ("CHANGELOG.md", "CHANGELOG.en.md"):
            path = self.repo_root / changelog_name
            if not path.is_file():
                self._add(f"{changelog_name} missing")
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if not re.search(rf"^##\s+{re.escape(version)}(?:\s+-|\s*$)", text, re.MULTILINE):
                self._add(f"{changelog_name} must contain a heading for version {version}")

    def _validate_release_tag(self, release_tag: str | None) -> None:
        if release_tag is None:
            return
        version = self.manifest.get("version")
        if not isinstance(version, str):
            return
        if "+" in release_tag or not RELEASE_TAG_RE.fullmatch(release_tag):
            self._add("--release-tag must be vX.Y.Z and must not include build metadata")
            return
        if release_tag != f"v{version}":
            self._add(f"--release-tag {release_tag} does not match manifest version {version}")

    def _validate_no_plugin_symlinks(self) -> None:
        if not self.plugin_root.exists():
            return
        for root, dirs, files in os.walk(self.plugin_root):
            for name in [*dirs, *files]:
                path = Path(root) / name
                try:
                    is_link = path.is_symlink()
                except OSError:
                    continue
                if is_link:
                    self._add(f"symlink not allowed under plugin root: {display_path(path, self.repo_root)}")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            return parse_key_values("\n".join(lines[1:index]))
    return None


def parse_simple_yaml(text: str) -> dict[str, object]:
    root: dict[str, object] = {}
    current_map: dict[str, str] | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and line.endswith(":"):
            key = line[:-1].strip()
            current_map = {}
            root[key] = current_map
            continue
        if current_map is not None and line.startswith("  "):
            key, value = split_yaml_pair(line.strip())
            if key:
                current_map[key] = unquote(value)
            continue
        key, value = split_yaml_pair(line)
        if key:
            root[key] = unquote(value)
            current_map = None
    return root


def parse_key_values(text: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw_line in text.splitlines():
        key, value = split_yaml_pair(raw_line.strip())
        if key:
            data[key] = unquote(value)
    return data


def split_yaml_pair(line: str) -> tuple[str, str]:
    if ":" not in line:
        return "", ""
    key, value = line.split(":", 1)
    return key.strip(), value.strip()


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def has_skill_token(text: str, skill_name: str) -> bool:
    token = re.escape(f"${skill_name}")
    return re.search(rf"(?<![\w-]){token}(?![\w-])", text) is not None


def tracked_or_current_markdown_files(repo_root: Path) -> list[Path]:
    files: set[Path] = set()
    try:
        result = subprocess.run(
            ["git", "ls-files", "--", "*.md"],
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        result = None
    if result and result.returncode == 0:
        files.update(repo_root / line for line in result.stdout.splitlines() if line.strip())

    files.update(path for path in repo_root.rglob("*.md") if ".git" not in path.parts)
    return sorted(path for path in files if path.is_file())


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
