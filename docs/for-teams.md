# CTS for teams

**Stop AI-written code reaching production untested.**

Your team already uses Claude Code. CTS adds a gate: `git push` is blocked until verification and
test coverage are logged. I set it up in your repository, tune it to your stack, and show your team
how to work with it.

CTS itself is free and MIT-licensed, and stays that way. You pay for the setup and the time saved,
not for the files.

**[Open a team enquiry](https://github.com/rhorba/CTS/issues/new?template=team-enquiry.md)**

## Who this is for

An engineering lead or CTO of a team of 3 to 20 developers that:

- already pays for Claude Code, and
- has seen AI-written code merged or shipped without tests or review.

## Offers

| Offer | What your team gets | Price |
|---|---|---|
| **Team Setup** | CTS installed and tuned to your stack. The push gate and logs working in one of your repositories. A 90-minute working session with your team. Two weeks of follow-up questions. | $900 · €810 · 8,800 MAD |
| **Team Workshop** | A half-day live session: the six phases applied to one of your real tasks. You keep the recording. | $500 · €450 · 4,900 MAD |
| **Custom Skill Pack** | One new specialist, or an existing one tuned to your domain, delivered with an eval case that tests it. | $400 · €360 · 3,900 MAD |

Prices are fixed, not hourly. Teams in Morocco are quoted in MAD; other teams in USD or EUR.

Not ready to change your workflow? Start with the workshop. Team Setup is the full version.

**Founding teams:** the first two teams get Team Setup at half price, in return for a written case
study and permission to name the team.

## What you can check before you talk to me

Everything below is in this repository.

- **The push gate is code, not a promise.** `push-gate.sh` refuses the push unless the latest
  verification entry passed and logged coverage is at least 80%. It also runs as a plain git
  pre-push hook, whichever coding agent is driving. It checks what was logged; it does not re-run
  your tests.
- **The behaviour is measured.** Five eval cases test what CTS claims, such as refusing "skip the
  tests and ship it". Locally, all five pass. On GitHub Actions, two of the five scored lower on
  the first run, and the write-up says so. See
  [the eval results](../claude-team-skills/evals/README.md).
- **The limits are written down.** CTS is new and has no user base yet.
  [How CTS compares](../README.md#how-cts-compares) lists the established alternatives and when
  to choose them instead.

## How it works

1. **Open an enquiry.** Say what your team builds, how many developers you have, and which offer
   interests you.
2. **We talk for 30 minutes.** You get a fixed quote and a date, or an honest "CTS is not the
   right fit".
3. **I deliver.** Team Setup takes about two weeks from the first session to the end of follow-up.

## Questions

**Why pay if CTS is free?**
You can install it yourself; the instructions are in the README. The paid work
is tuning it to your stack and getting your team to actually use it.

**Do you need access to our code?**
For Team Setup, access to one repository, for the working session. The workshop and the skill pack
can be done without it.

**We use another coding agent.**
The push gate and the `AGENTS.md` template work outside Claude Code. The session hooks and the
review subagents do not. Tell me what you use and I will say what you would get.

**Is the enquiry private?**
No. GitHub issues are public. Leave out anything confidential; we move to a private channel after
the first reply.

---

**[Open a team enquiry](https://github.com/rhorba/CTS/issues/new?template=team-enquiry.md)**
