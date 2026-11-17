# Outreach kit

Messages, a follow-up, reply scripts and a tracker for the direct outreach channel in the
[monetisation plan](monetisation-plan.md). Targets: first 20 messages sent by 27 November 2026,
40 by 13 December 2026.

**Who to write to**: engineering leads and CTOs of teams of 3 to 20 developers who already use
Claude Code (see [CTS for teams](for-teams.md)). One person per company.

**Rules for every message**

- One paragraph, one link, one question. The question comes first; the product comes second.
- Write the first line yourself, about them: something they posted, built or said. Never send a
  message where the first line could go to anyone.
- Send 10 a week. Write each one by hand from a version below; do not mail-merge.
- After 20 messages with no reply, change the opening question or the version before sending more.

## Version A: someone you know

Use for former colleagues, classmates and people who know your work.

> Hi [first name], [one line about them: new role, recent project, something they posted].
> Quick question, since your team uses Claude Code: how do you stop AI-written code shipping
> untested? I've been building an open-source plugin for exactly that. It blocks `git push` until
> tests and coverage are logged, and I've measured whether it actually holds:
> https://github.com/rhorba/CTS. I'd like to hear how your team handles it, even if the answer is
> "we don't". 15 minutes this week or next?

## Version B: cold, on LinkedIn

Use for engineering leads you have not met. Connection notes are capped at 300 characters, so
send the short version as the note and the long version only after they accept.

**Connection note (under 300 characters)**

> Hi [first name], I saw [specific post or project]. I'm researching how teams stop AI-written
> code shipping untested, and built an open-source Claude Code plugin for it. Could I ask you
> one question about how your team handles it?

**After they accept**

> Thanks for connecting, [first name]. The question: when Claude Code writes part of a change,
> what stops it reaching main without tests? Most teams I talk to rely on review catching it.
> I built CTS to make it a hard rule, with a push gate that refuses until verification and
> coverage are logged: https://github.com/rhorba/CTS. How does your team do it today?

## Version C: someone who already uses Claude Code in public

Use for people who post about Claude Code, publish plugins or skills, or write about AI coding
workflows.

> Hi [first name], I read your [post / repo] on [topic]. You mentioned [specific detail]. I've hit
> the same thing from the other side: Claude Code agreeing to "skip the tests and ship it". I
> built CTS, an MIT-licensed plugin that blocks the push with a hook rather than a prompt, and I ran
> evals to check it holds: https://github.com/rhorba/CTS. Does your team have a rule for this,
> or is it down to whoever reviews?

## Follow-up (once, after 5 working days with no reply)

> Hi [first name], bumping this in case it got buried. Short version: how does your team stop
> AI-written code shipping without tests? Happy to share what I've learned either way.

No second follow-up. Mark them "no reply" and move on.

## Reply scripts

**They are interested** → book the call.

> Glad it's useful. Would a 30-minute call work? I'll ask how your team ships today, show the push
> gate in a repository, and you'll know by the end whether CTS fits. Here are three slots:
> [day time], [day time], [day time] ([time zone]). Or send me one that suits you.

**They ask the price** → answer straight, then offer the call.

> CTS itself is free and MIT-licensed. If you want it set up for your team, Team Setup is $900
> (€810 / 8,800 MAD): installed and tuned to your stack, a 90-minute session with your team, and
> two weeks of follow-up questions. The first two teams get it at half price in return for a case
> study. Full details: https://github.com/rhorba/CTS/blob/main/docs/for-teams.md. Worth a
> 30-minute call to see if it fits?

**"Not now" or "we're fine"** → leave the door open, ask for nothing.

> Makes sense, thanks for answering. If AI-written code ever slips through untested, the plugin is
> free to try on its own. Mind if I check back in a few months?

**"We use Cursor / Copilot / another agent"**

> The push gate and the `AGENTS.md` template work outside Claude Code; the session hooks and review
> subagents don't. If you tell me which agent, I'll say exactly what you'd get.

## Tracker

Copy this table into a private note or spreadsheet; do not commit names of real people to this public
repository. Versions: A, B or C. Status: sent, replied, call booked, no reply, not now, quote sent, paid.

| # | Name | Company | Version | Sent | Follow-up | Reply | Status | Next step |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |
| 4 | | | | | | | | |
| 5 | | | | | | | | |
| 6 | | | | | | | | |
| 7 | | | | | | | | |
| 8 | | | | | | | | |
| 9 | | | | | | | | |
| 10 | | | | | | | | |
| 11 | | | | | | | | |
| 12 | | | | | | | | |
| 13 | | | | | | | | |
| 14 | | | | | | | | |
| 15 | | | | | | | | |
| 16 | | | | | | | | |
| 17 | | | | | | | | |
| 18 | | | | | | | | |
| 19 | | | | | | | | |
| 20 | | | | | | | | |

**After every 20**, record these three numbers (the counts, not the names) in `.logs/metrics.md`:
messages sent, replies, calls booked. If replies are 0, change the opening question.
