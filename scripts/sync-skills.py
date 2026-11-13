#!/usr/bin/env python3
"""Mirror the plugin's skills into .claude/skills so this repo runs its own skills.

The single source of truth is claude-team-skills/skills/. Never edit .claude/skills/ by hand.

    python3 scripts/sync-skills.py          # rewrite the mirror
    python3 scripts/sync-skills.py --check  # exit 1 if the mirror has drifted (used in CI)
"""

import filecmp
import shutil
import sys
from pathlib import Path

SOURCE = Path("claude-team-skills/skills")
MIRROR = Path(".claude/skills")


def relative_files(root):
    return {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}


def drift(source=SOURCE, mirror=MIRROR):
    """Return a sorted list of human-readable differences between source and mirror."""
    src = relative_files(source)
    dst = relative_files(mirror) if mirror.exists() else set()
    problems = [f"missing in mirror: {f}" for f in src - dst]
    problems += [f"extra in mirror: {f}" for f in dst - src]
    problems += [
        f"content differs: {f}"
        for f in src & dst
        if not filecmp.cmp(source / f, mirror / f, shallow=False)
    ]
    return sorted(problems)


def sync(source=SOURCE, mirror=MIRROR):
    # File-by-file rather than rmtree + copytree: on Windows a directory held open
    # by an editor or sync client cannot be removed, but its files can be replaced.
    src = relative_files(source)
    dst = relative_files(mirror) if mirror.exists() else set()
    for f in dst - src:
        (mirror / f).unlink()
    for f in src:
        target = mirror / f
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / f, target)
    for d in sorted((p for p in mirror.rglob("*") if p.is_dir()), reverse=True):
        try:
            d.rmdir()  # only succeeds when empty
        except OSError:
            pass


def main(argv):
    if not SOURCE.exists():
        print(f"FAIL  Source not found: {SOURCE} (run from repo root)")
        return 1
    if "--check" in argv:
        problems = drift()
        if problems:
            print("FAIL  .claude/skills has drifted from claude-team-skills/skills:")
            for p in problems:
                print(f"  {p}")
            print("Run: python3 scripts/sync-skills.py")
            return 1
        print("PASS  .claude/skills mirror is in sync")
        return 0
    sync()
    print(f"Synced {len(relative_files(SOURCE))} files to {MIRROR}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
