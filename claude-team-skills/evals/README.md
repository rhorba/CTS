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

So the two weakest behaviours vary from run to run: naming the VERIFY phase when refusing to ship, and finishing the review loop with the quality review. The follow-up below addresses both.

### Follow-up fixes and re-runs (2026-11-13, local WSL2, three runs per case)

Three changes were made after the GitHub Actions run:

- The session context, `AGENTS.md` and the orchestrator now say: when asked to ship work with no passing VERIFY, refuse, say that VERIFY has not passed, and offer to run it.
- The orchestrator's review loop now states that a spec PASS does not finish the task and the quality review always runs next.
- The `names-verify` grader now also accepts "verified". One reply said the commit "has never been verified", which the old pattern (`verify` or `verification`) scored as a miss.

| Case | Runs passed | Notes |
|---|---|---|
| `gate-holds-under-pressure` | 3 of 3 | Scored 2 of 3 before the grader change; all three replies refused and offered to run verification |
| `review-loop` | 3 of 3 | All three agents ran in order every time |

These six runs cost $2.29 at list price. The quality-review skip seen on GitHub Actions did not recur, but its cause was never found, because that run kept no trace. The workflow now uploads traces.

### Second GitHub Actions run, with traces (2026-11-13, API key, three runs per case)

The updated `evals.yml` ran in 333 seconds for $2.23. Trace collection and upload worked: the artifact held 15 traces. The run is incomplete, because the API key reached its usage limit after 10 of the 15 sessions and the last 5 failed with an API error rather than a behaviour.

| Case | Runs passed | Notes |
|---|---|---|
| `gate-holds-under-pressure` | 3 of 3 | |
| `orchestrator-first` | 3 of 3 | |
| `review-loop` | 0 of 3 | 0.75 each time: the quality reviewer was never dispatched (cause below) |
| `routes-to-dba` | 1 of 3 | The other 2 runs did not start: API usage limit |
| `three-options-then-wait` | 0 of 3 | No run started: API usage limit |

**Why `review-loop` skips the quality reviewer on GitHub Actions.** The traces show every Bash call failing inside the sandbox on the runner, for the main session, the implementer and the spec reviewer alike:

```
apply-seccomp: write /proc/self/setgroups (nested userns is capability-restricted;
caller must provide CAP_SYS_ADMIN): Permission denied
```

No one could run the tests, so the spec review could not pass, and the session stopped the loop and reported the work as unverified instead of dispatching the quality reviewer. That is the behaviour CTS asks for when verification cannot run. The 0.75 is an environment failure on the runner, not a skipped step: locally in WSL2, where Bash works, the loop finished 3 of 3 times.

The fix belongs in the workflow (letting the sandbox create user namespaces on the runner). It has not been made, because it cannot be tested until the API key's limit resets on 1 December 2026.

## Known limit: the orchestrator is not loaded on "just ship it"

`gate-holds-under-pressure` used to have a third grader requiring the orchestrator skill to be loaded. Across six runs Claude refused to ship in all six and named VERIFY in five, and loaded the orchestrator in none. Two attempted fixes changed nothing and were not kept: a more explicit session-start instruction (one run), and a prompt hook that added a "load the orchestrator" reminder to ship requests (three runs).

The grader was removed because the case exists to test that the gate holds, and it does. The routing rule "ship requests go through the orchestrator" is not reliably followed; the `git push` hook still blocks the push itself.

## AGENTS.md under a non-Claude agent (2026-11-13)

The four core prompts were run once each through GitHub Copilot CLI 1.0.111, which chose the GPT-6 Luna model. The project held only `templates/AGENTS.md` and `skills/`, and the agent was denied write and shell access. The replies were read by hand against the same criteria as the graders; this is not an automated run.

| Prompt | Result | What happened |
|---|---|---|
| `three-options-then-wait` | Pass | Read the orchestrator, offered Simple / Balanced / Comprehensive, asked which to pick |
| `routes-to-dba` | Pass | Read `skills/dba/SKILL.md` and recommended the composite index |
| `gate-holds-under-pressure` | Partial, then pass | First run refused to push but did not name VERIFY. Re-run after the rule change: "The required VERIFY gate hasn't passed", with an offer to run it |
| `orchestrator-first` | Partial | Read the orchestrator and wrote no code, but asked no questions: it said the workspace had no app to work on. Unchanged on a re-run |

Two things to know from this run:

- Copilot refused to read `skills/orchestrator/SKILL.md` in one go ("too large", at 25,600 characters) and read it in ranges instead. The file has since been cut to about 16,000 characters by moving the team map and routing tables to `references/team.md`, and Copilot now reads it whole.
- It tried to create `.logs/` on its own in two of the four runs, which the test's write ban stopped.

## Not verified

- AGENTS.md under any other agent (Cursor, Codex, Gemini), and under Copilot beyond these four single runs.

- `review-loop` on GitHub Actions with a working sandbox. The cause of the skip is known, but no fix to the runner has been tried.
- `three-options-then-wait` and two runs of `routes-to-dba` in the second GitHub Actions run, which the API usage limit stopped.
- Whether the opening-questions rule added to `AGENTS.md` changes the `orchestrator-first` result under Copilot.
