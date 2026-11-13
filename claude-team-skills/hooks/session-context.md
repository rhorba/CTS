# Claude Team Skills (CTS) is active

Load the `cts:orchestrator` skill before acting on any project request and follow it.

- All six phases run and are logged, every time: UNDERSTAND → BRAINSTORM → PLAN → EXECUTE → VERIFY → SHIP. A phase may be brief; it may not be skipped.
- Two user gates: the user picks a BRAINSTORM option before PLAN, and confirms the PLAN before EXECUTE.
- Load one specialist at a time, with a written HANDOFF note on every switch.
- `git push` is blocked by a hook until VERIFY is logged as passing and coverage is logged. The hook reads:
  - `.logs/issues.md`: an entry headed `### [date] [VERIFY] — title` containing `- Status: pass`, newer than the last `[SHIP]` entry in `.logs/activity.md`
  - `.logs/metrics.md`: a line `Coverage: N%` with N ≥ 80, or `Coverage: n/a — reason` when the change has no executable code
- After shipping, log `### [date] [SHIP] — title` to `.logs/activity.md`.
