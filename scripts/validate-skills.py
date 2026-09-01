#!/usr/bin/env python3
"""Validate CTS skill files — checks frontmatter, required skills, and file structure."""

import re
import sys
from pathlib import Path

SKILLS_DIR = Path("claude-team-skills")

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

REQUIRED_ROOT_FILES = ["CLAUDE.md", "QUICKSTART.md", "INSTALL.md"]

errors = []
warnings = []


def parse_frontmatter(content, path):
    if not content.startswith("---"):
        errors.append(f"{path}: Missing YAML frontmatter (file must start with ---)")
        return {}
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        errors.append(f"{path}: Malformed frontmatter (no closing ---)")
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            fields[key.strip()] = val.strip()
    return fields


def validate_skill(skill_name):
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_path.exists():
        errors.append(f"Missing required skill file: {skill_path}")
        return

    content = skill_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content, skill_path)
    if not fm:
        return

    if "name" not in fm:
        errors.append(f"{skill_path}: Missing 'name:' in frontmatter")
    if "description" not in fm:
        errors.append(f"{skill_path}: Missing 'description:' in frontmatter")

    closing = content.index("---", 3) + 3
    body = content[closing:].strip()
    if len(body) < 100:
        errors.append(f"{skill_path}: Skill body too short (< 100 chars)")


def validate_root_files():
    for filename in REQUIRED_ROOT_FILES:
        path = SKILLS_DIR / filename
        if not path.exists():
            errors.append(f"Missing required file: {path}")
        elif len(path.read_text(encoding="utf-8").strip()) < 50:
            errors.append(f"{path}: File appears empty or too short")


def validate_reference_dirs():
    for skill_name in REQUIRED_SKILLS:
        ref_dir = SKILLS_DIR / skill_name / "references"
        if ref_dir.exists() and not list(ref_dir.glob("*.md")):
            warnings.append(f"{ref_dir}: references/ dir exists but contains no .md files")


def main():
    if not SKILLS_DIR.exists():
        print(f"FAIL  Skills directory not found: {SKILLS_DIR} (run from repo root)")
        sys.exit(1)

    validate_root_files()
    validate_reference_dirs()
    for skill in REQUIRED_SKILLS:
        validate_skill(skill)

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  WARN  {w}")

    if errors:
        print("\nVALIDATION FAILED:")
        for e in errors:
            print(f"  FAIL  {e}")
        sys.exit(1)

    print(f"PASS  All {len(REQUIRED_SKILLS)} skills validated")
    print(f"PASS  Required root files: {', '.join(REQUIRED_ROOT_FILES)}")
    if warnings:
        print(f"WARN  {len(warnings)} warning(s) above")
    print("CI: green")


if __name__ == "__main__":
    main()
