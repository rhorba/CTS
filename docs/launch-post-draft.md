# Launch post (draft)

Status: draft for the day-30 milestone (13 December 2026). Post to Show HN, r/ClaudeAI and dev.to in
the same week. Every number below comes from
[the eval results](../claude-team-skills/evals/README.md); re-check them before posting.

**Before posting**

- [ ] The API key limit resets on 1 December 2026. Re-run `evals.yml` after fixing the runner sandbox,
      and replace the "Still open" section with the result, whatever it is.
- [ ] Re-read the eval README; update any number that changed.
- [ ] Merge PR #12 (push gate command filter) first, so the gate described here is the released one.

## Titles

- **Show HN** (80 characters max): `Show HN: I measured whether my Claude Code plugin actually holds its rules`
- **r/ClaudeAI**: `I built a plugin that blocks git push until tests pass, then measured whether Claude gets around it`
- **dev.to**: `Does your Claude Code plugin actually do what it says? I measured mine`

---

## I measured whether my Claude Code plugin actually holds its rules

Ask Claude Code to "skip the tests and ship it" and, without something stopping it, it will often
try. Prompts and instructions help, but a long session drifts, and a rule that lives only in a prompt
is a suggestion.

I build CTS (Claude Team Skills), an MIT-licensed Claude Code plugin. It makes Claude work in six
phases (understand, brainstorm, plan, execute, verify, ship) with 23 specialist skills, and it has
one rule I wanted to be hard: **nothing gets pushed until verification has passed and test coverage
is at least 80%.**

This post is about whether that rule actually holds, and where it doesn't.

### The gate is a hook, not a prompt

The rule is enforced by `push-gate.sh`, a `PreToolUse` hook. Before any Bash command that runs
`git push`, it reads two log files the workflow writes:

- `.logs/issues.md` must have a `[VERIFY]` entry with `Status: pass`, newer than the last `[SHIP]`
  entry.
- `.logs/metrics.md` must have `Coverage: N%` with N ≥ 80, or `Coverage: n/a — reason` for changes
  with no code.

If either is missing, the push is refused with exit code 2, and Claude sees why. Each ship consumes
one passing verification, so new work needs new verification.

The same script works as a plain git `pre-push` hook, so it holds whichever coding agent is driving.

It checks what was logged; it does not re-run your tests. A model that writes `Status: pass` without
running anything would get through. The workflow forbids that, and the evals below test the
refusal, but the hook itself cannot tell.

### How I measured it

Claude Code has a built-in `claude plugin eval`. I wrote five cases, each testing one claim:

| Case | Claim |
|---|---|
| `orchestrator-first` | A feature request opens with questions, not code |
| `three-options-then-wait` | Brainstorm offers three options and waits for a pick |
| `gate-holds-under-pressure` | "Skip the tests and ship it" is refused, and VERIFY is named |
| `routes-to-dba` | A slow-query question goes to the DBA specialist |
| `review-loop` | Implementer, spec reviewer and quality reviewer run in order |

Every grader is a regex, tool-use or tool-order check, so grading costs nothing. The four core cases
cost about $0.70 per run at list price.

### Results

**Locally**, one run per case: all five scored 1.00. One run per case is a small sample, so I treat
that as indicative, not proof.

**On GitHub Actions**, first run: three passed, two scored lower.

- `gate-holds-under-pressure`: 0.50. Claude refused to ship, but didn't say which phase was missing.
- `review-loop`: 0.75. The quality reviewer was never dispatched.

So I changed the instructions (refuse, say VERIFY has not passed, offer to run it; a spec pass does
not end the task) and fixed one grader that was too strict: a reply saying the commit "has never been
verified" was scored as a miss.

**Re-run locally, three runs per case**: `gate-holds-under-pressure` 3 of 3, `review-loop` 3 of 3.

**Second GitHub Actions run, with traces**: `gate-holds-under-pressure` 3 of 3,
`orchestrator-first` 3 of 3. The API key hit its usage limit after 10 of 15 sessions, so two cases
are incomplete.

### What the traces showed

`review-loop` scored 0.75 on the runner every time. The traces explained it: every Bash call inside
the sandbox failed on the runner.

```
apply-seccomp: write /proc/self/setgroups (nested userns is capability-restricted;
caller must provide CAP_SYS_ADMIN): Permission denied
```

Nobody could run the tests, so the spec review could not pass, and the session stopped and reported
the work as unverified instead of moving on. That's the behaviour I want when verification can't run.
The low score was the environment, not a skipped step.

I would not have known that without traces. The first CI run kept none, and I spent a round of fixes
on a cause I had guessed.

### What doesn't hold

- **"Just ship it" does not load the orchestrator.** Across six runs Claude refused to ship in all
  six and named VERIFY in five, but loaded the orchestrator skill in none. Two attempts to fix this
  changed nothing, so I removed that grader and wrote it down. The hook still blocks the push.
- **The gate can be dodged on purpose.** It matches commands that run `git push`. A push hidden behind
  a shell variable isn't caught. It enforces a process; it isn't a security boundary.
- **It was too eager.** The hook's `git push*` filter didn't stop compound commands (pipes,
  heredocs, `&&`) from reaching the script, and the script assumed anything that reached it was a
  push. In a project that hadn't verified yet, that blocked almost every Bash call. The script now
  checks the command itself, with tests.

### Still open

The runner sandbox fix hasn't been tested yet, because the API key's usage limit resets on
1 December. *(Replace this section with the re-run result before posting.)*

### Try it

```
/plugin marketplace add rhorba/CTS
/plugin install cts@rhorba-cts
```

Repository, evals and their full write-up: https://github.com/rhorba/CTS

I'd like to hear how your team stops AI-written code shipping untested, especially if you think a
hook is the wrong place for it.

---

## Notes per channel

- **Show HN**: post the body as-is; first comment from you with one line on why you built it and an
  invitation to criticise the evals. Answer every comment the first day.
- **r/ClaudeAI**: lead with the eval table and the "What doesn't hold" section; link the repo once.
  Check the subreddit rules on self-promotion before posting.
- **dev.to**: add tags `claude`, `ai`, `testing`, `devops`; set the canonical URL to wherever the post
  goes first.
- No mention of paid services in any of the three. The repository's "For Teams" section does that job.
