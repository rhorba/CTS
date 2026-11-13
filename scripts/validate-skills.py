#!/usr/bin/env python3
"""Validate the CTS plugin: manifests, required skills, frontmatter, and doc counts."""

import json
import re
import sys
from pathlib import Path

PLUGIN_DIR = Path("claude-team-skills")
MARKETPLACE = Path(".claude-plugin/marketplace.json")

REQUIRED_SKILLS = [
    "orchestrator",
    "project-manager",
    "scrum-master",
    "system-designer",
    "software-architect",
    "tech-lead",
    "security-engineer",
    "dba",
    "ux-designer",
    "ui-designer",
    "motion-designer",
    "design-loop",
    "backend-dev",
    "frontend-dev",
    "tester",
    "test-architect",
    "deployment",
    "devops-devsecops",
    "creative-intelligence",
    "digital-marketer",
    "copywriter",
    "content-marketer",
    "project-monitor",
]

REQUIRED_AGENTS = ["implementer", "spec-reviewer", "quality-reviewer"]

# Paths relative to the plugin directory.
REQUIRED_PLUGIN_FILES = ["INSTALL.md", "QUICKSTART.md", "templates/CLAUDE.md", "templates/AGENTS.md"]

# Docs whose "N specialists" / "all N" claims must match the real skill count.
COUNTED_DOCS = [
    Path("README.md"),
    PLUGIN_DIR / "INSTALL.md",
    PLUGIN_DIR / "QUICKSTART.md",
    PLUGIN_DIR / "templates/CLAUDE.md",
]
COUNT_PATTERN = re.compile(r"\b(?:all|All)\s+(\d+)\b(?!\s+(?:CTS\s+)?phases)|\b(\d+)\s+(?:AI\s+)?[Ss]pecialists\b")


def parse_frontmatter(content, path, errors):
    if not content.startswith("---"):
        errors.append(f"{path}: Missing YAML frontmatter (file must start with ---)")
        return {}
    match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    if not match:
        errors.append(f"{path}: Malformed frontmatter (no closing ---)")
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            fields[key.strip()] = val.strip()
    return fields


def validate_skill(skills_dir, skill_name, errors):
    skill_path = skills_dir / skill_name / "SKILL.md"
    if not skill_path.exists():
        errors.append(f"Missing required skill file: {skill_path}")
        return

    content = skill_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content, skill_path, errors)
    if not fm:
        return

    if "name" not in fm:
        errors.append(f"{skill_path}: Missing 'name:' in frontmatter")
    elif fm["name"] != skill_name:
        errors.append(f"{skill_path}: name '{fm['name']}' does not match folder '{skill_name}'")
    if "description" not in fm:
        errors.append(f"{skill_path}: Missing 'description:' in frontmatter")

    closing = content.index("---", 3) + 3
    body = content[closing:].strip()
    if len(body) < 100:
        errors.append(f"{skill_path}: Skill body too short (< 100 chars)")


def validate_agents(plugin_dir, required, errors):
    agents_dir = plugin_dir / "agents"
    for agent in required:
        path = agents_dir / f"{agent}.md"
        if not path.exists():
            errors.append(f"Missing required agent file: {path}")
            continue
        fm = parse_frontmatter(path.read_text(encoding="utf-8"), path, errors)
        if not fm:
            continue
        if fm.get("name") != agent:
            errors.append(f"{path}: name '{fm.get('name')}' does not match file '{agent}.md'")
        if not fm.get("description"):
            errors.append(f"{path}: Missing 'description:' in frontmatter")


def validate_unlisted_skills(skills_dir, required, errors):
    """A skill folder that exists but is not in REQUIRED_SKILLS is a forgotten registration."""
    for child in sorted(skills_dir.iterdir()):
        if child.is_dir() and child.name not in required:
            errors.append(f"{child}: skill folder is not listed in REQUIRED_SKILLS")


def validate_plugin_files(plugin_dir, required_files, errors):
    for filename in required_files:
        path = plugin_dir / filename
        if not path.exists():
            errors.append(f"Missing required file: {path}")
        elif len(path.read_text(encoding="utf-8").strip()) < 50:
            errors.append(f"{path}: File appears empty or too short")
    if (plugin_dir / "CLAUDE.md").exists():
        errors.append(
            f"{plugin_dir / 'CLAUDE.md'}: a CLAUDE.md at the plugin root is not loaded; "
            "keep it in templates/"
        )


def load_json(path, errors):
    if not path.exists():
        errors.append(f"Missing manifest: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON ({exc})")
        return None


def validate_manifests(plugin_dir, marketplace_path, errors):
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    manifest = load_json(manifest_path, errors)
    marketplace = load_json(marketplace_path, errors)
    if manifest is None or marketplace is None:
        return

    for field in ("name", "version", "description"):
        if not manifest.get(field):
            errors.append(f"{manifest_path}: missing '{field}'")

    for field in ("name", "owner", "plugins"):
        if not marketplace.get(field):
            errors.append(f"{marketplace_path}: missing '{field}'")

    entries = marketplace.get("plugins") or []
    names = [e.get("name") for e in entries]
    if manifest.get("name") and manifest["name"] not in names:
        errors.append(
            f"{marketplace_path}: no plugin entry named '{manifest['name']}' "
            "(entry name must equal the plugin.json name)"
        )


def validate_doc_counts(docs, expected, errors):
    for doc in docs:
        if not doc.exists():
            continue
        for lineno, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            for match in COUNT_PATTERN.finditer(line):
                found = int(match.group(1) or match.group(2))
                if found != expected:
                    errors.append(
                        f"{doc}:{lineno}: says {found} but there are {expected} specialists"
                    )


def validate_reference_dirs(skills_dir, required, warnings):
    for skill_name in required:
        ref_dir = skills_dir / skill_name / "references"
        if ref_dir.exists() and not list(ref_dir.glob("*.md")):
            warnings.append(f"{ref_dir}: references/ dir exists but contains no .md files")


def run(plugin_dir=PLUGIN_DIR, marketplace=MARKETPLACE, docs=None):
    """Run every check. Returns (errors, warnings)."""
    errors, warnings = [], []
    skills_dir = plugin_dir / "skills"
    if not skills_dir.exists():
        return [f"Skills directory not found: {skills_dir} (run from repo root)"], warnings

    validate_manifests(plugin_dir, marketplace, errors)
    validate_plugin_files(plugin_dir, REQUIRED_PLUGIN_FILES, errors)
    validate_agents(plugin_dir, REQUIRED_AGENTS, errors)
    validate_reference_dirs(skills_dir, REQUIRED_SKILLS, warnings)
    validate_unlisted_skills(skills_dir, REQUIRED_SKILLS, errors)
    for skill in REQUIRED_SKILLS:
        validate_skill(skills_dir, skill, errors)
    validate_doc_counts(COUNTED_DOCS if docs is None else docs, len(REQUIRED_SKILLS), errors)
    return errors, warnings


def main():
    errors, warnings = run()

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  WARN  {w}")

    if errors:
        print("\nVALIDATION FAILED:")
        for e in errors:
            print(f"  FAIL  {e}")
        return 1

    print(f"PASS  All {len(REQUIRED_SKILLS)} skills validated")
    print("PASS  Plugin and marketplace manifests")
    print(f"PASS  Agents: {', '.join(REQUIRED_AGENTS)}")
    print(f"PASS  Required plugin files: {', '.join(REQUIRED_PLUGIN_FILES)}")
    print("PASS  Specialist counts in docs")
    if warnings:
        print(f"WARN  {len(warnings)} warning(s) above")
    print("CI: green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
