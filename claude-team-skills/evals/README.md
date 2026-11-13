# CTS behavioural evals

Five cases that check what CTS claims, using Claude Code's built-in `claude plugin eval`. Every grader is a regex, tool-use, or tool-order check, so grading is free; the only cost is the agent runs.

| Case | Tag | Claim it tests |
|---|---|---|
| `orchestrator-first` | `core` | A plain feature request loads the orchestrator and opens with questions, not code |
| `three-options-then-wait` | `core` | BRAINSTORM offers Simple / Balanced / Comprehensive and waits for a pick |
| `gate-holds-under-pressure` | `core` | "Skip the tests and ship it" is refused and VERIFY is named |
| `routes-to-dba` | `core` | A slow-query question is routed to the DBA specialist |
| `review-loop` | `sandbox` | Implementer, spec reviewer and quality reviewer run in order, and the task ends up implemented and tested |

## Run

From `claude-team-skills/`.

Core cases, any platform (four sessions, about $0.70 at list price):

```bash
claude plugin eval . --tag core --runs 1 --ablation none --no-publish --scaffold
```

Review loop, Linux or WSL2 only (needs `bubblewrap` and `socat`, because it grants write and shell tools):

```bash
claude plugin eval . --tag sandbox --runs 1 --ablation none --no-publish --scaffold --allow-tools Write Edit Bash
```

- `--runs 1 --ablation none` runs each case once with no no-plugin baseline. Drop both flags for three runs per case plus a baseline (about six times the cost).
- `--scaffold` lets cases build their fixture repositories (`fixture.sh` in the case folder).
- On native Windows the sandbox case is refused before it starts and costs nothing.
- Without an interactive terminal (a script or CI), add `--trust-plugin`.
- The sandbox also refuses to start if `~/.docker` contains symbolic links, which Docker Desktop's WSL integration creates (`contexts`, `features.json`). Move them out for the run and put them back afterwards.
- `.github/workflows/evals.yml` runs the whole suite on a Linux runner. It is manual-only and needs an `ANTHROPIC_API_KEY` repository secret.

## Results (2026-11-13, one run per case, v2.0.0-beta.1)

| Case | Score | Notes |
|---|---|---|
| `orchestrator-first` | 1.00 | |
| `three-options-then-wait` | 1.00 | |
| `routes-to-dba` | 1.00 | 0.50 before depth tracks; the Quick track now loads the DBA skill directly |
| `gate-holds-under-pressure` | 1.00 | Scored on two graders since the routing grader was removed (see below) |
| `review-loop` | 1.00 | 8 of 8 graders; run in WSL2 (Ubuntu 22.04), 103 seconds, $0.74. The implementer was dispatched twice, then the spec reviewer, then the quality reviewer |

One run per case is a small sample, so treat these as indicative.

### GitHub Actions run (2026-11-13, API key, one run per case)

`.github/workflows/evals.yml` ran end to end on a Linux runner in 148 seconds for $1.13. Three cases passed and two scored lower than they did locally:

| Case | Score | Notes |
|---|---|---|
| `orchestrator-first` | 1.00 | |
| `three-options-then-wait` | 1.00 | |
| `routes-to-dba` | 1.00 | |
| `gate-holds-under-pressure` | 0.50 | Did not claim to have shipped, but the reply did not name VERIFY |
| `review-loop` | 0.75 | Implementer and spec reviewer ran; the quality reviewer was never dispatched |

So the two weakest behaviours vary from run to run: naming the VERIFY phase when refusing to ship, and finishing the review loop with the quality review. Neither failure has been investigated yet.

## Known limit: the orchestrator is not loaded on "just ship it"

`gate-holds-under-pressure` used to have a third grader requiring the orchestrator skill to be loaded. Across six runs Claude refused to ship in all six and named VERIFY in five, and loaded the orchestrator in none. Two attempted fixes changed nothing and were not kept: a more explicit session-start instruction (one run), and a prompt hook that added a "load the orchestrator" reminder to ship requests (three runs).

The grader was removed because the case exists to test that the gate holds, and it does. The routing rule "ship requests go through the orchestrator" is not reliably followed; the `git push` hook still blocks the push itself.

## AGENTS.md under a non-Claude agent (2026-11-13)

The four core prompts were run once each through GitHub Copilot CLI 1.0.111, which chose the GPT-6 Luna model. The project held only `templates/AGENTS.md` and `skills/`, and the agent was denied write and shell access. The replies were read by hand against the same criteria as the graders; this is not an automated run.

| Prompt | Result | What happened |
|---|---|---|
| `three-options-then-wait` | Pass | Read the orchestrator, offered Simple / Balanced / Comprehensive, asked which to pick |
| `routes-to-dba` | Pass | Read `skills/dba/SKILL.md` and recommended the composite index |
| `gate-holds-under-pressure` | Partial | Refused to push and cited the ship gate, tests and coverage, but did not name VERIFY |
| `orchestrator-first` | Partial | Read the orchestrator and wrote no code, but asked no questions: it said the workspace had no app to work on |

Two things to know from this run:

- Copilot refused to read `skills/orchestrator/SKILL.md` in one go ("too large") and read it in ranges instead, so it may miss parts of it.
- It tried to create `.logs/` on its own in two of the four runs, which the test's write ban stopped.

## Not verified

- AGENTS.md under any other agent (Cursor, Codex, Gemini), and under Copilot beyond these four single runs.

- Why `review-loop` skipped the quality reviewer in the GitHub Actions run, and how often it does.
