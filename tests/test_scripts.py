"""Tests for scripts/validate-skills.py and scripts/sync-skills.py."""

import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def load(name):
    """Import a hyphenated script file as a module."""
    path = REPO / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate = load("validate-skills")
sync = load("sync-skills")

SKILL_BODY = "x" * 120


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_plugin(root, skills=None):
    """Build a minimal valid plugin + marketplace under root. Returns (plugin_dir, marketplace)."""
    plugin = root / "plugin"
    for name in skills if skills is not None else validate.REQUIRED_SKILLS:
        write(
            plugin / "skills" / name / "SKILL.md",
            f"---\nname: {name}\ndescription: does things\n---\n{SKILL_BODY}\n",
        )
    for filename in validate.REQUIRED_PLUGIN_FILES:
        write(plugin / filename, "y" * 60)
    write(
        plugin / ".claude-plugin" / "plugin.json",
        json.dumps({"name": "cts", "version": "1.0.0", "description": "d"}),
    )
    marketplace = root / "marketplace.json"
    write(
        marketplace,
        json.dumps({"name": "m", "owner": {"name": "o"}, "plugins": [{"name": "cts"}]}),
    )
    return plugin, marketplace


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)


class ValidateTests(TempDirCase):
    def run_checks(self, plugin, marketplace, docs=()):
        return validate.run(plugin, marketplace, list(docs))

    def test_valid_plugin_passes(self):
        plugin, marketplace = make_plugin(self.root)
        errors, warnings = self.run_checks(plugin, marketplace)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_real_repo_passes(self):
        old = os.getcwd()
        os.chdir(REPO)
        try:
            errors, _ = validate.run()
        finally:
            os.chdir(old)
        self.assertEqual(errors, [])

    def test_missing_skills_dir(self):
        errors, _ = self.run_checks(self.root / "nope", self.root / "m.json")
        self.assertIn("Skills directory not found", errors[0])

    def test_missing_skill_file(self):
        plugin, marketplace = make_plugin(self.root)
        (plugin / "skills" / "tester" / "SKILL.md").unlink()
        errors, _ = self.run_checks(plugin, marketplace)
        self.assertTrue(any("Missing required skill file" in e for e in errors))

    def test_frontmatter_problems(self):
        plugin, marketplace = make_plugin(self.root)
        skills = plugin / "skills"
        write(skills / "tester" / "SKILL.md", "no frontmatter here")
        write(skills / "dba" / "SKILL.md", "---\nname: dba\nnever closed")
        write(skills / "copywriter" / "SKILL.md", f"---\ndescription: d\n---\n{SKILL_BODY}")
        write(skills / "deployment" / "SKILL.md", f"---\nname: deployment\n---\n{SKILL_BODY}")
        write(skills / "tech-lead" / "SKILL.md", f"---\nname: other\ndescription: d\n---\n{SKILL_BODY}")
        write(skills / "orchestrator" / "SKILL.md", "---\nname: orchestrator\ndescription: d\n---\nshort")
        errors, _ = self.run_checks(plugin, marketplace)
        joined = "\n".join(errors)
        self.assertIn("Missing YAML frontmatter", joined)
        self.assertIn("Malformed frontmatter", joined)
        self.assertIn("Missing 'name:'", joined)
        self.assertIn("Missing 'description:'", joined)
        self.assertIn("does not match folder", joined)
        self.assertIn("too short", joined)

    def test_crlf_frontmatter_is_accepted(self):
        plugin, marketplace = make_plugin(self.root)
        path = plugin / "skills" / "tester" / "SKILL.md"
        path.write_bytes(f"---\r\nname: tester\r\ndescription: d\r\n---\r\n{SKILL_BODY}".encode())
        errors, _ = self.run_checks(plugin, marketplace)
        self.assertEqual(errors, [])

    def test_unlisted_skill_folder(self):
        plugin, marketplace = make_plugin(self.root)
        write(plugin / "skills" / "surprise" / "SKILL.md", "x")
        errors, _ = self.run_checks(plugin, marketplace)
        self.assertTrue(any("not listed in REQUIRED_SKILLS" in e for e in errors))

    def test_plugin_files(self):
        plugin, marketplace = make_plugin(self.root)
        (plugin / "INSTALL.md").unlink()
        write(plugin / "QUICKSTART.md", "tiny")
        write(plugin / "CLAUDE.md", "should not be here")
        errors, _ = self.run_checks(plugin, marketplace)
        joined = "\n".join(errors)
        self.assertIn("Missing required file", joined)
        self.assertIn("empty or too short", joined)
        self.assertIn("plugin root is not loaded", joined)

    def test_manifest_missing_and_invalid(self):
        plugin, marketplace = make_plugin(self.root)
        marketplace.unlink()
        write(plugin / ".claude-plugin" / "plugin.json", "{not json")
        errors, _ = self.run_checks(plugin, marketplace)
        joined = "\n".join(errors)
        self.assertIn("Missing manifest", joined)
        self.assertIn("invalid JSON", joined)

    def test_manifest_fields_and_name_mismatch(self):
        plugin, marketplace = make_plugin(self.root)
        write(plugin / ".claude-plugin" / "plugin.json", json.dumps({"name": "cts"}))
        write(marketplace, json.dumps({"name": "m", "plugins": [{"name": "different"}]}))
        errors, _ = self.run_checks(plugin, marketplace)
        joined = "\n".join(errors)
        self.assertIn("missing 'version'", joined)
        self.assertIn("missing 'owner'", joined)
        self.assertIn("no plugin entry named 'cts'", joined)

    def test_doc_counts(self):
        plugin, marketplace = make_plugin(self.root)
        doc = self.root / "README.md"
        write(
            doc,
            "23 specialists here\nnever all 21\nall 6 phases are mandatory\n12 AI Specialists\n",
        )
        errors, _ = self.run_checks(plugin, marketplace, [doc, self.root / "absent.md"])
        self.assertEqual(len(errors), 2)
        self.assertIn("README.md:2: says 21", errors[0])
        self.assertIn("README.md:4: says 12", errors[1])

    def test_empty_references_dir_warns(self):
        plugin, marketplace = make_plugin(self.root)
        (plugin / "skills" / "tester" / "references").mkdir()
        errors, warnings = self.run_checks(plugin, marketplace)
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)

    def test_main_reports_pass_and_fail(self):
        old = os.getcwd()
        os.chdir(REPO)
        try:
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(validate.main(), 0)
            self.assertIn("CI: green", out.getvalue())

            os.chdir(self.root)
            (self.root / "claude-team-skills" / "skills" / "tester" / "references").mkdir(parents=True)
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(validate.main(), 1)
            self.assertIn("VALIDATION FAILED", out.getvalue())
            self.assertIn("WARN", out.getvalue())
        finally:
            os.chdir(old)


class SyncTests(TempDirCase):
    def setUp(self):
        super().setUp()
        self.source = self.root / "src"
        self.mirror = self.root / "mirror"
        write(self.source / "a" / "SKILL.md", "alpha")
        write(self.source / "b" / "references" / "r.md", "beta")

    def test_sync_creates_identical_mirror(self):
        sync.sync(self.source, self.mirror)
        self.assertEqual(sync.drift(self.source, self.mirror), [])

    def test_drift_reports_each_kind(self):
        sync.sync(self.source, self.mirror)
        (self.mirror / "a" / "SKILL.md").write_text("changed", encoding="utf-8")
        (self.mirror / "b" / "references" / "r.md").unlink()
        write(self.mirror / "c" / "stale.md", "old")
        self.assertEqual(
            sync.drift(self.source, self.mirror),
            [
                "content differs: a/SKILL.md",
                "extra in mirror: c/stale.md",
                "missing in mirror: b/references/r.md",
            ],
        )

    def test_sync_repairs_drift_and_prunes_empty_dirs(self):
        sync.sync(self.source, self.mirror)
        write(self.mirror / "c" / "stale.md", "old")
        (self.mirror / "a" / "SKILL.md").write_text("changed", encoding="utf-8")
        sync.sync(self.source, self.mirror)
        self.assertEqual(sync.drift(self.source, self.mirror), [])
        self.assertFalse((self.mirror / "c").exists())

    def test_drift_when_mirror_absent(self):
        self.assertEqual(len(sync.drift(self.source, self.mirror)), 2)

    def run_main(self, argv):
        old = os.getcwd()
        os.chdir(self.root)
        out = io.StringIO()
        try:
            with redirect_stdout(out):
                code = sync.main(argv)
        finally:
            os.chdir(old)
        return code, out.getvalue()

    def test_main_modes(self):
        code, out = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("Source not found", out)

        write(self.root / "claude-team-skills" / "skills" / "a" / "SKILL.md", "alpha")
        code, out = self.run_main(["--check"])
        self.assertEqual(code, 1)
        self.assertIn("drifted", out)

        code, out = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("Synced 1 files", out)

        code, out = self.run_main(["--check"])
        self.assertEqual(code, 0)
        self.assertIn("in sync", out)


if __name__ == "__main__":
    unittest.main()
