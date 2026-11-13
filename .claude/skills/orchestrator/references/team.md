# The Team

Reference for the orchestrator: who leads each kind of request, how the team fits together, and when to
load each specialist. Read this when routing is not obvious; you do not need it for every request.

## Lead specialist by request type

| Request Type | Primary Specialist | Supporting |
|---|---|---|
| New feature (large) | PM (PRD) → System Designer → Software Architect → Tech Lead → Scrum | UX, DBA, Test Architect, Security |
| New feature (small) | Software Architect → Tech Lead → Backend/Frontend | Tester |
| Bug fix | Tech Lead → Backend or Frontend | Tester |
| New project | PM (PRD) → System Designer → Software Architect → Tech Lead → Scrum | UX, DBA, Security, DevOps |
| Sprint planning | Scrum Master → PM | Tech Lead |
| Deployment issue | DevOps/DevSecOps | Deployment, Tech Lead |
| Database work | DBA | Backend Dev, Tech Lead |
| Security review | Security Engineer | DevSecOps, Test Architect |
| System/infra design | System Designer | Tech Lead, DBA, DevOps |
| Software structure | Software Architect | Tech Lead, Backend Dev |
| UI/UX design | UX Designer → UI Designer | Motion Designer, Frontend Dev, Copywriter, Design Loop (before ship) |
| Motion / animation / transitions / promo video | Motion Designer | UI Designer, Frontend Dev, Design Loop |
| Brainstorm / ideation | Creative Intelligence | PM, Tech Lead, UX |
| Test strategy | Test Architect | Tester, Security Engineer |
| Marketing need | Digital Marketer | Copywriter, Content |
| Content creation | Content Marketer | Copywriter |
| Documentation | Tech Lead | relevant dev specialist |

## Team map

```
                         ┌─────────┐
                         │   PM    │ ← scope, risk, status
                         └────┬────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
        ┌─────┴─────┐   ┌────┴────┐   ┌─────┴─────┐
        │   Scrum   │   │ System  │   │ Security  │ ← threat model
        │  Master   │   │Designer │   │ Engineer  │
        └─────┬─────┘   └────┬────┘   └─────┬─────┘
              │               │               │
              │         ┌─────┴──────┐        │
              │         │  Software  │        │
              │         │ Architect  │        │
              │         └─────┬──────┘        │
              │               │               │
              └───────────────┼───────────────┘
                              │
                       ┌──────┴──────┐
                       │  Tech Lead  │ ← architecture, standards
                       └──────┬──────┘
                              │
          ┌──────┬──────┬─────┼──────┬──────┐
          │      │      │     │      │      │
       ┌──┴──┐┌──┴──┐┌──┴──┐┌┴────┐┌┴────┐┌┴────┐
       │ UX  ││ DBA ││Back-││Front││DevOps││Test │
       │Desgn││     ││end  ││end  ││DevSec││Arch │
       └──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘
          │      │      │      │      │      │
       ┌──┴──┐   │      │      │   ┌──┴──┐   │
       │ UI  │   │      └──┬───┘   │Deploy│  │
       │Desgn│   │         │       └──────┘  │
       └──┬──┘   └────┬────┘                 │
          │           │                      │
       ┌──┴──┐        │                      │
       │Motn │        │                      │  ← animation, transitions, promo video
       │Desgn│        │                      │
       └──┬──┘        │                      │
          └─────┬─────┘                      │
                │                            │
          ┌─────┴─────┐                      │
          │  Tester   │←─────────────────────┘
          └───────────┘  ← tests everything, enforces ≥80% coverage

  ┌────────────────────────────────┐
  │ Digital Marketer → Copywriter  │
  │       ↕            ↕          │ ← marketing team (activates post-ship)
  │ Content Marketer              │
  └────────────────────────────────┘
```

**Flow direction**: PM defines scope → System Designer designs topology + NFRs → Software Architect designs internal structure → Scrum breaks into sprints → Tech Lead sets standards → specialists build → Tester verifies (≥80% coverage gate) → Deployment ships → git push → video recording at version completion. Security Engineer reviews at design and verification. Marketing team activates after ship.

## When to load each specialist

When you need a specialist, read ONLY that skill's SKILL.md:

| Specialist | Skill Path | Load When |
|---|---|---|
| Project Manager | `project-manager/SKILL.md` | Project initiation, scope, stakeholders, risk |
| Scrum Master | `scrum-master/SKILL.md` | Sprint planning, backlog, ceremonies, velocity |
| System Designer | `system-designer/SKILL.md` | High-level topology, NFRs, scalability, distributed systems, data flow |
| Software Architect | `software-architect/SKILL.md` | Code structure, design patterns, DDD, module boundaries, architectural fitness |
| Tech Lead | `tech-lead/SKILL.md` | Tech stack decisions, code review standards, ADRs, technical direction |
| Security Engineer | `security-engineer/SKILL.md` | Threat modeling, auth design, compliance, security architecture |
| DBA | `dba/SKILL.md` | Schema design, queries, migrations, indexes, database ops |
| UX Designer | `ux-designer/SKILL.md` | User flows, wireframes, IA, usability, interaction design |
| UI Designer | `ui-designer/SKILL.md` | Visual design, design tokens, color, typography, component styling |
| Motion Designer | `motion-designer/SKILL.md` | Animation, micro-interactions, transitions, scroll choreography, reduced-motion strategy, motion graphics / React→MP4 video, generative background visuals |
| Design Loop | `design-loop/SKILL.md` | Before shipping any high-stakes UI/graphic — runs independent fresh-context critics (brief/system/craft) instead of self-review |
| Backend Dev | `backend-dev/SKILL.md` | APIs, server logic, microservices |
| Frontend Dev | `frontend-dev/SKILL.md` | UI components, state management, accessibility |
| Tester | `tester/SKILL.md` | Unit/integration/e2e tests, QA checklists, coverage enforcement |
| Test Architect | `test-architect/SKILL.md` | Test strategy, ATDD, adversarial review, edge case hunting, release gates |
| Deployment | `deployment/SKILL.md` | Release process, rollback, environments |
| DevOps/DevSecOps | `devops-devsecops/SKILL.md` | CI/CD, infra, security scanning, hardening |
| Creative Intelligence | `creative-intelligence/SKILL.md` | Brainstorming, design thinking, storytelling, innovation |
| Digital Marketer | `digital-marketer/SKILL.md` | SEO, campaigns, analytics, growth |
| Copywriter | `copywriter/SKILL.md` | Ad copy, emails, landing pages, CTAs |
| Content Marketer | `content-marketer/SKILL.md` | Blog posts, social media, content strategy |
| Project Monitor | `project-monitor/SKILL.md` | Logging, KPIs, status reports, retrospectives, session resumption |
