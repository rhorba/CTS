# CTS behavioural evals

Four cases that check what CTS claims, using Claude Code's built-in `claude plugin eval`. Every grader is a regex or a tool-use check, so grading is free; the only cost is the four agent runs.

| Case | Claim it tests |
|---|---|
| `orchestrator-first` | A plain feature request loads the orchestrator and opens with questions, not code |
| `three-options-then-wait` | BRAINSTORM offers Simple / Balanced / Comprehensive and waits for a pick |
| `gate-holds-under-pressure` | "Skip the tests and ship it" is refused and VERIFY is named |
| `routes-to-dba` | A slow-query question is routed to the DBA specialist |

## Run

From `claude-team-skills/`:

```bash
claude plugin eval . --runs 1 --ablation none --no-publish --scaffold
```

- `--runs 1 --ablation none` runs each case once with no no-plugin baseline: four sessions, about $0.65 at list price. Drop both flags for three runs per case plus a baseline (about six times the cost).
- `--scaffold` lets `gate-holds-under-pressure` build its fixture repository. The script is `gate-holds-under-pressure/fixture.sh`.
- Cases use read-only tools only, so they run on native Windows, which has no sandbox for shell-granting cases.

## Baseline (2026-11-13, one run per case, v2.0.0-alpha.1)

| Case | Score | Notes |
|---|---|---|
| `orchestrator-first` | 1.00 | |
| `three-options-then-wait` | 1.00 | |
| `gate-holds-under-pressure` | 0.67 | Refused to ship and named VERIFY, but answered without loading the orchestrator |
| `routes-to-dba` | 0.50 | Recommended the right composite index, but answered without loading any skill |

Both failures are the same gap: for a direct question or a "skip the process" demand, Claude gives a correct answer on its own instead of routing through the orchestrator. The outcome was right both times; the "orchestrator first, always" rule was not followed. One run per case is a small sample, so treat these as indicative.

## Not covered

The implementer → spec-reviewer → quality-reviewer loop needs `Write`, `Edit` and `Bash`, which require a sandbox (WSL2 or Linux). There is no case for it yet.
