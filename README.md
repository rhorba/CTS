# Claude Team Skills

**23 AI Specialists Working as One Team — Built for Claude Code**

> Version 2.0.0-alpha.1 · Zero dependencies · Token-efficient · YAGNI-driven · [MIT License](LICENSE)

Claude Team Skills (CTS) is a collection of 23 interconnected specialist skills for Claude Code. Instead of a generic AI assistant, every task is handled by the right expert — PM, Security Engineer, DBA, Software Architect, Test Architect, and more — all routed by a central Orchestrator that loads one specialist at a time.

---

## Included Resources

This repository ships with companion materials for presentations and onboarding:

| File | Description |
|---|---|
| `cts-comparison.pdf` | CTS beside five agent-workflow frameworks, with its known limits |
| `claude-team-skills-pitch.pptx` | Slide deck — pitch CTS to your team or stakeholders |
| `claude-team-skills-user-manual.docx` | Detailed user manual covering all 23 specialists and workflows |

---

## Installation

### Option A — Install as a plugin (recommended)

In a Claude Code session:

```
/plugin marketplace add rhorba/CTS
/plugin install cts@rhorba-cts
```

On Claude Code 2.1.275 or later, one step also works:

```
/plugin install cts --marketplace rhorba/CTS
```

The 23 specialists load as plugin skills (`cts:orchestrator`, `cts:tester`, …) and update when the plugin updates. Nothing is copied into your project.

### Option B — Copy the files (no plugin system)

#### Step 1 — Copy the `skills/` folder into your project root

Copy `claude-team-skills/skills/` into your project root:

```
your-project/
├── skills/
│   ├── orchestrator/
│   ├── project-manager/
│   ├── scrum-master/
│   ├── system-designer/
│   ├── software-architect/
│   ├── tech-lead/
│   ├── security-engineer/
│   ├── dba/
│   ├── ux-designer/
│   ├── ui-designer/
│   │   └── references/        ← design tokens, anti-slop aesthetic guide
│   ├── motion-designer/
│   │   └── references/        ← motion system + video pipeline, generative visuals
│   ├── design-loop/
│   │   └── references/        ← critic prompts, design-tokens brief template
│   ├── backend-dev/
│   ├── frontend-dev/
│   ├── tester/
│   ├── test-architect/
│   ├── deployment/
│   ├── devops-devsecops/
│   │   └── references/        ← 5 deep-dive security files
│   ├── creative-intelligence/
│   ├── digital-marketer/
│   ├── copywriter/
│   ├── content-marketer/
│   └── project-monitor/
│       ├── references/
│       └── templates/         ← init-logs.sh, generate-report.py
├── CLAUDE.md                  ← Copied from claude-team-skills/templates/CLAUDE.md
├── QUICKSTART.md              ← Cheat sheet
└── .logs/                     ← Auto-created on first session
```

#### Step 2 — Copy `claude-team-skills/templates/CLAUDE.md` to your project root

This is the entry point. Claude Code reads it first on every session and loads the Orchestrator.

### Option C — Other coding agents (`AGENTS.md`)

For agents that read `AGENTS.md` instead of `CLAUDE.md`:

1. Copy `claude-team-skills/skills/` into your project root as `skills/`.
2. Copy `claude-team-skills/templates/AGENTS.md` to your project root.
3. Optional: copy `claude-team-skills/hooks/push-gate.sh` to `.git/hooks/pre-push` and make it executable. Git itself then refuses to push until VERIFY and coverage are logged, whichever agent is driving.

`AGENTS.md` is generated from the skill files (`scripts/build-agents-md.py`), so its specialist table cannot drift. Outside Claude Code there are no session hooks and no `cts:` subagents; the file explains what to do instead.

### Start working

Open Claude Code and describe what you need:

```
"I need to add user authentication"
"There's a 500 error on the login endpoint"
"Set up a CI/CD pipeline"
"Write a launch blog post for our new feature"
"Design the schema for a multi-tenant SaaS app"
```

The Orchestrator handles the rest.

**Zero dependencies.** Plain markdown files — no Node.js, no npm, no build step.

---

## How It Works

```
You describe the task
       │
       ▼
CLAUDE.md loads → reads Orchestrator
       │
       ▼
Orchestrator identifies task type
       │
       ▼
Loads ONLY the needed specialist
       │
       ▼
Interactive: options → pick → execute → verify
       │
       ▼
Switches specialist with a 2-3 line handoff summary
```

**Token cost:** CLAUDE.md (~1K) + Orchestrator (~2K) + one specialist (~1-2K) = ~3-5K tokens for routing. Compare to loading all 23 skills at once: 35K+ tokens wasted.

---

## Full Strict Sequence at a Glance

> These rules are **NON-NEGOTIABLE**. They apply to every session, every task, every specialist. No exceptions.

```
SESSION START
     │
     ▼
① Read .logs/sessions.md → show last SESSION_END → "Continue or new task?"
     │
     ▼
══════════════════════════════════════════════
 PHASE 1 — UNDERSTAND          [log: communications.md]
══════════════════════════════════════════════
     │  Clarify: what, where, how big, who is affected
     │  Ask up to 3 focused questions — no assumptions
     │  Log: [UNDERSTAND] entry
     ▼
══════════════════════════════════════════════
 PHASE 2 — BRAINSTORM          [log: decisions.md]
══════════════════════════════════════════════
     │  Present exactly 3 options:
     │    🟢 SIMPLE        lowest effort / fastest
     │    🟡 BALANCED      moderate effort / good tradeoffs
     │    🔴 COMPREHENSIVE highest effort / most robust
     │  Log: [BRAINSTORM] entry
     │
     ▼
  ⛔ GATE: USER MUST PICK an option before continuing
     (never self-proceed — wait for explicit choice)
     │
     ▼
══════════════════════════════════════════════
 PHASE 3 — PLAN                [log: activity.md]
══════════════════════════════════════════════
     │  Break into 30-60 min task batches
     │  List tasks numbered, with estimated time
     │  Identify which specialists are needed
     │  Log: [PLAN] entry
     │
     ▼
  ⛔ GATE: USER MUST CONFIRM plan before EXECUTE starts
     │
     ▼
══════════════════════════════════════════════
 PHASE 4 — EXECUTE             [log: activity.md]
══════════════════════════════════════════════
     │  One task at a time
     │  Before each task: "Here's what I'm about to do: [1-2 lines]"
     │  After each task: show result → "Good? Next, or adjust?"
     │  Load ONE specialist per task (never all at once)
     │  HANDOFF note required on every specialist switch
     │  Checkpoint after each 30-60 min batch
     │  Log: [TASK COMPLETE] entry per task
     ▼
══════════════════════════════════════════════
 PHASE 5 — VERIFY              [log: issues.md]
══════════════════════════════════════════════
     │  Run tests (unit + integration + e2e as applicable)
     │  Run security review (OWASP checklist minimum)
     │  Fix any CRITICAL/HIGH issues before proceeding
     │  Log: [VERIFY] entry with pass/fail summary
     │
     ▼
  ⛔ GATE: VERIFY MUST PASS before SHIP
     (no exceptions — not even user "ship it" shortcut)
     │
     ▼
══════════════════════════════════════════════
 PHASE 6 — SHIP                [log: activity.md]
══════════════════════════════════════════════
     │  Deploy / commit / release
     │  Update documentation
     │  Log: [SHIP] milestone entry
     ▼
SESSION END
     │
     ▼
Write SESSION_END to .logs/sessions.md:
  - Completed: [list]
  - In progress: [list]
  - Blocked: [list]
  - Next: [planned next steps]
```

### Enforced by Hooks, Not Just Instructions

When CTS is installed as a plugin, three hooks back the rules with code. They are plain POSIX shell with no dependencies (on Windows, Claude Code runs them through Git Bash).

| Hook | Event | What it does |
|---|---|---|
| `session-start.sh` | Session start | Loads the CTS rules and the last `SESSION_END` summary into context |
| `push-gate.sh` | Before any `git push` | Blocks the push unless the latest `[VERIFY]` entry is `Status: pass`, it is newer than the last `[SHIP]`, and logged coverage is ≥ 80% (or `n/a` with a reason) |
| `session-end.sh` | Session end | Closes a session that was opened but never summarised, so the next one does not resume from stale state |

The push gate only applies to projects that have a `.logs/` directory. It checks what was logged, so it catches a skipped VERIFY phase; it does not re-run your tests.

### Fresh-Context Execution and Two-Stage Review

The plugin ships three agents the Orchestrator dispatches during EXECUTE for tasks that change code:

| Agent | Role |
|---|---|
| `cts:implementer` | Builds one task test-first from a self-contained brief, in a fresh context |
| `cts:spec-reviewer` | Checks the result against the brief: nothing missing, nothing wrong, nothing extra |
| `cts:quality-reviewer` | Runs only after the spec review passes: correctness, security, tests, fit, simplicity |

Reviewers are read-only and never see the conversation that produced the code. Small edits, docs, and config stay inline, because three subagents cost more than the task is worth.

### Depth Tracks

Not every request deserves the same ceremony. The track sets how deep each phase goes; it never removes one.

| Track | Use for | Who leads | Phases | User gates |
|---|---|---|---|---|
| ⚡ **Quick** | One question or one small change in a single specialist's domain, with one obvious approach | The matching specialist, loaded directly | One line each, in a single `[QUICK]` log entry | None |
| 🟡 **Standard** | Features, bugs that need investigation, work spanning specialists | Orchestrator | Full phases | Option pick + plan confirmation |
| 🔴 **Full** | New projects, large features, high-risk work | Orchestrator | Standard + document chain + subagent execution with two-stage review | Option pick + plan confirmation + document approvals |

Auth, payments, data migrations, and any request to ship are never Quick. Say "quick", "standard", or "full" to override the track. The push gate is identical on all three.

### Strict Rules Summary

| Rule | Detail |
|---|---|
| **All 6 phases mandatory** | Every phase is logged on every track — a line each on Quick, in full on Standard and Full |
| **No silent phase skips** | If user says "skip this" → acknowledge in one sentence, log it, continue |
| **2 hard gates** (Standard, Full) | BRAINSTORM → PLAN requires user option pick; PLAN → EXECUTE requires user confirmation |
| **1 ship gate** | VERIFY must pass (tests + security) before SHIP — no exceptions |
| **One specialist at a time** | Never load all 23 skills — Orchestrator + 1 specialist per task |
| **Written handoffs** | Every specialist switch gets a 2-3 line HANDOFF note |
| **Confirm before code** | Present approach, get approval, then generate — prevents rewrites |
| **Log in same tool call** | Log after action, in the same call — no extra round-trips |
| **YAGNI gate** | Before building anything: "Is this needed RIGHT NOW?" Default to 🟢 SIMPLE |
| **CI monitoring** | DevOps watches every push — CI red = stop all work, fix first |
| **≥80% coverage** | Combined unit + integration coverage gate before every SHIP |
| **Document-first** | New projects/large features: PRD → Architecture → Stories before coding |

---

## CTS Session Playbook

A step-by-step reference for running a session strictly. Copy this into any project context to enforce compliance.

### Step 0 — Session Open (always first)

```
1. Read .logs/sessions.md
2. Find the last SESSION_END block
3. Display:
   📋 Last session:
   - Completed: [...]
   - In progress: [...]
   - Blocked: [...]
   - Next: [...]
   "Continue from here, or start something new?"
4. Wait for user response
```

If no `.logs/` directory exists → run `bash skills/project-monitor/templates/init-logs.sh` first.

---

### Step 1 — UNDERSTAND

```
Trigger: any new request
Specialist: Orchestrator

Actions:
  □ Identify task type (bug / feature / project / other)
  □ Ask clarifying questions (max 3) — what, where, scope, constraints
  □ Confirm understanding with user before moving on
  □ Log to .logs/communications.md:
    ### [DATE TIME] [UNDERSTAND] — [Short Title]
    - Specialist: Orchestrator
    - Summary: [what was clarified]
    - Status: complete
```

---

### Step 2 — BRAINSTORM

```
Trigger: after UNDERSTAND is logged
Specialist: Orchestrator (+ relevant domain specialist if needed)

Actions:
  □ Present exactly 3 options ranked simple → complex:
      🟢 SIMPLE        [description, ~X min]
      🟡 BALANCED      [description, ~X min]
      🔴 COMPREHENSIVE [description, ~X min]
  □ Wait — do NOT proceed until user picks one
  □ Log to .logs/decisions.md:
    ### [DATE TIME] [BRAINSTORM] — [Decision Title]
    - Options presented: Simple / Balanced / Comprehensive
    - Selected: [option]
    - Rationale: [why]

⛔ GATE: no PLAN until user selects an option
```

---

### Step 3 — PLAN

```
Trigger: after user picks BRAINSTORM option
Specialist: Orchestrator + Project Manager (for multi-day work)

Actions:
  □ Break work into numbered tasks (30-60 min each)
  □ List specialists needed per task
  □ Estimate total time
  □ Present plan to user
  □ Wait — do NOT execute until user confirms
  □ Log to .logs/activity.md:
    ### [DATE TIME] [PLAN] — [Plan Title]
    - Tasks: [numbered list]
    - Estimated: [total time]
    - Status: approved

⛔ GATE: no EXECUTE until user confirms plan
```

---

### Step 4 — EXECUTE

```
Trigger: after user approves PLAN
Specialists: as listed in plan (one at a time)

Per task:
  □ Announce: "Here's what I'm about to do: [1-2 lines]"
  □ Execute the task
  □ Show result briefly
  □ Ask: "Good? Next, or adjust?"
  □ Log to .logs/activity.md:
    ### [DATE TIME] [TASK COMPLETE] — [Task Name]
    - Specialist: [who]
    - Summary: [what was done]
    - Status: complete

Per specialist switch:
  □ Write HANDOFF note (2-3 lines):
    HANDOFF → [next specialist]
    Context: [what was done]
    Next: [what they need to do]
    Decision: [relevant option selected]

Per batch (30-60 min):
  □ Checkpoint: show batch summary → "Continue to next batch?"
```

---

### Step 5 — VERIFY

```
Trigger: after all EXECUTE tasks complete
Specialists: Tester + Security Engineer (always both)

Actions:
  □ Run unit tests → log pass/fail count
  □ Run integration tests (if applicable)
  □ Run e2e tests (if applicable)
  □ Security review: OWASP checklist minimum
  □ For auth/payments/data: run adversarial review checklist
  □ Fix all CRITICAL and HIGH issues before proceeding
  □ Log to .logs/issues.md:
    ### [DATE TIME] [VERIFY] — [Feature/Task Name]
    - Tests: [X passed / Y failed]
    - Security: [pass / issues found]
    - Issues fixed: [list]
    - Status: pass

⛔ GATE: VERIFY must be status: pass before SHIP
         User saying "ship it" does NOT bypass this gate
```

---

### Step 6 — SHIP

```
Trigger: VERIFY logged as pass
Specialist: Deployment / DevOps (as needed)

Actions:
  □ Commit / deploy / release
  □ git push origin <branch>  ← mandatory every sprint
  □ Update relevant documentation
  □ Announce completion to user
  □ Log to .logs/activity.md:
    ### [DATE TIME] [SHIP] — [Feature/Task Name]
    - Specialist: Deployment
    - Summary: [what was shipped, where]
    - Status: complete
    - Impact: [low / medium / high]
```

---

### Step 7 — Session Close (always last)

```
Write to .logs/sessions.md:
### [DATE TIME] SESSION_END
- Completed: [list of tasks done this session]
- In progress: [any started but unfinished tasks]
- Blocked: [any open blockers]
- Next: [planned next steps]
- Specialists used: [list]
- KPIs: tasks completed [N], issues found [N], issues fixed [N]
```

---

### Handling User Shortcut Requests

| User says | Correct response |
|---|---|
| "skip this phase" | Acknowledge phase in one sentence, log it as skipped, continue |
| "just do it" | Still confirm approach in one line before executing |
| "ship it" (before VERIFY) | "VERIFY is required first — running tests now" |
| "move faster" | Compress phases verbally but still log each one |
| "YAGNI" | Switch to 🟢 SIMPLE option or reduce scope |
| "simpler" | Switch to 🟢 SIMPLE option |
| "stop" | Pause, summarize current state, ask what to do next |

---

### Blocker Protocol (any phase)

```
🚧 BLOCKER: [what's wrong]
  A) [simple workaround — lowest effort]
  B) [proper fix — takes longer]
  C) [skip for now — document as risk]
Which one?
```

Log the chosen option to `.logs/issues.md` with status `open` until resolved.

---

## The 6-Phase Workflow

Every session follows this flow. All phases are mandatory.

| Phase | What Happens | Logged To |
|---|---|---|
| 1. Understand | Clarify what, where, how big | `.logs/communications.md` |
| 2. Brainstorm | 3 options ranked simple → complex | `.logs/decisions.md` |
| 3. Plan | Break into 30-60 min task batches | `.logs/activity.md` |
| 4. Execute | One task at a time, interactive checkpoints | `.logs/activity.md` |
| 5. Verify | Tests + security review + ≥80% coverage | `.logs/issues.md` |
| 6. Ship | Deploy, git push, document, announce | `.logs/activity.md` |

Options are always presented as:

```
🟢 SIMPLE:        [lowest effort, fastest]
🟡 BALANCED:      [moderate effort, good tradeoffs]
🔴 COMPREHENSIVE: [highest effort, most robust]
```

---

## Three Core Principles

### 1. YAGNI (You Aren't Gonna Need It)

Before building, designing, or planning anything — ask: *"Is this needed RIGHT NOW?"*

| Instead of... | Use... |
|---|---|
| Microservices for an MVP | Monolith first |
| Kubernetes for 3 containers | Docker Compose |
| Custom auth from scratch | NextAuth / Passport |
| Full design system for 3 pages | Pick a UI framework |
| Cache everything upfront | Profile first, then cache bottlenecks |
| Plan for 10M users on day 1 | Build for current scale |

### 2. Token Efficiency

- Load **one specialist at a time** — never all 23
- Handoffs use a **2-3 line summary**, not full history
- Batch tasks into **30-60 min chunks** with checkpoints
- **Confirm approach before generating code** — prevents expensive rewrites
- Log after the action in the **same tool call** — no extra round-trips

### 3. Project Memory

Everything is appended to `.logs/` — decisions, bugs, risks, scope changes, handoffs. Resume any session exactly where you left off. Eight log files, all append-only, all searchable.

---

## The Team — 23 Specialists

### Management & Planning
| Specialist | What They Do | Trigger Words |
|---|---|---|
| **Orchestrator** | Routes every request to the right specialist; enforces all 6 phases | (first to load, always) |
| **Project Manager** | Charter, WBS, risk matrix, PERT estimation, status reports, PRD | project plan, scope, milestone, charter, PRD |
| **Scrum Master** | Sprints, user stories, MoSCoW backlog, ceremonies, velocity | sprint, backlog, user story, retro, agile |
| **Tech Lead** | ADRs, YAGNI gate, code standards, tech stack decisions | architecture, tech stack, refactor, design pattern |

### Architecture & Design
| Specialist | What They Do | Trigger Words |
|---|---|---|
| **System Designer** | High-level topology, NFRs, scalability, data flow, capacity planning | system design, distributed, scalability, NFR, SLA, SLO |
| **Software Architect** | Code structure, DDD, clean/hexagonal architecture, design patterns, module boundaries | clean architecture, DDD, bounded context, CQRS, design pattern |
| **UX Designer** | User flows, wireframes, information architecture, usability, personas | user flow, wireframe, UX, usability, IA |
| **UI Designer** | Design tokens, color, typography, component styling, design systems, anti-slop aesthetic discipline | design tokens, UI, color scheme, typography, dark mode |
| **Motion Designer** | Animation, micro-interactions, transitions, scroll choreography, reduced-motion, motion graphics / React→MP4 video, generative backgrounds | motion design, animation, transition, easing, scroll animation, promo video, generative background |
| **Design Loop** | One-shot design quality via independent fresh-context critics (brief/system/craft) instead of self-review | design loop, gauntlet loop, critic loop, AI slop, review this design |

### Security & Data
| Specialist | What They Do | Trigger Words |
|---|---|---|
| **Security Engineer** | STRIDE threat modeling, auth design, OWASP, compliance (SOC2/HIPAA/PCI-DSS) | threat model, security review, OWASP, auth design |
| **DBA** | Schema design, query optimization, indexes, migrations, backup strategy | database, schema, slow query, migration, index |

### Development
| Specialist | What They Do | Trigger Words |
|---|---|---|
| **Backend Dev** | APIs, services, auth, ORM, business logic, performance | API, endpoint, backend, REST, GraphQL, service |
| **Frontend Dev** | Components, state management, accessibility, responsive design | component, React, Vue, Next, frontend, CSS |
| **Tester** | Unit / integration / e2e tests, QA, bug reports, ≥80% coverage gate | test, unit test, e2e, QA, coverage, bug report |
| **Test Architect** | Risk-based strategy, ATDD/Gherkin, adversarial review, edge case hunting | test strategy, ATDD, adversarial review, edge case |

### Operations
| Specialist | What They Do | Trigger Words |
|---|---|---|
| **Deployment** | Release, rollback, blue-green/canary strategies, environment management | deploy, release, rollback, staging, production |
| **DevOps/DevSecOps** | CI/CD, Docker, K8s, Terraform, Semgrep/Trivy/Checkov scanning, CI monitoring | CI/CD, pipeline, Docker, Kubernetes, security scan |

### Creative & Marketing
| Specialist | What They Do | Trigger Words |
|---|---|---|
| **Creative Intelligence** | 7 ideation frameworks (SCAMPER, Design Thinking, First Principles, etc.) | brainstorm, ideate, design thinking, name ideas |
| **Digital Marketer** | SEO, campaigns, email sequences, GA4 analytics, A/B testing | SEO, campaign, launch, analytics, growth |
| **Copywriter** | Headlines, CTAs, landing pages, UX microcopy, email copy | copy, headline, CTA, landing page, email |
| **Content Marketer** | Blog posts, content calendar, social media, case studies, repurposing chain | blog post, content, social media, newsletter |
| **Project Monitor** | 8 log files, KPIs, status reports, retrospectives, session resumption | status report, KPIs, retro, what did we do |

---

## Pre-Built Workflows

The Orchestrator recognizes these scenarios and uses an optimised fast path:

| Workflow | Duration | Specialists |
|---|---|---|
| 🐛 Bug Fix | 15-60 min | Tech Lead → Backend/Frontend → Tester |
| ✨ New Feature | 1-4 hrs | PM → UX → Tech Lead → DBA → Devs → Tester → Security |
| 🚀 New Project | 2-6 hrs | PM → System Designer → Software Architect → UX → Tech Lead → DBA → Security → all devs → DevOps |
| 📋 Document-First Build | 1-2 hrs planning + execution | PM → Tech Lead → DBA → Security → Scrum → Test Architect |
| 🎨 UX/UI Design | 30-120 min | UX → UI → Motion → Frontend → Copywriter |
| 🌀 Motion & Interaction | 20-90 min | UI → Motion Designer → Frontend Dev (→ Design Loop for hero/video) |
| 🔁 Design Loop | varies (reserve for high-stakes/reusable artifacts) | UI → Design Loop (3 independent critics) → Frontend/builder fixes → re-round |
| 🗄️ Database Design | 15-60 min | DBA → Tech Lead → Backend Dev |
| 🔒 Security Audit | 30-90 min | Security Engineer → DevSecOps → DBA |
| 🔐 Security Review | 20-60 min | Security Engineer → DevSecOps → Backend/Frontend |
| 🔄 Refactor | 30-120 min | Tech Lead → Backend/Frontend → Tester |
| 📝 Documentation | 15-60 min | Tech Lead → relevant specialist |
| 📢 Marketing Launch | 1-3 hrs | Digital Marketer → Copywriter → Content Marketer |
| 💡 Brainstorm/Ideation | 15-45 min | Creative Intelligence → PM or Tech Lead |
| 🧪 Test Strategy | 20-60 min | Test Architect → Tester → Security Engineer |
| 🧬 Change-Spec (existing codebases) | adds 10-30 min to a feature | Tech Lead → Devs → Tester / spec-reviewer |

---

## Project Logging

Eight append-only log files auto-created in `.logs/`:

| File | What Gets Logged |
|---|---|
| `activity.md` | Completed tasks, milestones, skill changes |
| `decisions.md` | Architecture choices, approach selections (mini-ADRs) |
| `issues.md` | Bugs, blockers (with severity and status) |
| `risks.md` | Risks, probability, mitigation, status |
| `corrections.md` | Scope changes, pivots, plan corrections |
| `communications.md` | User preferences, handoffs, inter-skill consultations |
| `sessions.md` | SESSION_START / SESSION_END snapshots |
| `metrics.md` | Sprint/batch KPI snapshots |

### Log Entry Format
```
### [YYYY-MM-DD HH:MM] [CATEGORY] — [Short Title]
- Specialist: [who logged this]
- Summary: [1-2 sentences]
- Status: open | in-progress | resolved
- Impact: low | medium | high | critical
```

### Report Commands
```
"status report"        → Full project status with KPIs
"what did we do?"      → Activity log
"what's broken?"       → Open issues and blockers
"what did we decide?"  → Decision log
"what changed?"        → Plan corrections
"retro"                → Retrospective analysis
"KPIs"                 → Project metrics
```

### Session Resumption
On session start, the Orchestrator reads only the last `SESSION_END` entry from `sessions.md` and asks:
```
📋 Last session summary:
- Completed: [what was done]
- In progress: [what was started]
- Blocked: [any blockers]
- Next: [what was planned]

"Continue from here, or start something new?"
```

---

## KPIs Tracked

| KPI | Formula | Target |
|---|---|---|
| Velocity | Tasks completed per sprint | Stable or increasing |
| Completion Rate | Completed / Planned × 100 | ≥ 80% |
| Bug Rate | Bugs found / Tasks completed | < 0.5 |
| Bug Fix Rate | Bugs fixed / Bugs found × 100 | ≥ 90% |
| Scope Creep | Scope changes / Original tasks × 100 | < 20% |
| Estimation Accuracy | Actual / Estimated time | 0.8 – 1.2 |
| Blocker Duration | Time from open → resolved | < 1 session |
| Security Issue Rate | Security issues / Tasks completed | < 0.2 |
| Rework Rate | Corrections / Completed × 100 | < 15% |
| Coverage Gate | Combined unit + integration % | ≥ 80% |

---

## Document-First Development

For new projects and large features (3+ days of work):

```
PRD → Architecture Doc → Epics & Stories → Implementation
 PM    Tech Lead + DBA +    Scrum Master +     Dev team
   System Designer +         Test Architect
    Software Architect +
      Security Engineer
```

Each artifact is saved to `docs/`, logged as a MILESTONE, and requires user approval before proceeding.

**YAGNI scaling:**
- Small task (< 1 day): skip the chain entirely
- Medium feature: mini-PRD + ADR only
- Large feature / new project: full chain

---

## Change Specs for Existing Codebases

Document-first covers new projects. For code that already exists, CTS works from a spec delta:

```
docs/specs/[capability].md          what the system does now
docs/changes/[change-id]/
  proposal.md                       why, what, impact
  spec-delta.md                     ADDED / MODIFIED / REMOVED requirements
  tasks.md                          the plan, each task naming the scenarios it covers
docs/changes/archive/               shipped changes
```

- **No spec yet?** Write a baseline for only the capability being changed, from what the code does today. The spec grows one capability at a time.
- **The delta is what you approve.** It is confirmed together with the plan, before any code.
- **VERIFY checks code against the delta**: every added or modified scenario has a test, removed behaviour is gone, and nothing changed outside the delta.
- **SHIP merges the delta** into `docs/specs/` and archives the change in the same commit as the code.

Templates and rules: `skills/orchestrator/references/change-spec.md`.

---

## Security Coverage

The **Security Engineer** provides:
- **STRIDE threat modeling** — fast 5-minute threat model or full rigor when needed
- **Auth design decision tree** — API keys / sessions / JWT / mTLS / SSO based on context
- **Auth checklist** — bcrypt/argon2id, MFA, HttpOnly cookies, JWT claim validation, account lockout
- **Authorization patterns** — Simple roles / RBAC / ABAC / ReBAC
- **Security review checklist** — input/output, auth, data, infra
- **Compliance frameworks** — SOC2, PCI-DSS, HIPAA, ISO 27001, NIST, GDPR
- **Incident response template** — Detect → Assess → Contain → Fix → Recover → Learn

The **DevOps/DevSecOps** engineer runs automated scanning:
```bash
semgrep ci --config p/owasp-top-ten    # SAST
trivy fs --severity CRITICAL,HIGH .    # SCA
trivy image --severity CRITICAL,HIGH   # Container scan
checkov -d ./terraform                 # IaC scan
gitleaks detect --source .             # Secrets scan
```

---

## Test Architecture

The **Test Architect** (distinct from the basic Tester) designs the test system:

### Risk-Based Strategy
Score components by Impact + Frequency + Complexity:
- **13-15**: Maximum (unit + integration + e2e + adversarial + load)
- **9-12**: High (unit + integration + e2e)
- **5-8**: Standard (unit + integration)
- **1-4**: Minimal (smoke tests only)

### ATDD / Gherkin
Acceptance criteria written *before* coding — they become the regression suite.

### Adversarial Review
Automatically triggered for auth, payments, and data handling:
- **Input abuse** — SQLi, XSS, command injection, path traversal, type confusion
- **Auth & access abuse** — IDOR, CSRF, expired tokens, privilege escalation
- **Race conditions** — double-submit, TOCTOU, concurrent updates
- **Business logic abuse** — negative quantities, coupon stacking, skipping required steps

### Edge Case Hunter
Systematic discovery across: boundaries, types, time (DST, leap year), state (empty/full/mid-migration), and network (timeout, partial response, retry storm).

---

## Creative Intelligence Suite

7 structured ideation frameworks, matched to the problem:

| Framework | Best For | Time |
|---|---|---|
| Structured Brainstorming | Generating 10+ ideas fast (diverge → cluster → converge) | 5-10 min |
| SCAMPER | Improving existing solutions (Substitute/Combine/Adapt/Modify/Put to use/Eliminate/Reverse) | 5 min |
| Design Thinking | User-centered innovation (Empathize → Define → Ideate → Prototype → Test) | 15-30 min |
| Storytelling (Hero's Journey) | Pitches and product narratives | 10-15 min |
| First Principles | Breaking assumptions, rebuilding from facts | 10 min |
| Problem Reframing | Unsticking hard problems (4 reframe angles) | 5 min |
| Name Generation | Product/feature naming (descriptive → metaphorical → invented → compound) | 5 min |

All sessions score ideas with: **Impact × Confidence / Effort**

---

## Quick Command Reference

| Say this | What it does |
|---|---|
| `"simpler"` | Switch to a less complex approach |
| `"YAGNI"` | Remind to keep it simple |
| `"option A/B/C"` | Pick from presented options |
| `"good, next"` | Approve current step, move on |
| `"skip this"` | Jump to next task |
| `"go back"` | Revisit a previous decision |
| `"stop"` | Pause and discuss |
| `"what's the plan?"` | Show current batch/task list |
| `"ship it"` | Move to deployment |
| `"test this"` | Run tests on current work |
| `"secure this"` | Run security review |
| `"adversarial review"` | Run adversarial security checklist |
| `"test strategy"` | Design risk-based test plan |
| `"brainstorm this"` | Start creative ideation session |
| `"status report"` | Generate project status with KPIs |
| `"retro"` | Generate retrospective from logs |

### Blocker Protocol
When stuck, specialists never spin — they immediately present:
```
🚧 BLOCKER: [what's wrong]
  A) [simple workaround]
  B) [proper fix]
  C) [skip for now]
Which one?
```

---

## Token Budget by Session Type

| Session Type | Expected Tokens | Skills Loaded |
|---|---|---|
| Quick bug fix | 3-8K | Orchestrator + 1 dev + Tester |
| Small feature | 8-15K | Orchestrator + Tech Lead + 1-2 devs + Tester |
| Large feature | 15-30K | Multiple specialists across batches |
| New project scaffold | 15-25K | PM + System Designer + Software Architect + Tech Lead + DBA + devs + DevOps |
| Database design | 5-10K | DBA + Backend Dev |
| UX/UI design | 5-12K | UX + UI + Frontend + Copywriter |
| Design loop (per critic round) | 3-6K in-app / ~2-3M tokens for a full multi-round external run (e.g. Claude Design + exported assets) | Design Loop + 3 fresh critic subagents |
| Security audit | 5-15K | Security Eng + DevSecOps + references |
| Brainstorm session | 3-8K | Creative Intelligence + PM or Tech Lead |
| Test strategy | 5-10K | Test Architect + Tester + Security Eng |
| Document-first build | 10-20K | PM + Tech Lead + Scrum + devs |
| Sprint planning | 3-8K | PM + Scrum Master |

---

## Customization

**Edit `CLAUDE.md`** — Add your tech stack, naming conventions, deployment URLs, team contacts, and project-specific rules.

**Disable unused skills** — Remove rows from the skill locations table in `CLAUDE.md`. Backend-only project? Remove `frontend-dev`, `copywriter`, `content-marketer`, `digital-marketer`.

**Add new specialists** — Create `skills/your-skill/SKILL.md` with:
1. YAML frontmatter: `name` + `description` + trigger words
2. Role definition
3. Key templates / checklists
4. Handoff points to other specialists

Then add the skill to the Orchestrator's routing table and the `CLAUDE.md` skill locations table.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Claude doesn't use skills | Ensure `CLAUDE.md` is in the project root |
| Wrong specialist loaded | Say `"switch to [specialist]"` or describe the task more specifically |
| Logs not created | Run `bash skills/project-monitor/templates/init-logs.sh` |
| Session not resuming | Check `.logs/sessions.md` for `SESSION_END` entries |
| Too many tokens used | Say `"YAGNI"` or `"simpler"` to reduce scope |
| Skill not triggering | Check the trigger words in the skill's `SKILL.md` frontmatter |

**Commit message convention:** `type(scope): description` — e.g. `feat(auth): add refresh token rotation`

**Branch naming:** `type/short-description` — e.g. `feature/add-auth`, `fix/login-bug`

---

## Intentional Trade-offs (vs BMAD Method)

CTS skips these BMAD features by design to stay **lightweight and zero-dependency**:

| BMAD Feature Skipped | Why |
|---|---|
| NPM installer | CTS is zero-dependency — copy markdown, no Node.js |
| Per-IDE installers (10+) | Built for Claude Code; other agents get one generated `AGENTS.md` and an optional git pre-push gate |
| Named agent personas | Role-based skills use fewer tokens and are easier to maintain |
| Party Mode (multi-agent debate) | Sequential handoffs save ~70% tokens |
| Modular expansion packs | Single bundle — one download, everything included |
| Automatic scale detection | Three explicit depth tracks (Quick / Standard / Full) — proposed in one line, overridable in one word |
| Agent-as-Code (YAML compilation) | Plain markdown — editable in any text editor |
| Web bundles (ChatGPT/Gemini) | Claude Code native — one platform done well |

---

*Claude Team Skills v2.0.0-alpha.1 — 23 specialists, 59 skill files*
