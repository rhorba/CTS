"""Behaviour tests for the plugin's shell hooks. Each test runs the real script with sh."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOOKS = REPO / "claude-team-skills" / "hooks"
SH = shutil.which("sh")

VERIFY_PASS = "### [2026-01-01 10:00] [VERIFY] — feature\n- Tests: 5 passed / 0 failed\n- Status: pass\n"
VERIFY_FAIL = "### [2026-01-01 09:00] [VERIFY] — feature\n- Tests: 3 passed / 2 failed\n- Status: fail\n"
SHIP = "### [2026-01-01 11:00] [SHIP] — feature\n- Status: complete\n"


@unittest.skipIf(SH is None, "sh is not available")
class HookCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.project = Path(self._tmp.name)
        self.logs = self.project / ".logs"
        self.addCleanup(self._tmp.cleanup)

    def log(self, name, text):
        self.logs.mkdir(exist_ok=True)
        (self.logs / name).write_text(text, encoding="utf-8", newline="\n")

    def run_hook(self, script):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=self.project.as_posix())
        return subprocess.run(
            [SH, (HOOKS / script).as_posix()],
            input="{}",
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            timeout=30,
        )


class PushGateTests(HookCase):
    def gate(self):
        return self.run_hook("push-gate.sh")

    def assert_blocked(self, result, fragment):
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn(fragment, result.stderr)

    def test_allows_projects_without_cts_logs(self):
        self.assertEqual(self.gate().returncode, 0)

    def test_blocks_when_issues_log_missing(self):
        self.logs.mkdir()
        self.assert_blocked(self.gate(), "VERIFY has not been logged")

    def test_blocks_when_no_verify_entry(self):
        self.log("issues.md", "# Issue Log\n### [2026-01-01] BUG — something\n- Status: open\n")
        self.assert_blocked(self.gate(), "no [VERIFY] entry")

    def test_blocks_when_latest_verify_failed(self):
        self.log("issues.md", VERIFY_PASS + VERIFY_FAIL)
        self.log("metrics.md", "Coverage: 95%\n")
        self.assert_blocked(self.gate(), "not 'Status: pass'")

    def test_blocks_when_verify_already_shipped(self):
        self.log("issues.md", VERIFY_PASS)
        self.log("activity.md", SHIP)
        self.log("metrics.md", "Coverage: 95%\n")
        self.assert_blocked(self.gate(), "already used by a previous SHIP")

    def test_failed_verifies_do_not_count_toward_ships(self):
        # Sprint 1: fail, pass, ship. Sprint 2 pushes with only an old failure on top.
        self.log("issues.md", VERIFY_FAIL + VERIFY_PASS)
        self.log("activity.md", SHIP)
        self.log("metrics.md", "Coverage: 95%\n")
        self.assert_blocked(self.gate(), "already used by a previous SHIP")

    def test_blocks_when_coverage_not_logged(self):
        self.log("issues.md", VERIFY_PASS)
        self.assert_blocked(self.gate(), "no coverage logged")
        self.log("metrics.md", "# Project Metrics\n")
        self.assert_blocked(self.gate(), "no coverage logged")

    def test_blocks_when_coverage_below_gate(self):
        self.log("issues.md", VERIFY_PASS)
        self.log("metrics.md", "- [2026-01-01] Coverage: 91%\n- [2026-01-02] Coverage: 79%\n")
        self.assert_blocked(self.gate(), "coverage is 79%")

    def test_blocks_when_coverage_unreadable(self):
        self.log("issues.md", VERIFY_PASS)
        self.log("metrics.md", "Coverage: pending\n")
        self.assert_blocked(self.gate(), "could not read a percentage")

    def test_allows_verified_and_covered(self):
        self.log("issues.md", VERIFY_FAIL + VERIFY_PASS)
        self.log("metrics.md", "- [2026-01-01] Coverage: 60%\n- [2026-01-02] Coverage: 80%\n")
        result = self.gate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_allows_second_sprint_after_new_verify(self):
        self.log("issues.md", VERIFY_PASS + VERIFY_PASS)
        self.log("activity.md", SHIP)
        self.log("metrics.md", "Coverage: 88.5%\n")
        self.assertEqual(self.gate().returncode, 0)

    def test_allows_coverage_not_applicable(self):
        self.log("issues.md", VERIFY_PASS)
        self.log("metrics.md", "Coverage: 40%\nCoverage: n/a — documentation only\n")
        self.assertEqual(self.gate().returncode, 0)


@unittest.skipIf(SH is None or shutil.which("git") is None, "sh and git are required")
class GitPrePushTests(HookCase):
    """push-gate.sh also works as a plain git pre-push hook, for agents without Claude Code hooks."""

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args],
            cwd=cwd or self.project,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=60,
        )

    def setUp(self):
        super().setUp()
        self.remote = self.project.parent / (self.project.name + "-remote.git")
        self.addCleanup(shutil.rmtree, self.remote, True)
        self.git("init", "-q", "--bare", str(self.remote), cwd=self.project.parent)
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "T")
        self.git("config", "core.hooksPath", ".git/hooks")
        self.git("remote", "add", "origin", self.remote.as_posix())
        (self.project / "a.txt").write_text("a", encoding="utf-8")
        self.log("issues.md", "# Issue Log\n")
        self.git("add", "a.txt")
        self.git("commit", "-q", "-m", "init")
        hook = self.project / ".git" / "hooks" / "pre-push"
        hook.parent.mkdir(exist_ok=True)
        shutil.copyfile(HOOKS / "push-gate.sh", hook)
        hook.chmod(0o755)

    def test_push_blocked_then_allowed(self):
        blocked = self.git("push", "origin", "HEAD:main")
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("CTS push gate", blocked.stderr)

        self.log("issues.md", VERIFY_PASS)
        self.log("metrics.md", "Coverage: 90%\n")
        allowed = self.git("push", "origin", "HEAD:main")
        self.assertEqual(allowed.returncode, 0, allowed.stderr)


class SessionStartTests(HookCase):
    def test_prints_rules_and_init_hint_without_logs(self):
        result = self.run_hook("session-start.sh")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("cts:orchestrator", result.stdout)
        self.assertIn("init-logs.sh", result.stdout)

    def test_prints_only_the_last_session_end(self):
        self.log(
            "sessions.md",
            "# Session Log\n"
            "### [2026-01-01 09:00] SESSION_START\n- Task: old\n"
            "### [2026-01-01 10:00] SESSION_END\n- Completed: OLD WORK\n"
            "### [2026-01-02 09:00] SESSION_START\n- Task: new\n"
            "### [2026-01-02 10:00] SESSION_END\n- Completed: NEW WORK\n- Next: tests\n"
            "### [2026-01-03 09:00] SESSION_START\n- Task: UNFINISHED\n",
        )
        result = self.run_hook("session-start.sh")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("NEW WORK", result.stdout)
        self.assertIn("Next: tests", result.stdout)
        self.assertNotIn("OLD WORK", result.stdout)
        self.assertNotIn("UNFINISHED", result.stdout)
        self.assertIn("Continue from here", result.stdout)

    def test_reports_first_session(self):
        self.log("sessions.md", "# Session Log\n### [2026-01-01 09:00] SESSION_START\n")
        result = self.run_hook("session-start.sh")
        self.assertIn("first logged session", result.stdout)


class SessionEndTests(HookCase):
    def sessions(self):
        return (self.logs / "sessions.md").read_text(encoding="utf-8")

    def test_no_logs_is_a_no_op(self):
        self.assertEqual(self.run_hook("session-end.sh").returncode, 0)
        self.assertFalse(self.logs.exists())

    def test_closes_an_open_session(self):
        self.log("sessions.md", "# Session Log\n### [2026-01-01 09:00] SESSION_START\n- Task: x\n")
        self.assertEqual(self.run_hook("session-end.sh").returncode, 0)
        self.assertIn("SESSION_END (auto)", self.sessions())

    def test_leaves_a_closed_session_alone(self):
        text = "### [2026-01-01 09:00] SESSION_START\n### [2026-01-01 10:00] SESSION_END\n- Completed: all\n"
        self.log("sessions.md", text)
        self.run_hook("session-end.sh")
        self.assertEqual(self.sessions(), text)

    def test_auto_close_is_not_repeated(self):
        self.log("sessions.md", "### [2026-01-01 09:00] SESSION_START\n")
        self.run_hook("session-end.sh")
        self.run_hook("session-end.sh")
        self.assertEqual(self.sessions().count("SESSION_END (auto)"), 1)


class HooksConfigTests(unittest.TestCase):
    def test_every_configured_script_exists(self):
        config = json.loads((HOOKS / "hooks.json").read_text(encoding="utf-8"))
        commands = [
            handler["command"]
            for groups in config["hooks"].values()
            for group in groups
            for handler in group["hooks"]
        ]
        self.assertEqual(len(commands), 3)
        for command in commands:
            script = command.split("/hooks/")[1].rstrip('"')
            self.assertTrue((HOOKS / script).exists(), script)

    def test_push_gate_is_scoped_to_git_push(self):
        config = json.loads((HOOKS / "hooks.json").read_text(encoding="utf-8"))
        handler = config["hooks"]["PreToolUse"][0]["hooks"][0]
        self.assertEqual(handler["if"], "Bash(git push*)")


if __name__ == "__main__":
    unittest.main()
