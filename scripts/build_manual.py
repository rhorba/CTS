"""Build claude-team-skills-user-manual.docx from project source of truth."""

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

from pathlib import Path

OUT = str(Path(__file__).resolve().parent.parent / "claude-team-skills-user-manual.docx")

doc = Document()

# ── Page setup ────────────────────────────────────────────────────────────────
section = doc.sections[0]
section.page_width  = Inches(8.5)
section.page_height = Inches(11)
section.left_margin = section.right_margin = Inches(1.0)
section.top_margin  = section.bottom_margin = Inches(1.0)

PURPLE     = RGBColor(0x6B, 0x4E, 0xFF)
DARK       = RGBColor(0x1A, 0x1A, 0x2E)
MID_GRAY   = RGBColor(0x55, 0x55, 0x66)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_BG   = RGBColor(0xF5, 0xF5, 0xF7)


# ── Style helpers ─────────────────────────────────────────────────────────────

def set_font(run, size=11, bold=False, color=None, italic=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color


def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after  = Pt(6)
    run = p.add_run(text)
    set_font(run, 22, bold=True, color=PURPLE)
    return p


def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    set_font(run, 15, bold=True, color=DARK)
    return p


def h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(2)
    run = p.add_run(text)
    set_font(run, 12, bold=True, color=PURPLE)
    return p


def body(text, size=11, color=None, italic=False, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    set_font(run, size, color=color or DARK, italic=italic)
    return p


def bullet(text, level=0, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.25 + level * 0.25)
    p.paragraph_format.space_after = Pt(2)
    if bold_prefix:
        run = p.add_run(bold_prefix)
        set_font(run, 11, bold=True, color=DARK)
        run2 = p.add_run(text)
        set_font(run2, 11, color=DARK)
    else:
        run = p.add_run(text)
        set_font(run, 11, color=DARK)
    return p


def code_block(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Inches(0.3)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)
    run.font.color.rgb = DARK
    return p


def rule():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '6B4EFF')
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def page_break():
    doc.add_page_break()


def add_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    # header row
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.paragraphs[0].clear()
        p = cell.paragraphs[0]
        run = p.add_run(h)
        set_font(run, 10, bold=True, color=WHITE)
        cell._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:fill'), '6B4EFF')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:val'), 'clear')
        cell._tc.tcPr.append(shd)
    # data rows
    for ri, row_data in enumerate(rows):
        row = table.rows[ri + 1]
        for ci, cell_text in enumerate(row_data):
            cell = row.cells[ci]
            cell.paragraphs[0].clear()
            p = cell.paragraphs[0]
            run = p.add_run(str(cell_text))
            set_font(run, 10, color=DARK)
            if ri % 2 == 0:
                shd = OxmlElement('w:shd')
                shd.set(qn('w:fill'), 'F5F5F7')
                shd.set(qn('w:color'), 'auto')
                shd.set(qn('w:val'), 'clear')
                cell._tc.get_or_add_tcPr().append(shd)
    if col_widths:
        for ri, row in enumerate(table.rows):
            for ci, cell in enumerate(row.cells):
                cell.width = Inches(col_widths[ci])
    doc.add_paragraph()
    return table


# =============================================================================
# COVER PAGE
# =============================================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(60)
run = p.add_run("Claude Team Skills")
set_font(run, 36, bold=True, color=PURPLE)

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
run2 = p2.add_run("User Manual")
set_font(run2, 24, bold=False, color=DARK)

p3 = doc.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
run3 = p3.add_run("23 AI Specialists. One Team. Zero Dependencies.")
set_font(run3, 14, italic=True, color=MID_GRAY)

doc.add_paragraph()

meta = [
    ("Version",   "2.0.0-beta.1"),
    ("License",   "MIT"),
    ("Platform",  "Claude Code"),
    ("Specialists", "23"),
    ("Files",     "59 markdown skill files"),
    ("Total lines", "10,754"),
]
for label, value in meta:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(f"{label}: ")
    set_font(r1, 11, bold=True, color=MID_GRAY)
    r2 = p.add_run(value)
    set_font(r2, 11, color=DARK)

page_break()


# =============================================================================
# CHAPTER 1 — INTRODUCTION
# =============================================================================
h1("1. Introduction")
rule()
body(
    "Claude Team Skills (CTS) is a collection of 23 interconnected specialist skills for Claude Code. "
    "Instead of a generic AI assistant, every task is handled by the right expert — Project Manager, "
    "Security Engineer, DBA, Software Architect, Test Architect, and more — all routed by a central "
    "Orchestrator that loads one specialist at a time."
)
body(
    "CTS is zero-dependency: plain markdown files, no Node.js, no npm, no build step. "
    "Copy the skills/ folder, add CLAUDE.md to your project root, and start working."
)

h2("1.1 Core Design Principles")
principles = [
    ("YAGNI", "You Aren't Gonna Need It. Before building, designing, or planning anything, "
               "ask: \"Is this needed RIGHT NOW?\" Default to the simplest approach."),
    ("Token Efficiency", "Load one specialist at a time. Handoffs use 2-3 line summaries. "
                          "~3-5K tokens for routing vs 35K+ if all skills loaded at once."),
    ("Project Memory", "Eight append-only log files in .logs/. Resume any session exactly where "
                        "you left off. Decisions, bugs, and risks never disappear."),
    ("Strict Process", "6 mandatory phases with hard gates. VERIFY before SHIP — always. "
                        "CI must be green. >=80% test coverage enforced."),
]
for name, desc in principles:
    bullet(f" {desc}", bold_prefix=f"{name}: ")

h2("1.2 What's Included")
add_table(
    ["File / Directory", "Description"],
    [
        ["claude-team-skills/", "The plugin: skills/, agents/, hooks/, evals/, templates/"],
        ["claude-team-skills/skills/", "23 skill directories — each with SKILL.md and a references/ deep-dive file"],
        ["claude-team-skills/agents/", "implementer, spec-reviewer, quality-reviewer"],
        ["claude-team-skills/hooks/", "session-start, push-gate, session-end (POSIX shell)"],
        ["claude-team-skills/evals/", "Four behavioural eval cases and their recorded results"],
        ["claude-team-skills/templates/CLAUDE.md", "Entry point for a copy install — copy to your project root"],
        ["claude-team-skills/templates/AGENTS.md", "Generated entry point for other coding agents"],
        ["claude-team-skills/QUICKSTART.md", "Cheat sheet for ongoing use"],
        ["claude-team-skills/INSTALL.md", "Detailed installation and FAQ"],
        ["scripts/validate-skills.py", "CI validation: manifests, 23 skills, 3 agents, and specialist counts in docs"],
        ["scripts/sync-skills.py", "Mirrors the skills into .claude/skills; CI fails on drift"],
        ["scripts/build-agents-md.py", "Generates templates/AGENTS.md from the skill frontmatter"],
        ["scripts/build_pitch.py", "Regenerates the pitch deck PPTX"],
        ["scripts/build_manual.py", "Regenerates this user manual"],
        ["scripts/build_comparison.py", "Regenerates the comparison PDF"],
        ["cts-comparison.pdf", "CTS beside five agent-workflow frameworks"],
        ["claude-team-skills-pitch.pptx", "14-slide pitch deck for teams and stakeholders"],
        ["claude-team-skills-user-manual.docx", "This document"],
    ],
    col_widths=[2.5, 4.0]
)

h2("1.3 What's New in Version 2")
body("Version 2 backs the rules of version 1 with code, and scales the process to the size of the request.")
add_table(
    ["Capability", "Version 1.1", "Version 2"],
    [
        ["Install", "Copy markdown files", "One-command Claude Code plugin, or copy"],
        ["Ship gate", "A written rule", "A hook blocks git push until VERIFY and coverage are logged"],
        ["Session memory", "Read on request", "Hooks load the last summary and close unfinished sessions"],
        ["Execution", "One context", "A fresh implementer subagent per code task"],
        ["Code review", "Self-review", "Spec review, then quality review, both read-only"],
        ["Small requests", "Full ceremony", "Quick track: one specialist, one log entry"],
        ["Existing codebases", "Document-first only", "Change-spec workflow with spec deltas"],
        ["Other agents", "Claude Code only", "Generated AGENTS.md and an optional git pre-push gate"],
        ["Evidence", "Structure checks", "Behavioural evals: 3 of 4 cases pass (evals/README.md)"],
    ],
    col_widths=[1.5, 1.7, 3.3]
)
body(
    "Depth tracks: Quick (one question or small change, answered by one specialist), Standard (the full "
    "six-phase flow with two user gates), and Full (Standard plus the document chain and subagent execution). "
    "All six phases are logged on every track. Auth, payments, data migrations and requests to ship are never Quick."
)

page_break()


# =============================================================================
# CHAPTER 2 — INSTALLATION
# =============================================================================
h1("2. Installation")
rule()

h2("Option A — Install as a plugin (recommended)")
body("In a Claude Code session:")
code_block("/plugin marketplace add rhorba/CTS\n/plugin install cts@rhorba-cts")
body(
    "The 23 specialists load as plugin skills (cts:orchestrator, cts:tester, ...), together with three agents "
    "and three hooks. Nothing is copied into your project. The hooks are POSIX shell; on Windows they need Git Bash."
)

h2("Option B — Copy the files")
body("Hooks and agents are not included with this option. Follow the four steps below.")

h2("Step 1 — Copy the skills/ folder")
body("Copy claude-team-skills/skills/ into your project root as skills/:")
code_block(
    "your-project/\n"
    "  skills/\n"
    "    orchestrator/\n"
    "    project-manager/\n"
    "    scrum-master/\n"
    "    system-designer/\n"
    "    software-architect/\n"
    "    tech-lead/\n"
    "    security-engineer/\n"
    "    dba/\n"
    "    ux-designer/\n"
    "    ui-designer/          <- design tokens, anti-slop aesthetic guide\n"
    "    motion-designer/      <- motion system + video pipeline, generative visuals\n"
    "    design-loop/          <- independent fresh-context design critics\n"
    "    backend-dev/\n"
    "    frontend-dev/\n"
    "    tester/\n"
    "    test-architect/\n"
    "    deployment/\n"
    "    devops-devsecops/    <- 5 deep-dive security references\n"
    "    creative-intelligence/\n"
    "    digital-marketer/\n"
    "    copywriter/\n"
    "    content-marketer/\n"
    "    project-monitor/     <- templates: init-logs.sh, generate-report.py\n"
    "  CLAUDE.md              <- copy this to project root\n"
    "  QUICKSTART.md\n"
    "  .logs/                 <- auto-created on first session"
)

h2("Step 2 — Add CLAUDE.md to your project root")
body(
    "Copy claude-team-skills/templates/CLAUDE.md to your project root. Claude Code reads it on every session start and loads the Orchestrator. "
    "It contains 12 strict framework rules, the skill locations table, commit conventions, and env var guidance."
)

h2("Step 3 — Initialize logs (optional)")
body("If you want to pre-create the .logs/ directory with all 8 log files:")
code_block("bash skills/project-monitor/templates/init-logs.sh")

h2("Step 4 — Start working")
body("Open Claude Code and describe what you need. Examples:")
for ex in [
    '"I need to add user authentication"',
    '"There\'s a 500 error on the login endpoint"',
    '"Set up a CI/CD pipeline with security scanning"',
    '"Write a launch blog post for our new feature"',
    '"Design the schema for a multi-tenant SaaS app"',
    '"Run a security review before we ship"',
]:
    bullet(ex)

h2("Customization")
bullet("Edit CLAUDE.md — add your tech stack, naming conventions, deployment URLs.")
bullet("Disable unused skills — remove rows from the skill locations table in CLAUDE.md.")
bullet("Add new specialists — create skills/your-skill/SKILL.md with name, description, triggers, "
       "role definition, templates, and handoff points.")

page_break()


# =============================================================================
# CHAPTER 3 — THE 6-PHASE WORKFLOW
# =============================================================================
h1("3. The 6-Phase Workflow")
rule()
body(
    "Every session follows this flow. All 6 phases are MANDATORY. Phases cannot be skipped, merged, "
    "or abbreviated. Hard gates enforce user confirmation before PLAN and EXECUTE start, "
    "and before SHIP is allowed."
)

phases = [
    ("Phase 1 — UNDERSTAND", "communications.md",
     "Clarify: what, where, how big, who is affected. Ask up to 3 focused questions — no assumptions. "
     "Identify all env vars needed. Collect values before EXECUTE.",
     []),
    ("Phase 2 — BRAINSTORM", "decisions.md",
     "Present exactly 3 options ranked simple to complex:",
     [
         "🟢 SIMPLE — lowest effort, fastest",
         "🟡 BALANCED — moderate effort, good tradeoffs",
         "🔴 COMPREHENSIVE — highest effort, most robust",
     ]),
    ("Phase 3 — PLAN", "activity.md",
     "Break work into numbered tasks (30-60 min each). List specialists needed per task. "
     "Estimate total time. Wait for user confirmation — do NOT execute until confirmed.",
     []),
    ("Phase 4 — EXECUTE", "activity.md",
     "One task at a time. Announce what you're about to do (1-2 lines). Show result after each. "
     "Write a HANDOFF note on every specialist switch. Checkpoint after each 30-60 min batch.",
     []),
    ("Phase 5 — VERIFY", "issues.md",
     "Run tests (unit + integration + e2e). Run OWASP security checklist minimum. "
     "Fix all CRITICAL and HIGH issues before proceeding. Coverage gate: >=80% combined unit + integration.",
     []),
    ("Phase 6 — SHIP", "activity.md",
     "Commit, deploy, git push (mandatory every sprint). Update documentation. "
     "CI must be green — no exceptions. Log SHIP milestone.",
     []),
]
for title, log, desc, subitems in phases:
    h2(title)
    p = doc.add_paragraph()
    r1 = p.add_run("Logs to: ")
    set_font(r1, 10, bold=True, color=MID_GRAY)
    r2 = p.add_run(f".logs/{log}")
    r2.font.name = 'Courier New'
    set_font(r2, 10, color=DARK)
    body(desc)
    for item in subitems:
        bullet(item)

h2("Hard Gates")
add_table(
    ["Gate", "Condition", "What happens if skipped"],
    [
        ["BRAINSTORM → PLAN", "User must pick one of 3 options", "Orchestrator waits — never self-proceeds"],
        ["PLAN → EXECUTE", "User must confirm the task plan", "No code generated until confirmed"],
        ["VERIFY → SHIP", "Tests pass + security check pass + >=80% coverage", "SHIP is blocked even if user says \"ship it\""],
    ],
    col_widths=[1.8, 2.5, 2.2]
)

h2("Handling Shortcut Requests")
add_table(
    ["User says", "Correct response"],
    [
        ['"skip this phase"', "Acknowledge in one sentence, log it as skipped, continue"],
        ['"just do it"', "Still confirm approach in one line before executing"],
        ['"ship it" (before VERIFY)', "\"VERIFY is required first — running tests now\""],
        ['"move faster"', "Compress phases verbally but still log each one"],
        ['"YAGNI"', "Switch to 🟢 SIMPLE option or reduce scope"],
        ['"simpler"', "Switch to 🟢 SIMPLE option"],
        ['"stop"', "Pause, summarize current state, ask what to do next"],
    ],
    col_widths=[2.0, 4.5]
)

page_break()


# =============================================================================
# CHAPTER 4 — THE 23 SPECIALISTS
# =============================================================================
h1("4. The 23 Specialists")
rule()
body(
    "Each specialist is a markdown file (SKILL.md) with YAML frontmatter declaring its name, "
    "description, and trigger words. The Orchestrator loads exactly one specialist per task."
)

h2("4.1 Management & Planning")

specialists_mgmt = [
    ("Orchestrator", "orchestrator/SKILL.md",
     "Routes every request to the right specialist. Enforces all 6 phases, written handoffs, "
     "CI monitoring, and coverage gate. Always the first skill loaded.",
     "Any general work request, session start, 'let's work on', 'new feature', 'bug fix', 'plan', 'sprint'"),
    ("Project Manager", "project-manager/SKILL.md",
     "Project charter, WBS, risk matrix (H/M/L probability x impact), PERT estimation, "
     "status reports (Green/Amber/Red), change management, PRD in document-first chain.",
     "'project plan', 'scope', 'timeline', 'milestone', 'stakeholder', 'WBS', 'charter', 'PRD'"),
    ("Scrum Master", "scrum-master/SKILL.md",
     "Sprint planning, user stories (Given/When/Then), MoSCoW prioritization, story points (1-13 Fibonacci), "
     "retrospectives, velocity tracking. Solo dev = skip ceremonies.",
     "'sprint', 'backlog', 'user story', 'acceptance criteria', 'velocity', 'retro', 'agile'"),
    ("Tech Lead", "tech-lead/SKILL.md",
     "Architecture Decision Records (ADRs), YAGNI gate, code standards (SOLID/DRY/KISS), "
     "tech stack decisions, project structure templates, technical debt triage.",
     "'architecture', 'tech stack', 'code review', 'technical debt', 'refactor', 'design pattern'"),
]

for name, path, desc, triggers in specialists_mgmt:
    h3(name)
    p = doc.add_paragraph()
    r1 = p.add_run("File: ")
    set_font(r1, 10, bold=True, color=MID_GRAY)
    r2 = p.add_run(path)
    r2.font.name = 'Courier New'
    set_font(r2, 10, color=DARK)
    body(desc)
    p2 = doc.add_paragraph()
    r3 = p2.add_run("Trigger words: ")
    set_font(r3, 10, bold=True, color=MID_GRAY)
    r4 = p2.add_run(triggers)
    set_font(r4, 10, italic=True, color=DARK)

h2("4.2 Architecture & Design")

specialists_arch = [
    ("System Designer", "system-designer/SKILL.md",
     "High-level topology (clients -> CDN/WAF -> LB -> API Gateway -> services -> DB -> observability), "
     "NFR capture (availability, latency p99, throughput RPS, RTO/RPO), scalability patterns, "
     "capacity estimation, integration patterns (REST/Webhooks/Queue/Event Bus/gRPC/GraphQL), "
     "System Design Decision Records (SDR).",
     "'system design', 'distributed', 'scalability', 'capacity', 'NFR', 'SLA', 'SLO', 'message queue', 'load balancer'"),
    ("Software Architect", "software-architect/SKILL.md",
     "Architecture style selector (MVC/Layered -> Clean -> Hexagonal -> DDD -> CQRS -> Event Sourcing), "
     "module boundaries, dependency rules, design patterns (8 patterns), DDD (bounded contexts, aggregates, "
     "value objects, domain events), architectural fitness functions (>=80% coverage, 0 dependency cycles).",
     "'clean architecture', 'hexagonal', 'DDD', 'bounded context', 'CQRS', 'event sourcing', 'design pattern', 'coupling'"),
    ("UX Designer", "ux-designer/SKILL.md",
     "3-tier process (Lightweight 30min / Standard 2-4h / Full days), quick personas, user flow notation "
     "(happy path + error paths + edge cases), wireframe screen state checklist (empty/loading/loaded/error), "
     "information architecture, Nielsen's 10 heuristics quick-check.",
     "'user flow', 'wireframe', 'persona', 'UX', 'usability', 'IA', 'navigation', 'interaction design'"),
    ("UI Designer", "ui-designer/SKILL.md",
     "Design token system (semantic colors, typography scale 12px-36px, 4px spacing grid, border radius scale), "
     "component patterns (4 button types + 6 states, form rules, card structure), 12/8/4 column grid "
     "(desktop/tablet/mobile), dark mode rules, visual hierarchy checklist, 44x44px touch targets. "
     "Anti-slop aesthetic discipline: name the aesthetic + mix 3 references + write the out-of-bounds "
     "list before the first render.",
     "'UI design', 'color palette', 'typography', 'design tokens', 'component library', 'dark mode', 'design system'"),
    ("Motion Designer", "motion-designer/SKILL.md",
     "Motion token system (duration scale 0-480ms, easing curves, choreography/stagger, named interaction "
     "inventory), hard rules (nothing blocking > 400ms, prefers-reduced-motion, compositor-only props), "
     "scroll reveals / parallax / view transitions, motion graphics via React->MP4 (Remotion-style "
     "render->review->fix loop), generative/procedural hero visuals. Delivers a Motion Spec table to Frontend Dev.",
     "'motion design', 'animation', 'micro-interaction', 'transition', 'easing', 'scroll animation', 'promo video', 'generative background'"),
    ("Design Loop", "design-loop/SKILL.md",
     "One-shot design quality via independent fresh-context critics instead of self-review. Step 0 design "
     "system first, then three critics (Brief / System / Craft) that see only the rendered artifact + brief + "
     "tokens, each returning pass/fail + a numbered concrete fix list. Re-round with fresh context until all "
     "pass or issues stop surfacing. YAGNI-gated to high-stakes / reusable artifacts.",
     "'design loop', 'gauntlet loop', 'critic loop', 'AI slop', 'review this design', 'does this look AI-generated'"),
]
for name, path, desc, triggers in specialists_arch:
    h3(name)
    p = doc.add_paragraph()
    r1 = p.add_run("File: ")
    set_font(r1, 10, bold=True, color=MID_GRAY)
    r2 = p.add_run(path)
    r2.font.name = 'Courier New'
    set_font(r2, 10, color=DARK)
    body(desc)
    p2 = doc.add_paragraph()
    r3 = p2.add_run("Trigger words: ")
    set_font(r3, 10, bold=True, color=MID_GRAY)
    r4 = p2.add_run(triggers)
    set_font(r4, 10, italic=True, color=DARK)

h2("4.3 Security & Data")

specialists_sec = [
    ("Security Engineer", "security-engineer/SKILL.md",
     "5-minute STRIDE threat model, auth decision tree (Public API / User app / Service-to-service / Admin / IoT), "
     "auth checklist (bcrypt/argon2id, MFA, HttpOnly cookies, JWT validation, account lockout), "
     "authorization patterns (Simple / RBAC / ABAC / ReBAC), incident response template "
     "(DETECT->ASSESS->CONTAIN->FIX->RECOVER->LEARN), compliance: SOC2, PCI-DSS, HIPAA, ISO 27001, NIST, GDPR.",
     "'security review', 'threat model', 'OWASP', 'auth design', 'encryption', 'zero trust', 'compliance'"),
    ("DBA", "dba/SKILL.md",
     "Database selection (default: PostgreSQL), schema design (entities -> relationships -> tables), "
     "naming conventions, normalization (always 1NF/2NF/3NF), 4 PostgreSQL index types (B-tree/Hash/GIN/GiST) "
     "with SQL, query optimization (EXPLAIN ANALYZE, red flags), migration rules (5 rules, forward-only in prod), "
     "performance fixes ordered by effort, backup strategy (pg_dump daily, WAL continuous, cloud snapshots).",
     "'database', 'schema', 'migration', 'slow query', 'index', 'PostgreSQL', 'MongoDB', 'Redis', 'sharding'"),
]
for name, path, desc, triggers in specialists_sec:
    h3(name)
    p = doc.add_paragraph()
    r1 = p.add_run("File: ")
    set_font(r1, 10, bold=True, color=MID_GRAY)
    r2 = p.add_run(path)
    r2.font.name = 'Courier New'
    set_font(r2, 10, color=DARK)
    body(desc)
    p2 = doc.add_paragraph()
    r3 = p2.add_run("Trigger words: ")
    set_font(r3, 10, bold=True, color=MID_GRAY)
    r4 = p2.add_run(triggers)
    set_font(r4, 10, italic=True, color=DARK)

page_break()

h2("4.4 Development")

specialists_dev = [
    ("Backend Dev", "backend-dev/SKILL.md",
     "API design checklist (RESTful naming, consistent response format, validation, status codes, "
     "pagination, rate limiting, versioning), service layer pattern (Route->Controller->Service->Repository->DB), "
     "error handling, auth flow, performance checklist (N+1 prevention, pooling, caching, async, bulk ops).",
     "'API', 'endpoint', 'backend', 'REST', 'GraphQL', 'service', 'middleware', 'auth', 'ORM', 'queue', 'cache'"),
    ("Frontend Dev", "frontend-dev/SKILL.md",
     "Component design rules (single responsibility, props down/events up, composition, a11y, mobile-first), "
     "state management decision table (local/lift/global store/query cache/URL params/form library), "
     "accessibility checklist (7 items), breakpoints (sm:640/md:768/lg:1024/xl:1280).",
     "'component', 'React', 'Vue', 'Next', 'Svelte', 'frontend', 'CSS', 'Tailwind', 'accessibility', 'responsive'"),
    ("Tester", "tester/SKILL.md",
     "Testing pyramid (many unit / some integration / few e2e), 80% combined coverage gate (hard non-negotiable), "
     "AAA pattern (Arrange/Act/Assert), test plan format, bug report format (severity/steps/expected/actual/evidence), "
     "framework quick reference (Jest/pytest/Cypress/Playwright/Go testing).",
     "'test', 'unit test', 'e2e', 'coverage', 'QA', 'bug report', 'regression', 'TDD', 'BDD'"),
    ("Test Architect", "test-architect/SKILL.md",
     "Risk-based strategy (score impact+frequency+complexity -> max/high/standard/minimal tiers), "
     "ATDD workflow (DISCOVER->FORMULATE->AUTOMATE->DEVELOP->REVIEW), Gherkin acceptance scenarios "
     "(with Scenario Outline for boundaries), adversarial review checklist (input abuse, auth abuse, "
     "race conditions, business logic abuse), edge case hunter (boundaries/types/time/state/network), "
     "traceability matrix, release gate criteria.",
     "'test strategy', 'ATDD', 'adversarial review', 'edge case', 'risk-based', 'release gate', 'quality gate'"),
]
for name, path, desc, triggers in specialists_dev:
    h3(name)
    p = doc.add_paragraph()
    r1 = p.add_run("File: ")
    set_font(r1, 10, bold=True, color=MID_GRAY)
    r2 = p.add_run(path)
    r2.font.name = 'Courier New'
    set_font(r2, 10, color=DARK)
    body(desc)
    p2 = doc.add_paragraph()
    r3 = p2.add_run("Trigger words: ")
    set_font(r3, 10, bold=True, color=MID_GRAY)
    r4 = p2.add_run(triggers)
    set_font(r4, 10, italic=True, color=DARK)

h2("4.5 Operations")

specialists_ops = [
    ("Deployment", "deployment/SKILL.md",
     "Pre-deployment checklist (code/infrastructure/rollback/monitoring), deployment strategies "
     "(Rolling/Blue-Green/Canary/Recreate/Feature Flags), blue-green and rolling procedures with bash, "
     "environment management (local->dev->staging->production), CI green gate (mandatory — rollback immediately "
     "if post-deploy check fails).",
     "'deploy', 'release', 'rollback', 'staging', 'production', 'Vercel', 'Netlify', 'AWS', 'blue-green', 'canary'"),
    ("DevOps / DevSecOps", "devops-devsecops/SKILL.md",
     "GitHub Actions CI/CD pipeline template (lint-test, security, build jobs), hardened Dockerfile "
     "(multi-stage, non-root user, healthcheck), Docker Compose dev template, Terraform starter, "
     "monitoring stack (Prometheus/Grafana/Loki/Jaeger/Sentry + 6 essential alerts), security scanning "
     "(Semgrep SAST, Trivy SCA + container, Checkov IaC, Gitleaks secrets), CI monitoring protocol "
     "(watch every push — red = stop all work, fix first).\n"
     "5 reference files: cicd-security.md, cloud-security.md, code-security.md, "
     "container-k8s-security.md, threat-model-compliance.md.",
     "'CI/CD', 'pipeline', 'Docker', 'Kubernetes', 'Terraform', 'Semgrep', 'Trivy', 'monitoring', 'DevOps'"),
]
for name, path, desc, triggers in specialists_ops:
    h3(name)
    p = doc.add_paragraph()
    r1 = p.add_run("File: ")
    set_font(r1, 10, bold=True, color=MID_GRAY)
    r2 = p.add_run(path)
    r2.font.name = 'Courier New'
    set_font(r2, 10, color=DARK)
    body(desc)
    p2 = doc.add_paragraph()
    r3 = p2.add_run("Trigger words: ")
    set_font(r3, 10, bold=True, color=MID_GRAY)
    r4 = p2.add_run(triggers)
    set_font(r4, 10, italic=True, color=DARK)

page_break()

h2("4.6 Creative & Marketing")

specialists_creative = [
    ("Creative Intelligence", "creative-intelligence/SKILL.md",
     "7 ideation frameworks: Structured Brainstorming (diverge 10+ ideas -> cluster -> converge top 3), "
     "SCAMPER (Substitute/Combine/Adapt/Modify/Put to use/Eliminate/Reverse), Design Thinking "
     "(Empathize->Define->Ideate->Prototype->Test), Storytelling/Hero's Journey for pitches, "
     "First Principles, Problem Reframing (4 angles), Name Generation (descriptive/metaphorical/invented/compound). "
     "All sessions score ideas: Impact x Confidence / Effort.",
     "'brainstorm', 'ideate', 'design thinking', 'SCAMPER', 'name ideas', 'storytelling', 'first principles'"),
    ("Digital Marketer", "digital-marketer/SKILL.md",
     "SEO checklist (technical + on-page per page), marketing funnel "
     "(AWARENESS->INTEREST->CONSIDERATION->CONVERSION->RETENTION->ADVOCACY), campaign planning template, "
     "email 5-sequence template, GA4 minimum events (7 events to track), A/B testing rules "
     "(one variable, 100 conversions min, 2 weeks, 95% significance).",
     "'SEO', 'keyword', 'Google Ads', 'campaign', 'conversion', 'funnel', 'GA4', 'growth', 'A/B test'"),
    ("Copywriter", "copywriter/SKILL.md",
     "Core frameworks (AIDA, PAS, BAB), 5 headline types with templates, CTAs (bad vs good examples), "
     "email subject line rules, landing page 8-section structure, UX microcopy "
     "(error/empty/loading/success states), 7 copy rules (benefits over features, one CTA, active voice, "
     "You>We, specific>vague, cut ruthlessly), tone adaptation (professional/friendly/bold/playful).",
     "'copy', 'headline', 'CTA', 'landing page', 'email subject', 'UX writing', 'microcopy', 'slogan'"),
    ("Content Marketer", "content-marketer/SKILL.md",
     "Content strategy (3-5 content pillars), weekly content calendar table (day/platform/type/topic/pillar/"
     "funnel stage/status), blog post template (title/meta/keyword/hook/H2 sections/takeaways/CTA), "
     "social media templates (LinkedIn post, Twitter/X thread 1-7 structure), case study structure "
     "(challenge/solution/results/quote), 9-item quality checklist, repurposing chain "
     "(blog->LinkedIn->Twitter->email->infographic->video->slides).",
     "'blog post', 'content calendar', 'social media', 'LinkedIn', 'case study', 'content strategy'"),
    ("Project Monitor", "project-monitor/SKILL.md",
     "Manages 8 append-only log files: activity.md, decisions.md, issues.md, risks.md, corrections.md, "
     "communications.md, sessions.md, metrics.md. Tracks 10 KPIs with formulas and targets. "
     "Generates status reports, retrospectives. Session resumption protocol reads only last SESSION_END. "
     "Templates: init-logs.sh (creates all 8 log files), generate-report.py (status report generator).",
     "'status report', 'KPIs', 'retro', 'what did we do', 'log this', 'what issues', 'metrics'"),
]
for name, path, desc, triggers in specialists_creative:
    h3(name)
    p = doc.add_paragraph()
    r1 = p.add_run("File: ")
    set_font(r1, 10, bold=True, color=MID_GRAY)
    r2 = p.add_run(path)
    r2.font.name = 'Courier New'
    set_font(r2, 10, color=DARK)
    body(desc)
    p2 = doc.add_paragraph()
    r3 = p2.add_run("Trigger words: ")
    set_font(r3, 10, bold=True, color=MID_GRAY)
    r4 = p2.add_run(triggers)
    set_font(r4, 10, italic=True, color=DARK)

page_break()


# =============================================================================
# CHAPTER 5 — PRE-BUILT WORKFLOWS
# =============================================================================
h1("5. Pre-Built Workflows")
rule()
body(
    "The Orchestrator recognises 13 common scenarios and uses an optimised fast-path automatically. "
    "Each workflow has a defined duration, specialist sequence, and mandatory checkpoints."
)

add_table(
    ["Workflow", "Duration", "Specialists"],
    [
        ["Bug Fix",             "15-60 min",  "Tech Lead -> Backend/Frontend -> Tester"],
        ["New Feature",         "1-4 hrs",    "PM -> UX -> Tech Lead -> DBA -> Devs -> Tester -> Security Eng"],
        ["New Project",         "2-6 hrs",    "PM -> System Designer -> Software Architect -> UX -> Tech Lead -> DBA -> Security -> all devs -> DevOps"],
        ["Document-First Build","1-2 hrs+",   "PM -> Tech Lead -> DBA -> Security -> Scrum -> Test Architect"],
        ["UX/UI Design",        "30-120 min", "UX Designer -> UI Designer -> Frontend Dev -> Copywriter"],
        ["Database Design",     "15-60 min",  "DBA -> Tech Lead -> Backend Dev"],
        ["Security Audit",      "30-90 min",  "Security Engineer -> DevSecOps -> DBA"],
        ["Security Review",     "20-60 min",  "Security Engineer -> DevSecOps -> Backend/Frontend"],
        ["Refactor",            "30-120 min", "Tech Lead -> Backend/Frontend -> Tester"],
        ["Documentation",       "15-60 min",  "Tech Lead -> relevant specialist"],
        ["Marketing Launch",    "1-3 hrs",    "Digital Marketer -> Copywriter -> Content Marketer"],
        ["Brainstorm/Ideation", "15-45 min",  "Creative Intelligence -> PM or Tech Lead"],
        ["Test Strategy",       "20-60 min",  "Test Architect -> Tester -> Security Engineer"],
    ],
    col_widths=[1.8, 1.0, 3.7]
)

h2("Document-First Development")
body(
    "For new projects and large features (3+ days of work), CTS follows the full document chain "
    "before any code is written:"
)
code_block(
    "PRD  ->  Architecture Doc  ->  Epics & Stories  ->  Implementation\n"
    " PM      Tech Lead + DBA +      Scrum Master +        Dev team\n"
    "         System Designer +       Test Architect\n"
    "          Software Architect +\n"
    "           Security Engineer"
)
body("Each artifact is saved to docs/, logged as a MILESTONE, and requires user approval before proceeding.")
add_table(
    ["Task size", "Document chain"],
    [
        ["Small task (< 1 day)",    "Skip the chain entirely"],
        ["Medium feature",          "Mini-PRD + ADR only"],
        ["Large feature / new project", "Full PRD -> Architecture -> Stories chain"],
    ],
    col_widths=[2.5, 4.0]
)

page_break()


# =============================================================================
# CHAPTER 6 — PROJECT LOGGING
# =============================================================================
h1("6. Project Logging")
rule()
body(
    "CTS maintains 8 append-only log files in .logs/. These are the project's memory — "
    "never overwritten, always appended. Resume any session exactly where you left off."
)

h2("Log Files")
add_table(
    ["File", "What Gets Logged"],
    [
        ["activity.md",       "Completed tasks, milestones, skill changes, git pushes"],
        ["decisions.md",      "Architecture choices, approach selections (mini-ADRs), BRAINSTORM picks"],
        ["issues.md",         "Bugs and blockers with severity (CRITICAL/HIGH/MEDIUM/LOW) and status"],
        ["risks.md",          "Risks with probability, impact, mitigation strategy, and status"],
        ["corrections.md",    "Scope changes, pivots, plan corrections — anything that deviated from plan"],
        ["communications.md", "User preferences, handoffs between specialists, inter-skill consultations"],
        ["sessions.md",       "SESSION_START and SESSION_END snapshots for resumption"],
        ["metrics.md",        "Sprint/batch KPI snapshots — velocity, coverage, bug rate, etc."],
    ],
    col_widths=[1.5, 5.0]
)

h2("Log Entry Format")
code_block(
    "### [YYYY-MM-DD HH:MM] [CATEGORY] -- [Short Title]\n"
    "- Specialist: [who logged this]\n"
    "- Summary: [1-2 sentences]\n"
    "- Status: open | in-progress | resolved\n"
    "- Impact: low | medium | high | critical"
)

h2("The 10 KPIs Tracked")
add_table(
    ["KPI", "Formula", "Target"],
    [
        ["Velocity",             "Tasks completed per sprint",                     "Stable or increasing"],
        ["Completion Rate",      "Completed / Planned x 100",                      ">= 80%"],
        ["Bug Rate",             "Bugs found / Tasks completed",                   "< 0.5"],
        ["Bug Fix Rate",         "Bugs fixed / Bugs found x 100",                  ">= 90%"],
        ["Scope Creep",          "Scope changes / Original tasks x 100",           "< 20%"],
        ["Estimation Accuracy",  "Actual / Estimated time",                        "0.8 - 1.2"],
        ["Blocker Duration",     "Time from open to resolved",                     "< 1 session"],
        ["Security Issue Rate",  "Security issues / Tasks completed",              "< 0.2"],
        ["Rework Rate",          "Corrections / Completed x 100",                  "< 15%"],
        ["Coverage Gate",        "Combined unit + integration coverage %",         ">= 80%"],
    ],
    col_widths=[2.0, 2.5, 1.5]
)

h2("Report Commands")
body("Say any of these during a session:")
add_table(
    ["Command", "Output"],
    [
        ['"status report"',   "Full project status with all 10 KPIs"],
        ['"what did we do?"', "Activity log summary"],
        ['"what\'s broken?"', "Open issues and blockers"],
        ['"what did we decide?"', "Decision log (mini-ADRs)"],
        ['"what changed?"',   "Plan corrections and scope changes"],
        ['"retro"',           "Retrospective analysis from logs"],
        ['"KPIs"',            "Current project metrics"],
    ],
    col_widths=[2.0, 4.5]
)

h2("Session Resumption")
body("On every session start, the Orchestrator reads only the last SESSION_END entry and presents:")
code_block(
    "Last session:\n"
    "  Completed: [what was done]\n"
    "  In progress: [what was started]\n"
    "  Blocked: [any blockers]\n"
    "  Next: [planned next steps]\n\n"
    "Continue from here, or start something new?"
)

page_break()


# =============================================================================
# CHAPTER 7 — SECURITY & QUALITY
# =============================================================================
h1("7. Security & Quality")
rule()

h2("7.1 Security Engineer — Built-In From Design")
body(
    "The Security Engineer is engaged at the DESIGN phase, not after. Security is a gate, "
    "not an afterthought."
)
h3("STRIDE Threat Modeling")
body("5-minute fast model covers: Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation. "
     "Full rigor available via references/owasp-checklist.md for complex systems.")

h3("Authentication Decision Tree")
add_table(
    ["Context", "Recommended Auth"],
    [
        ["Public API (no user context)", "API keys + rate limiting"],
        ["User-facing web app",          "Sessions (HttpOnly cookies) or JWT with refresh tokens"],
        ["Service-to-service",           "mTLS or service account tokens"],
        ["Admin panel",                  "SSO + MFA mandatory"],
        ["IoT / embedded",               "Certificate-based or pre-shared keys"],
    ],
    col_widths=[2.5, 4.0]
)

h3("Compliance Frameworks Covered")
for f in ["SOC 2 Type II", "PCI-DSS", "HIPAA", "ISO 27001", "NIST Cybersecurity Framework", "GDPR"]:
    bullet(f)

h2("7.2 Test Architect — Risk-Based Quality")
h3("Risk Scoring")
body("Score each component: Impact (1-5) + Frequency (1-5) + Complexity (1-5) = total score")
add_table(
    ["Score", "Coverage Level", "Tests Required"],
    [
        ["13-15", "Maximum",  "Unit + integration + e2e + adversarial + load"],
        ["9-12",  "High",     "Unit + integration + e2e"],
        ["5-8",   "Standard", "Unit + integration"],
        ["1-4",   "Minimal",  "Smoke tests only"],
    ],
    col_widths=[1.0, 1.5, 4.0]
)

h3("Adversarial Review Triggers")
body("Automatically triggered for: authentication, payments, data handling, admin operations.")
add_table(
    ["Category", "What's Tested"],
    [
        ["Input abuse",           "SQLi, XSS, command injection, path traversal, type confusion"],
        ["Auth & access abuse",   "IDOR, CSRF, expired tokens, privilege escalation, JWT tampering"],
        ["Race conditions",       "Double-submit, TOCTOU, concurrent update conflicts"],
        ["Business logic abuse",  "Negative quantities, coupon stacking, skipping required steps"],
    ],
    col_widths=[2.0, 4.5]
)

h2("7.3 DevOps/DevSecOps — Automated Scanning")
body("Run on every push via GitHub Actions CI:")
code_block(
    "semgrep ci --config p/owasp-top-ten    # SAST\n"
    "trivy fs --severity CRITICAL,HIGH .    # SCA\n"
    "trivy image --severity CRITICAL,HIGH   # Container scan\n"
    "checkov -d ./terraform                 # IaC scan\n"
    "gitleaks detect --source .             # Secrets scan"
)
body("CI Monitoring Protocol: DevOps/DevSecOps watches every push. CI red = stop all work, "
     "diagnose, fix, re-push, repeat until green. Never mark a task done while CI is red.")

page_break()


# =============================================================================
# CHAPTER 8 — QUICK COMMAND REFERENCE
# =============================================================================
h1("8. Quick Command Reference")
rule()
body("Say any of these during a Claude Code session:")

add_table(
    ["Say this", "What it does"],
    [
        ['"simpler"',          "Switch to 🟢 SIMPLE option"],
        ['"YAGNI"',            "Enforce YAGNI — reduce scope to current need"],
        ['"option A/B/C"',     "Pick from the 3 brainstorm options"],
        ['"good, next"',       "Approve current step and move to the next"],
        ['"skip this"',        "Jump to next task (phase is logged, not erased)"],
        ['"go back"',          "Revisit a previous decision"],
        ['"stop"',             "Pause — summarize state and ask what to do next"],
        ['"what\'s the plan?"',"Show current batch and task list"],
        ['"ship it"',          "Move to SHIP phase (VERIFY must pass first)"],
        ['"test this"',        "Run tests on current work"],
        ['"secure this"',      "Run security review on current work"],
        ['"adversarial review"',"Run full adversarial checklist"],
        ['"test strategy"',    "Design risk-based test plan for the feature"],
        ['"brainstorm this"',  "Start structured creative ideation session"],
        ['"status report"',    "Generate project status with all 10 KPIs"],
        ['"retro"',            "Generate retrospective analysis from logs"],
        ['"KPIs"',             "Show current project metrics"],
        ['"switch to [X]"',    "Load a specific specialist (e.g. 'switch to DBA')"],
    ],
    col_widths=[2.2, 4.3]
)

h2("Blocker Protocol")
body("When stuck, specialists never spin — they immediately present 3 options:")
code_block(
    "BLOCKER: [what's wrong]\n"
    "  A) [simple workaround — lowest effort]\n"
    "  B) [proper fix — takes longer]\n"
    "  C) [skip for now — document as risk]\n"
    "Which one?"
)
body("The chosen option is logged to .logs/issues.md with status 'open' until resolved.")

h2("Handoff Protocol")
body("Every specialist switch requires a written handoff note (2-3 lines):")
code_block(
    "HANDOFF -> [Next Specialist]\n"
    "Context: [1-2 sentence summary of what was done]\n"
    "Need: [what the next specialist should do]\n"
    "Constraints: [decisions already made that must be respected]"
)

page_break()


# =============================================================================
# CHAPTER 9 — TOKEN EFFICIENCY
# =============================================================================
h1("9. Token Efficiency")
rule()
body("CTS is designed to use the minimum tokens needed for each task.")

h2("Load Cost Comparison")
add_table(
    ["Approach", "Token Cost"],
    [
        ["CLAUDE.md + Orchestrator + 1 specialist",     "~3-5K tokens"],
        ["CLAUDE.md + Orchestrator + 1 specialist + 1 reference file", "~6-10K tokens"],
        ["All 23 skills loaded at once",                "~35K+ tokens (wasteful)"],
    ],
    col_widths=[3.5, 3.0]
)

h2("Session Budget by Type")
add_table(
    ["Session Type", "Expected Tokens", "Skills Loaded"],
    [
        ["Quick bug fix",         "3-8K",   "Orchestrator + 1 dev + Tester"],
        ["Small feature",         "8-15K",  "Orchestrator + Tech Lead + 1-2 devs + Tester"],
        ["Large feature",         "15-30K", "Multiple specialists across batches"],
        ["New project scaffold",  "15-25K", "PM + System Designer + Software Architect + Tech Lead + DBA + devs + DevOps"],
        ["Database design",       "5-10K",  "DBA + Backend Dev"],
        ["UX/UI design",          "5-12K",  "UX + UI + Frontend + Copywriter"],
        ["Security audit",        "5-15K",  "Security Eng + DevSecOps + references"],
        ["Brainstorm session",    "3-8K",   "Creative Intelligence + PM or Tech Lead"],
        ["Test strategy",         "5-10K",  "Test Architect + Tester + Security Eng"],
        ["Document-first build",  "10-20K", "PM + Tech Lead + Scrum + devs"],
        ["Sprint planning",       "3-8K",   "PM + Scrum Master"],
    ],
    col_widths=[2.0, 1.5, 3.0]
)

h2("5 Efficiency Rules")
rules_tok = [
    ("Load Lazy", "Save ~20K tokens/session. Never pre-load all skills — Orchestrator loads on demand."),
    ("Summarize Don't Repeat", "Save ~2-5K/handoff. Handoffs are 2-3 lines, not full history."),
    ("Batch Smart", "30-60 min chunks with checkpoints — prevents unbounded context growth."),
    ("Confirm Before Generating", "Present approach, get approval, then generate — prevents rewrites."),
    ("Reference Files Are Optional", "Reference files (~3-5K each) only loaded when specialist needs deep detail."),
]
for name, desc in rules_tok:
    bullet(f" {desc}", bold_prefix=f"{name}: ")

page_break()


# =============================================================================
# CHAPTER 10 — TROUBLESHOOTING
# =============================================================================
h1("10. Troubleshooting")
rule()

add_table(
    ["Problem", "Solution"],
    [
        ["Claude doesn't use skills",    "Ensure CLAUDE.md is in the project root (not inside skills/)"],
        ["Wrong specialist loaded",       "Say 'switch to [specialist]' or describe the task more specifically"],
        ["Logs not created",             "Run: bash skills/project-monitor/templates/init-logs.sh"],
        ["Session not resuming",         "Check .logs/sessions.md for SESSION_END entries"],
        ["Too many tokens used",         "Say 'YAGNI' or 'simpler' to reduce scope"],
        ["Skill not triggering",         "Check trigger words in the skill's SKILL.md frontmatter"],
        ["CI failing on lint",           "Check .markdownlint.json — MD031/MD040/MD058/MD060 should be false"],
        ["CI failing on validate-skills","Run: python scripts/validate-skills.py locally to see errors"],
        ["Coverage below 80%",          "Identify uncovered paths, write targeted tests, re-run before SHIP"],
        ["Specialist not handoff-ing",   "Ensure HANDOFF note is written before loading next specialist"],
    ],
    col_widths=[2.3, 4.2]
)

h2("Commit and Branch Conventions")
body("CTS enforces these conventions in CLAUDE.md:")
code_block(
    "Commit messages:  type(scope): description\n"
    "  feat(auth): add refresh token rotation\n"
    "  fix(login): resolve 500 on invalid credentials\n"
    "  docs(readme): update specialist count to 23\n\n"
    "Branch naming:    type/short-description\n"
    "  feature/add-auth\n"
    "  fix/login-bug\n"
    "  docs/update-readme"
)

h2("Validation Script")
body("scripts/validate-skills.py checks:")
checks = [
    "claude-team-skills/ directory exists",
    "CLAUDE.md, QUICKSTART.md, INSTALL.md exist and have >50 chars",
    "All 23 skill directories have a SKILL.md file",
    "Each SKILL.md has valid YAML frontmatter (--- delimiters)",
    "Each SKILL.md frontmatter contains name: and description: fields",
    "Each SKILL.md body (after frontmatter) is >=100 chars",
    "Any references/ subdirectory contains at least one .md file (warning only)",
]
for c in checks:
    bullet(c)

page_break()


# =============================================================================
# CHAPTER 11 — CUSTOMIZATION
# =============================================================================
h1("11. Customization")
rule()

h2("Editing CLAUDE.md")
body("CLAUDE.md is your project's configuration file. Add:")
for item in [
    "Your tech stack (e.g. Node.js + PostgreSQL + React + Docker)",
    "Naming conventions specific to your codebase",
    "Deployment URLs and environment names",
    "Team contacts and escalation paths",
    "Project-specific rules (e.g. 'always use Tailwind', 'no class components')",
]:
    bullet(item)

h2("Disabling Unused Skills")
body(
    "Remove rows from the skill locations table in CLAUDE.md. Examples:"
)
add_table(
    ["Project type", "Skills to remove"],
    [
        ["Backend API only",       "frontend-dev, ui-designer, ux-designer, copywriter, content-marketer, digital-marketer"],
        ["Internal tool",          "digital-marketer, copywriter, content-marketer"],
        ["Library / OSS package",  "deployment (simplify), digital-marketer, copywriter, content-marketer"],
        ["Design sprint only",     "backend-dev, dba, deployment, devops-devsecops"],
    ],
    col_widths=[2.0, 4.5]
)

h2("Adding New Specialists")
body("Create skills/your-skill/SKILL.md with this structure:")
code_block(
    "---\n"
    "name: your-specialist-name\n"
    "description: One-line description of what this specialist does\n"
    "triggers:\n"
    "  - keyword1\n"
    "  - keyword2\n"
    "---\n\n"
    "## Role\n"
    "[Define the specialist's role and responsibilities]\n\n"
    "## Key Outputs\n"
    "[Templates, checklists, decision trees]\n\n"
    "## Handoff Points\n"
    "[When to hand off to which other specialist]"
)
body("Then add the skill to:")
bullet("The Orchestrator's routing table (orchestrator/SKILL.md)")
bullet("The skill locations table in CLAUDE.md")

page_break()


# =============================================================================
# APPENDIX A — FULL SPECIALIST QUICK REFERENCE
# =============================================================================
h1("Appendix A — All 23 Specialists at a Glance")
rule()

add_table(
    ["#", "Specialist", "Group", "One-liner"],
    [
        ["1",  "Orchestrator",         "Routing",     "Routes every request; enforces all 6 phases"],
        ["2",  "Project Manager",      "Management",  "Charter, WBS, risk matrix, PRD, status reports"],
        ["3",  "Scrum Master",         "Management",  "Sprints, stories, MoSCoW backlog, retros"],
        ["4",  "Tech Lead",            "Management",  "ADRs, YAGNI, code standards, tech stack"],
        ["5",  "System Designer",      "Architecture","NFRs, topology, scalability, capacity planning"],
        ["6",  "Software Architect",   "Architecture","Clean/Hexagonal/DDD, design patterns, modules"],
        ["7",  "UX Designer",          "Design",      "User flows, wireframes, personas, usability"],
        ["8",  "UI Designer",          "Design",      "Design tokens, color, typography, anti-slop aesthetic"],
        ["9",  "Motion Designer",      "Design",      "Motion tokens, transitions, scroll, React->MP4 video, generative BGs"],
        ["10", "Design Loop",          "Design",      "Independent fresh-context critics instead of self-review"],
        ["11", "Security Engineer",    "Security",    "STRIDE, auth design, OWASP, SOC2/HIPAA/PCI-DSS"],
        ["12", "DBA",                  "Data",        "Schema, query opt, indexes, migrations, backup"],
        ["13", "Backend Dev",          "Dev",         "REST/GraphQL APIs, service layer, ORM, auth"],
        ["14", "Frontend Dev",         "Dev",         "React/Vue/Next components, state, a11y, responsive"],
        ["15", "Tester",               "Quality",     "Unit/integration/e2e, >=80% coverage gate"],
        ["16", "Test Architect",       "Quality",     "Risk-based strategy, ATDD, adversarial review"],
        ["17", "Deployment",           "Operations",  "Rolling/Blue-Green/Canary, env management"],
        ["18", "DevOps/DevSecOps",     "Operations",  "CI/CD, Docker/K8s, Semgrep/Trivy/Checkov"],
        ["19", "Creative Intelligence","Creative",    "7 ideation frameworks, scoring matrix"],
        ["20", "Digital Marketer",     "Marketing",   "SEO, funnels, GA4, A/B testing, campaigns"],
        ["21", "Copywriter",           "Marketing",   "AIDA/PAS/BAB, headlines, CTAs, microcopy"],
        ["22", "Content Marketer",     "Marketing",   "Blog posts, calendar, social, case studies"],
        ["23", "Project Monitor",      "Memory",      "8 log files, 10 KPIs, status reports, retros"],
    ],
    col_widths=[0.3, 1.5, 1.1, 3.6]
)

# Final footer
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Claude Team Skills v2.0.0-beta.1  |  23 specialists  |  59 skill files  |  10,754 lines  |  MIT License")
set_font(run, 9, italic=True, color=MID_GRAY)

# ── Save ─────────────────────────────────────────────────────────────────────
doc.save(OUT)
print(f"Saved -> {OUT}")
