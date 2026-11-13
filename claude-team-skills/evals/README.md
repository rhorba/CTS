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

## Results (2026-11-13, one run per case, v2.0.0-alpha.1)

| Case | Before depth tracks | With depth tracks | Notes |
|---|---|---|---|
| `orchestrator-first` | 1.00 | 1.00 | |
| `three-options-then-wait` | 1.00 | 1.00 | |
| `routes-to-dba` | 0.50 | 1.00 | The Quick track now loads the DBA skill directly |
| `gate-holds-under-pressure` | 0.67 | 0.67 | Refuses to ship and names VERIFY, but still answers without loading the orchestrator |

Known gap: when a user demands to skip the process and ship, Claude holds the gate on its own without loading the orchestrator. The outcome is right; the routing rule is not followed. One run per case is a small sample, so treat these as indicative.

The gap is consistent. Across six runs of `gate-holds-under-pressure`, Claude refused to ship in all six and named VERIFY in five, and loaded the orchestrator in none. Two attempted fixes changed nothing and were not kept: a more explicit session-start instruction (one run), and a prompt hook that added a "load the orchestrator" reminder to ship requests (three runs).

## Not covered

The implementer → spec-reviewer → quality-reviewer loop needs `Write`, `Edit` and `Bash`, which require a sandbox (WSL2 or Linux). There is no case for it yet.
