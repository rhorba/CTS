# CTS monetisation plan

Drafted 13 November 2026. Status: draft for review.

## Summary

CTS stays free and MIT-licensed. Revenue comes from paid services to **teams** that use Claude Code:
a fixed-price setup, a workshop, and custom skill packs. Nothing new has to be built to start selling.

The starting position is 0 stars, 0 forks and no users, so the first 90 days are mostly about reaching
teams and getting two paid reference customers. Every price below is a proposal to test, not a
measured market rate.

## Charter

- **Objective**: earn the first service revenue from CTS within 90 days without closing the source.
- **In scope**: three service offers, a price test, an outreach channel, a decision point for open core.
- **Out of scope**: paid product tiers, a hosted service, a licence change, paid ads.
- **Success criteria**: 2 paying teams and 1 published case study by day 90.
- **Constraints**: one person, part-time; hours per week set the ceiling (see Capacity).

## Offers

| Offer | What the team gets | Your hours | USD | EUR | MAD |
|---|---|---|---|---|---|
| **Team Setup** | CTS installed and tuned to their stack, the push gate and logs working in one of their repos, a 90-minute working session, 2 weeks of follow-up questions | 10 | $900 | €810 | 8,800 MAD |
| **Team Workshop** | Half-day live session: the six phases on one of their real tasks, plus a recording | 6 | $500 | €450 | 4,900 MAD |
| **Custom Skill Pack** | One new specialist or a tuned version of an existing one for their domain, with an eval case | 5 | $400 | €360 | 3,900 MAD |

Prices are set in USD and converted at about 9.8 MAD per USD and 10.9 MAD per EUR (rates seen
7 to 11 November 2026), then rounded. Re-check the rates before quoting. The hours include preparation.

Team Setup is the lead offer. The workshop is the lower-commitment way in for a team that is not ready
to change its workflow; the skill pack is the follow-on sale.

## Capacity by hours per week

Assumptions, both yours to correct: 4.33 weeks per month, and 30% of your hours go to outreach,
calls and invoicing, leaving 70% for delivery.

```
delivery hours per month = hours per week × 4.33 × 0.70
```

| Hours per week | Delivery hours per month | What fits | Monthly ceiling |
|---|---|---|---|
| 5 | 15 | 1 Team Setup + 1 Skill Pack | $1,300 · €1,170 · 12,700 MAD |
| 10 | 30 | 3 Team Setups | $2,700 · €2,430 · 26,400 MAD |
| 20 | 61 | 6 Team Setups | $5,400 · €4,860 · 52,800 MAD |

These are ceilings if every delivery hour is sold. They are not forecasts: in the first 90 days expect
most hours to go to outreach, so the 30% figure will be too low at the start.

## Price test

1. **First two teams**: 50% off Team Setup in return for a written case study and permission to name them.
2. **Next five quotes**: full price, no discount offered. A "yes" is a paid deposit or a signed order,
   not a verbal one.
3. **Reading the result**:
   - 3 or more of 5 accept without negotiating: raise prices 25% for the next five.
   - 1 or 2 accept: keep the price.
   - 0 accept and price is the stated reason: cut the scope (fewer hours), not the hourly value.
   - 0 accept for another reason: the offer is wrong, not the price. Ask what they would pay for.

Quote local teams in MAD and foreign teams in USD or EUR. Whether to keep one price everywhere or set
a lower local price is open; the table uses one price.

## Reaching the first 10 teams

The buyer is an engineering lead or CTO of a team of 3 to 20 developers that already pays for Claude
Code and has been burned by unreviewed AI-written code reaching production.

**What you show them** (already in the repo):

- The push gate: `git push` is blocked until VERIFY and coverage are logged. This is the one claim
  backed by code and by eval runs, so it leads.
- The eval results, including the runs that failed. Measured behaviour is rarer than claims.
- `cts-comparison.pdf` and the pitch deck for the follow-up.

**Channels, in order**:

1. **Direct outreach**: 10 personal messages a week to engineering leads you can reach through your
   own network and LinkedIn. One paragraph, one link, one question ("how do you stop AI-written code
   shipping untested?"). This is the only channel that can produce a customer in the first month.
2. **One launch post**: a write-up of the push gate and the evals ("I measured whether my Claude Code
   plugin actually holds its rules"), posted to Hacker News (Show HN), r/ClaudeAI and dev.to in the
   same week.
3. **Plugin directories**: list CTS wherever Claude Code plugins are indexed. Low effort, slow return.
4. **README**: add a short "For teams" section linking to a one-page offer with a contact address.

**Targets for day 90** (planning assumptions, not benchmarks): 100 outreach messages sent, 15 calls,
7 quotes, 2 paid.

## Timeline

| By | Milestone |
|---|---|
| Day 14 (27 November 2026) | Offer page live, "For teams" section in README, GitHub Sponsors on, first 20 messages sent |
| Day 30 (13 December 2026) | Launch post published, 40 messages sent, first calls held |
| Day 60 (12 January 2027) | First discounted Team Setup delivered, case study drafted |
| Day 90 (11 February 2027) | 2 paying teams, 1 case study published, price test read |

## Risks

| Risk | Probability | Impact | Score | Mitigation |
|---|---|---|---|---|
| No audience: outreach gets no replies | H | H | 9 | Lead with the question, not the product; change the message after every 20 with no reply |
| Teams want it free because the core is free | M | M | 4 | Sell the time saved and the tuning, never the files |
| Claude Code ships a built-in equivalent | M | H | 6 | Keep services tied to your expertise, not to the plugin |
| Hours run out: delivery crowds out outreach | M | M | 4 | Cap at the table above; take the next customer only when a slot is free |
| Invoicing foreign clients and tax status | M | M | 4 | Open question: confirm with an accountant before the first invoice |

## When to revisit open core

Reconsider a paid product tier when both are true:

- 5 teams have paid for a service, and
- the same request has come up from 3 of them (for example a dashboard over `.logs/`, or hosted evals).

Until then, a paid tier has nobody to sell to.

## Open questions

1. How many hours per week will you commit? The plan works at 5; pick the row.
2. One price everywhere, or a lower local price in MAD?
3. Legal form for invoicing, and whether foreign-currency invoices need anything extra.
