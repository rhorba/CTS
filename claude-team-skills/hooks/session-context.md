# Claude Team Skills (CTS) is active

Pick a track for each work request before responding:

- **Quick**: one question or one small change, inside a single specialist's domain, with one obvious approach (a slow query, a one-line fix, a wording tweak). Load the matching specialist skill directly (`cts:dba`, `cts:backend-dev`, `cts:copywriter`, …) and answer with it. Then, if `.logs/` exists, append one `[QUICK]` entry to `.logs/activity.md`.
- **Standard or Full**: everything else. Features, bugs that need investigation, anything touching auth, payments, or data migrations, anything needing more than one specialist, and every request to ship or deploy. Load `cts:orchestrator` first and follow it.

When unsure, it is not Quick. The user can force a track by saying "quick", "standard", or "full".

Rules on every track:

- All six phases happen and are logged: UNDERSTAND → BRAINSTORM → PLAN → EXECUTE → VERIFY → SHIP. On Quick they take a line each inside one `[QUICK]` entry; they are never skipped.
- On Standard and Full there are two user gates: the user picks a BRAINSTORM option before PLAN, and confirms the PLAN before EXECUTE. Load one specialist at a time, with a written HANDOFF note on every switch.
- `git push` is blocked by a hook until VERIFY is logged as passing and coverage is logged. The hook reads:
  - `.logs/issues.md`: an entry headed `### [date] [VERIFY] — title` containing `- Status: pass`, newer than the last `[SHIP]` entry in `.logs/activity.md`
  - `.logs/metrics.md`: a line `Coverage: N%` with N ≥ 80, or `Coverage: n/a — reason` when the change has no executable code
- After shipping, log `### [date] [SHIP] — title` to `.logs/activity.md`.

`[QUICK]` entry format:

```
### [YYYY-MM-DD HH:MM] [QUICK] — [title]
- Specialist: [skill used]
- Understand: [the question or change, one line]
- Approach: [what was chosen and why, one line]
- Result: [what was answered or changed]
- Verify: [how it was checked, or "advice only — nothing executed"]
```
