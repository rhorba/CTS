"""Rebuild claude-team-skills-pitch.pptx from project source of truth."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ── Palette ──────────────────────────────────────────────────────────────────
PURPLE      = RGBColor(0x6B, 0x4E, 0xFF)   # CTS primary
DARK_PURPLE = RGBColor(0x3D, 0x1F, 0xAA)
NAVY        = RGBColor(0x1A, 0x1A, 0x2E)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY  = RGBColor(0xF5, 0xF5, 0xF7)
MID_GRAY    = RGBColor(0x8E, 0x8E, 0x93)
GREEN       = RGBColor(0x30, 0xD1, 0x58)
AMBER       = RGBColor(0xFF, 0xCC, 0x00)
RED_SOFT    = RGBColor(0xFF, 0x45, 0x3A)
SLIDE_BG    = RGBColor(0xFF, 0xFF, 0xFF)

W = Inches(13.33)   # widescreen 16:9
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

blank_layout = prs.slide_layouts[6]   # completely blank


# ── Helpers ──────────────────────────────────────────────────────────────────

def add_slide():
    slide = prs.slides.add_slide(blank_layout)
    # white background
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = SLIDE_BG
    return slide


def rect(slide, l, t, w, h, color, alpha=None):
    shape = slide.shapes.add_shape(1, l, t, w, h)   # MSO_SHAPE_TYPE.RECTANGLE = 1
    shape.line.fill.background()
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = color
    return shape


def txt(slide, text, l, t, w, h, size=18, bold=False, color=NAVY,
        align=PP_ALIGN.LEFT, wrap=True, italic=False):
    box = slide.shapes.add_textbox(l, t, w, h)
    box.word_wrap = wrap
    tf = box.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return box


def bullet_box(slide, items, l, t, w, h, size=14, color=NAVY, indent=False, bold_first=False):
    box = slide.shapes.add_textbox(l, t, w, h)
    box.word_wrap = True
    tf = box.text_frame
    tf.word_wrap = True
    first = True
    for item in items:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = item
        run.font.size = Pt(size)
        run.font.color.rgb = color
        if bold_first and item == items[0]:
            run.font.bold = True
    return box


def pill(slide, text, l, t, color=PURPLE, text_color=WHITE, size=11):
    w = Inches(2.2)
    h = Inches(0.32)
    r = rect(slide, l, t, w, h, color)
    tf = r.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = True
    run.font.color.rgb = text_color
    return r


def header_band(slide, title, subtitle=None, bg=PURPLE):
    rect(slide, 0, 0, W, Inches(1.55), bg)
    txt(slide, title, Inches(0.5), Inches(0.2), Inches(12), Inches(0.75),
        size=32, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        txt(slide, subtitle, Inches(0.5), Inches(0.92), Inches(12), Inches(0.5),
            size=15, color=RGBColor(0xD0, 0xC0, 0xFF), align=PP_ALIGN.LEFT)


def slide_number(slide, n, total):
    txt(slide, f"{n} / {total}", Inches(11.8), Inches(7.1), Inches(1.4), Inches(0.35),
        size=10, color=MID_GRAY, align=PP_ALIGN.RIGHT)


# ── Slide data ───────────────────────────────────────────────────────────────
from pathlib import Path

TOTAL = 14


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 1 — Hero
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
rect(s, 0, 0, W, H, NAVY)

# big accent stripe
rect(s, 0, Inches(4.8), W, Inches(0.06), PURPLE)

txt(s, "Claude Team Skills", Inches(0.7), Inches(1.1), Inches(11.9), Inches(1.5),
    size=54, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

txt(s, "23 AI Specialists. One Team. Zero Dependencies.",
    Inches(0.7), Inches(2.7), Inches(11.9), Inches(0.85),
    size=26, color=RGBColor(0xD0, 0xC0, 0xFF), align=PP_ALIGN.CENTER)

txt(s,
    "The structured, token-efficient way to run every software project with Claude Code.",
    Inches(1.5), Inches(3.55), Inches(10.3), Inches(0.75),
    size=16, color=RGBColor(0xBB, 0xBB, 0xCC), align=PP_ALIGN.CENTER)

# badges
badges = [
    ("v2.0", Inches(3.6)),
    ("MIT License", Inches(5.9)),
    ("Zero Dependencies", Inches(8.2)),
]
for label, lx in badges:
    pill(s, label, lx, Inches(5.1), PURPLE)

txt(s, "Built for Claude Code", Inches(0.7), Inches(6.7), Inches(11.9), Inches(0.5),
    size=12, color=MID_GRAY, align=PP_ALIGN.CENTER)
slide_number(s, 1, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 2 — The Problem
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "The Problem", "Generic AI gives you one voice for every role")

# 3 pain cards
cards = [
    ("🏗️  No Process",
     "No phases, no gates, no reviews. Code ships before tests exist and before security is checked."),
    ("🎯  Wrong Expert",
     "One generalist writes the DB schema, designs the UX, and plans the sprint — none of it well."),
    ("🔁  No Memory",
     "Every session starts cold. Decisions, bugs, and risks disappear between conversations."),
]
for i, (title, body) in enumerate(cards):
    lx = Inches(0.35 + i * 4.33)
    rect(s, lx, Inches(1.85), Inches(4.0), Inches(4.5), LIGHT_GRAY)
    rect(s, lx, Inches(1.85), Inches(4.0), Inches(0.06), RED_SOFT)
    txt(s, title, lx + Inches(0.18), Inches(2.05), Inches(3.65), Inches(0.6),
        size=15, bold=True, color=NAVY)
    txt(s, body, lx + Inches(0.18), Inches(2.7), Inches(3.65), Inches(3.0),
        size=13, color=NAVY)

slide_number(s, 2, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 3 — The Solution
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "The Solution", "23 interconnected specialists — each an expert in their domain")

cols = [
    ("23 Specialists", PURPLE,
     ["Every task goes to the right expert.", "PM, Security Eng, DBA, Test Architect,",
      "UX, UI, Motion, DevOps — and 15 more."]),
    ("One Orchestrator", DARK_PURPLE,
     ["Routes every request automatically.", "Loads ONE specialist at a time.",
      "Written handoff on every switch."]),
    ("Structured Workflow", NAVY,
     ["6 mandatory phases with hard gates.", "VERIFY before SHIP — always.",
      "git push at every sprint end."]),
    ("Project Memory", RGBColor(0x1A, 0x6B, 0x4E),
     ["8 append-only log files in .logs/.", "Resume any session from last checkpoint.",
      "KPIs tracked across every sprint."]),
]
for i, (title, bg, lines) in enumerate(cols):
    lx = Inches(0.25 + i * 3.27)
    rect(s, lx, Inches(1.8), Inches(3.1), Inches(4.9), bg)
    txt(s, title, lx + Inches(0.15), Inches(1.95), Inches(2.85), Inches(0.55),
        size=15, bold=True, color=WHITE)
    for j, line in enumerate(lines):
        txt(s, line, lx + Inches(0.15), Inches(2.6 + j * 0.62), Inches(2.85), Inches(0.55),
            size=12, color=RGBColor(0xDD, 0xDD, 0xFF))

slide_number(s, 3, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 4 — The 6-Phase Workflow
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "6-Phase Workflow", "All phases mandatory — hard gates before PLAN, EXECUTE, and SHIP")

phases = [
    ("1", "UNDERSTAND", "Clarify what, where, how big. Up to 3 questions — no assumptions."),
    ("2", "BRAINSTORM", "3 options: 🟢 Simple / 🟡 Balanced / 🔴 Comprehensive. User picks one."),
    ("3", "PLAN", "Numbered tasks in 30-60 min batches. User confirms before code starts."),
    ("4", "EXECUTE", "One task at a time. Show result after each. Written handoff every specialist switch."),
    ("5", "VERIFY", "Tests + OWASP security check. ≥80% coverage gate. Fix CRITICAL before SHIP."),
    ("6", "SHIP", "Deploy, git push, log milestone, notify. CI must be green — no exceptions."),
]
for i, (num, phase, desc) in enumerate(phases):
    row = i % 3
    col = i // 3
    lx = Inches(0.35 + col * 6.5)
    ty = Inches(1.85 + row * 1.72)
    rect(s, lx, ty, Inches(6.1), Inches(1.55), LIGHT_GRAY)
    rect(s, lx, ty, Inches(0.55), Inches(1.55), PURPLE)
    txt(s, num, lx + Inches(0.02), ty + Inches(0.42), Inches(0.52), Inches(0.6),
        size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, phase, lx + Inches(0.65), ty + Inches(0.15), Inches(5.3), Inches(0.45),
        size=14, bold=True, color=PURPLE)
    txt(s, desc, lx + Inches(0.65), ty + Inches(0.58), Inches(5.3), Inches(0.85),
        size=11.5, color=NAVY)

# gates annotation
txt(s, "⛔ GATE after BRAINSTORM   ⛔ GATE after PLAN   ⛔ GATE after VERIFY",
    Inches(0.35), Inches(7.05), Inches(12.6), Inches(0.35),
    size=10.5, color=RED_SOFT, align=PP_ALIGN.CENTER, bold=True)

slide_number(s, 4, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 5 — The Team: Management & Architecture
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "The Team — Management & Architecture",
            "Orchestrator + 7 strategic specialists")

rows = [
    ("Orchestrator",      "Routes every request. Enforces all 6 phases. Loads one specialist at a time."),
    ("Project Manager",   "Project charter, WBS, risk matrix, PERT estimation, PRD, status reports."),
    ("Scrum Master",      "Sprint planning, MoSCoW backlog, user stories (Given/When/Then), retros."),
    ("Tech Lead",         "ADRs, YAGNI gate, code standards, tech stack decisions, technical debt triage."),
    ("System Designer",   "NFRs, capacity planning, topology, scalability patterns, SLA/SLO design."),
    ("Software Architect","Clean/Hexagonal/DDD architecture, design patterns, module boundaries, CQRS."),
    ("Security Engineer", "STRIDE threat model, auth decision tree, OWASP checklist, SOC2/HIPAA/PCI-DSS."),
    ("UX Designer",       "User flows, wireframes, personas, IA, Nielsen heuristics, usability review."),
]
for i, (name, desc) in enumerate(rows):
    ty = Inches(1.78 + i * 0.68)
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(s, Inches(0.3), ty, Inches(12.7), Inches(0.62), bg)
    txt(s, name, Inches(0.45), ty + Inches(0.1), Inches(2.3), Inches(0.45),
        size=12.5, bold=True, color=PURPLE)
    txt(s, desc, Inches(2.8), ty + Inches(0.1), Inches(10.1), Inches(0.45),
        size=12, color=NAVY)

slide_number(s, 5, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 6 — The Team: Engineering & Quality
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "The Team — Design, Engineering & Quality",
            "10 specialists covering design polish, data, code, tests, and operations")

rows = [
    ("UI Designer",      "Design tokens, color/typography system, 4px grid, dark mode, anti-slop aesthetic discipline."),
    ("Motion Designer",  "Motion tokens, micro-interactions, scroll/transitions, React→MP4 video, generative backgrounds."),
    ("Design Loop",      "Independent fresh-context critics (Brief/System/Craft) instead of self-review — kills AI slop."),
    ("DBA",              "Schema design, query optimization, indexes, migrations, backup strategy (PostgreSQL default)."),
    ("Backend Dev",      "REST/GraphQL APIs, service layer pattern, ORM, auth flow, performance checklist."),
    ("Frontend Dev",     "React/Vue/Next components, state management, accessibility (WCAG), responsive design."),
    ("Tester",           "Unit/integration/e2e tests. Hard ≥80% coverage gate. Bug report format. Framework quick ref."),
    ("Test Architect",   "Risk-based strategy, ATDD/Gherkin, adversarial review, edge case hunter, release gates."),
    ("Deployment",       "Rolling/Blue-Green/Canary strategies, pre/post checklist, env management, CI green gate."),
    ("DevOps/DevSecOps", "CI/CD pipelines, Docker/K8s, Terraform, Semgrep/Trivy/Checkov/Gitleaks scanning."),
]
for i, (name, desc) in enumerate(rows):
    ty = Inches(1.72 + i * 0.55)
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(s, Inches(0.3), ty, Inches(12.7), Inches(0.5), bg)
    txt(s, name, Inches(0.45), ty + Inches(0.07), Inches(2.4), Inches(0.4),
        size=12, bold=True, color=PURPLE)
    txt(s, desc, Inches(2.9), ty + Inches(0.07), Inches(10.0), Inches(0.4),
        size=11, color=NAVY)

slide_number(s, 6, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 7 — The Team: Creative & Marketing
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "The Team — Creative & Marketing",
            "5 specialists for ideas, copy, content, growth, and project memory")

rows = [
    ("Creative Intelligence",
     "7 ideation frameworks: Structured Brainstorming, SCAMPER, Design Thinking, First Principles, "
     "Storytelling, Problem Reframing, Name Generation. Scores: Impact × Confidence / Effort."),
    ("Digital Marketer",
     "SEO checklist, marketing funnel (AWARENESS→ADVOCACY), GA4 events, A/B testing rules, "
     "email 5-sequence template, campaign planning."),
    ("Copywriter",
     "AIDA/PAS/BAB frameworks, 5 headline types, landing page 8-section structure, "
     "UX microcopy (error/empty/loading/success), 7 copy rules."),
    ("Content Marketer",
     "Content pillars, weekly calendar, blog post template, LinkedIn/Twitter templates, "
     "case study structure, 9-item quality checklist, repurposing chain."),
    ("Project Monitor",
     "8 append-only logs (activity, decisions, issues, risks, corrections, communications, "
     "sessions, metrics). 10 KPIs tracked. Status reports, retros, init-logs.sh, generate-report.py."),
]
for i, (name, desc) in enumerate(rows):
    ty = Inches(1.78 + i * 1.08)
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(s, Inches(0.3), ty, Inches(12.7), Inches(1.0), bg)
    txt(s, name, Inches(0.45), ty + Inches(0.08), Inches(2.3), Inches(0.45),
        size=12.5, bold=True, color=PURPLE)
    txt(s, desc, Inches(2.8), ty + Inches(0.08), Inches(10.1), Inches(0.85),
        size=11.5, color=NAVY)

slide_number(s, 7, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 8 — Token Efficiency
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "Token Efficiency", "Load one specialist at a time — about 2-8K tokens of routing vs 37K for all")

# Left: vs comparison
rect(s, Inches(0.3), Inches(1.75), Inches(5.8), Inches(5.45), RGBColor(0xFF, 0xF0, 0xF0))
txt(s, "❌  Without CTS",
    Inches(0.5), Inches(1.9), Inches(5.4), Inches(0.5),
    size=15, bold=True, color=RED_SOFT)
without = [
    "Load all skills upfront → about 37K tokens",
    "No handoffs → full history repeated each switch",
    "No phase structure → unbounded context growth",
    "No logging → decisions re-derived every session",
]
for i, line in enumerate(without):
    txt(s, f"• {line}", Inches(0.5), Inches(2.5 + i * 0.65), Inches(5.4), Inches(0.55),
        size=12.5, color=NAVY)

rect(s, Inches(6.5), Inches(1.75), Inches(6.55), Inches(5.45), RGBColor(0xF0, 0xFF, 0xF5))
txt(s, "✅  With CTS",
    Inches(6.7), Inches(1.9), Inches(6.15), Inches(0.5),
    size=15, bold=True, color=GREEN)
with_cts = [
    "Quick track ~2-4K · Standard track ~6-8K (estimates)",
    "2-3 line handoff summaries — full history stays in .logs/",
    "One specialist per task — context never bloats",
    "Reference files loaded on demand — not by default",
]
for i, line in enumerate(with_cts):
    txt(s, f"• {line}", Inches(6.7), Inches(2.5 + i * 0.65), Inches(6.15), Inches(0.55),
        size=12.5, color=NAVY)

# budget table
rect(s, Inches(0.3), Inches(5.95), Inches(12.75), Inches(1.25), LIGHT_GRAY)
budget = [
    ("Quick question", "~2K"),
    ("Bug fix", "~8K"),
    ("Small feature", "~11K"),
    ("UX/UI design", "~12K"),
    ("Security audit", "~9K"),
    ("New project", "~23K"),
]
col_w = Inches(2.12)
for i, (label, tokens) in enumerate(budget):
    lx = Inches(0.35) + i * col_w
    txt(s, label, lx, Inches(6.05), col_w - Inches(0.1), Inches(0.4),
        size=10.5, color=NAVY, align=PP_ALIGN.CENTER, bold=True)
    txt(s, tokens, lx, Inches(6.5), col_w - Inches(0.1), Inches(0.55),
        size=14, color=PURPLE, align=PP_ALIGN.CENTER, bold=True)

slide_number(s, 8, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 9 — Pre-Built Workflows
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "Pre-Built Workflows",
            "Orchestrator recognises the scenario and uses an optimised fast-path automatically")

workflows = [
    ("🐛 Bug Fix",            "15-60 min",  "Tech Lead → Backend/Frontend → Tester"),
    ("✨ New Feature",         "1-4 hrs",    "PM → UX → Tech Lead → DBA → Devs → Tester → Security"),
    ("🚀 New Project",         "2-6 hrs",    "PM → System Designer → Software Architect → UX → Tech Lead → DBA → Security → DevOps"),
    ("📋 Document-First Build","1-2 hrs+",   "PM → Tech Lead → DBA → Security → Scrum → Test Architect"),
    ("🎨 UX/UI Design",        "30-120 min", "UX → UI → Motion Designer → Frontend Dev → Copywriter"),
    ("🗄️ Database Design",     "15-60 min",  "DBA → Tech Lead → Backend Dev"),
    ("🔒 Security Audit",      "30-90 min",  "Security Engineer → DevSecOps → DBA"),
    ("🔐 Security Review",     "20-60 min",  "Security Engineer → DevSecOps → Backend/Frontend"),
    ("🔄 Refactor",            "30-120 min", "Tech Lead → Backend/Frontend → Tester"),
    ("📝 Documentation",       "15-60 min",  "Tech Lead → relevant specialist"),
    ("📢 Marketing Launch",    "1-3 hrs",    "Digital Marketer → Copywriter → Content Marketer"),
    ("💡 Brainstorm/Ideation", "15-45 min",  "Creative Intelligence → PM or Tech Lead"),
    ("🧪 Test Strategy",       "20-60 min",  "Test Architect → Tester → Security Engineer"),
]
for i, (emoji, duration, specialists) in enumerate(workflows):
    ty = Inches(1.75 + i * 0.425)
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(s, Inches(0.25), ty, Inches(12.85), Inches(0.4), bg)
    txt(s, emoji,     Inches(0.35), ty + Inches(0.04), Inches(2.7),  Inches(0.35), size=11.5, bold=True,  color=NAVY)
    txt(s, duration,  Inches(3.15), ty + Inches(0.04), Inches(1.4),  Inches(0.35), size=11,   color=PURPLE, bold=True)
    txt(s, specialists, Inches(4.7), ty + Inches(0.04), Inches(8.25), Inches(0.35), size=10.5, color=NAVY)

slide_number(s, 9, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 10 — Security & Quality Built-In
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "Security & Quality Built-In",
            "Not afterthoughts — gated into every session")

panels = [
    ("🔐  Security Engineer", PURPLE, [
        "5-minute STRIDE threat model",
        "Auth decision tree (JWT / sessions / mTLS / SSO)",
        "OWASP auth checklist + bcrypt/argon2id",
        "RBAC / ABAC / ReBAC authorization patterns",
        "Compliance: SOC2, PCI-DSS, HIPAA, ISO 27001",
        "Incident response: DETECT→CONTAIN→LEARN",
    ]),
    ("🧪  Test Architect", DARK_PURPLE, [
        "Risk-based strategy: score by impact+freq+complexity",
        "ATDD: acceptance criteria written BEFORE coding",
        "Adversarial review: SQLi, XSS, IDOR, CSRF, race conditions",
        "Edge case hunter: boundaries, time (DST/leap), state, network",
        "Release gate: all criteria must pass before SHIP",
        "Traceability matrix: story → test → result",
    ]),
    ("🚦  DevOps/DevSecOps", NAVY, [
        "Semgrep — SAST (OWASP top 10)",
        "Trivy — SCA + container scanning",
        "Checkov — IaC (Terraform) hardening",
        "Gitleaks — secrets detection",
        "CI monitoring: red = stop all work, fix first",
        "Hardened GitHub Actions pipeline template",
    ]),
]
for i, (title, bg, items) in enumerate(panels):
    lx = Inches(0.28 + i * 4.36)
    rect(s, lx, Inches(1.75), Inches(4.15), Inches(5.55), bg)
    txt(s, title, lx + Inches(0.15), Inches(1.88), Inches(3.85), Inches(0.55),
        size=14, bold=True, color=WHITE)
    for j, item in enumerate(items):
        txt(s, f"• {item}", lx + Inches(0.15), Inches(2.55 + j * 0.72), Inches(3.85), Inches(0.62),
            size=11.5, color=RGBColor(0xCC, 0xCC, 0xFF) if bg != NAVY else RGBColor(0xAA, 0xCC, 0xFF))

slide_number(s, 10, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 11 — Zero-Dependency Setup
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "Zero-Dependency Setup", "One plugin, plain markdown and shell — no Node.js, no npm, no build step")

steps = [
    ("Step 1", "Add the marketplace",
     "/plugin marketplace add rhorba/CTS\n\nOr copy the skills/ folder and CLAUDE.md by hand."),
    ("Step 2", "Install the plugin",
     "/plugin install cts@rhorba-cts\n\n23 skills, 3 agents and 3 hooks load together."),
    ("Step 3", "Start working",
     "Open Claude Code and describe what you need.\nThe Orchestrator handles the rest."),
]
for i, (num, title, body) in enumerate(steps):
    lx = Inches(0.5 + i * 4.25)
    rect(s, lx, Inches(1.85), Inches(3.95), Inches(3.8), LIGHT_GRAY)
    # number circle
    rect(s, lx + Inches(1.6), Inches(1.75), Inches(0.75), Inches(0.75), PURPLE)
    txt(s, num[-1], lx + Inches(1.6), Inches(1.78), Inches(0.75), Inches(0.65),
        size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, title, lx + Inches(0.15), Inches(2.6), Inches(3.65), Inches(0.55),
        size=16, bold=True, color=PURPLE)
    txt(s, body, lx + Inches(0.15), Inches(3.2), Inches(3.65), Inches(2.0),
        size=13, color=NAVY)

# file count badges
badges2 = [
    ("23 specialists", Inches(1.0)),
    ("59 skill files",  Inches(4.55)),
    ("10,754 lines",    Inches(8.1)),
    ("0 dependencies",  Inches(11.0)),
]
for label, lx in badges2:
    pill(s, label, lx, Inches(6.3), PURPLE)

txt(s, "Customize: edit CLAUDE.md · disable unused skills · add new specialists in 4 steps",
    Inches(0.5), Inches(6.95), Inches(12.3), Inches(0.4),
    size=11, color=MID_GRAY, align=PP_ALIGN.CENTER)

slide_number(s, 11, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 12 — What's New in v2
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "What's New in v2",
            "The rules are now backed by hooks, subagents and evals")

# column headers
rect(s, Inches(0.3), Inches(1.7), Inches(5.6), Inches(0.45), PURPLE)
rect(s, Inches(6.1), Inches(1.7), Inches(3.2), Inches(0.45), PURPLE)
rect(s, Inches(9.5), Inches(1.7), Inches(3.55), Inches(0.45), DARK_PURPLE)

txt(s, "Capability", Inches(0.4), Inches(1.72), Inches(5.5), Inches(0.4),
    size=12.5, bold=True, color=WHITE)
txt(s, "v1.1", Inches(6.2), Inches(1.72), Inches(3.0), Inches(0.4),
    size=12.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "v2", Inches(9.55), Inches(1.72), Inches(3.4), Inches(0.4),
    size=12.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

comparisons = [
    ("Install",              "Copy markdown files",             "One-command plugin, or copy"),
    ("Ship gate",            "A written rule",                  "Hook blocks git push"),
    ("Execution",            "One context",                     "Fresh subagent per code task"),
    ("Code review",          "Self-review",                     "Spec review, then quality review"),
    ("Small requests",       "Full ceremony",                   "Quick track: one specialist"),
    ("Existing codebases",   "Document-first only",             "Change-spec deltas"),
    ("Other agents",         "Claude Code only",                "Generated AGENTS.md"),
    ("Evidence",             "Structure checks",                "Behavioural evals: 3 of 4 pass"),
]
for i, (feature, before, now) in enumerate(comparisons):
    ty = Inches(2.2 + i * 0.59)
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(s, Inches(0.3), ty, Inches(12.75), Inches(0.55), bg)
    txt(s, feature, Inches(0.42), ty + Inches(0.07), Inches(5.4), Inches(0.42), size=12, color=NAVY, bold=True)
    txt(s, before,  Inches(6.1),  ty + Inches(0.07), Inches(3.2), Inches(0.42), size=11.5, color=MID_GRAY, align=PP_ALIGN.CENTER)
    txt(s, now,     Inches(9.5),  ty + Inches(0.07), Inches(3.55),Inches(0.42), size=11.5, color=GREEN, align=PP_ALIGN.CENTER)

slide_number(s, 12, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 13 — Quick-Start Examples
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
header_band(s, "Just Say What You Need",
            "Just say what you need — the Orchestrator picks the right specialist automatically")

examples = [
    ("💬 Feature",    '"I need to add user authentication"',         "PM → Security → Backend → Tester"),
    ("🐛 Bug",        '"There\'s a 500 error on the login endpoint"', "Tech Lead → Backend → Tester"),
    ("🗄️ Database",   '"Design the schema for a multi-tenant SaaS"', "DBA → Tech Lead → Backend"),
    ("🎨 Design",     '"Redesign the onboarding flow"',              "UX → UI → Frontend → Copywriter"),
    ("🔒 Security",   '"Run a security review before we ship"',      "Security Eng → DevSecOps → Tester"),
    ("🚀 DevOps",     '"Set up a CI/CD pipeline"',                   "DevOps → Deployment"),
    ("📢 Marketing",  '"Write a launch blog post for our feature"',  "Digital Marketer → Copywriter → Content"),
    ("📋 Planning",   '"Plan the next sprint"',                      "Scrum Master → PM → Tech Lead"),
    ("🏗️ Architecture",'"Design the system for 100K users"',         "System Designer → Software Architect → Tech Lead"),
    ("💡 Ideas",      '"Brainstorm names for our product"',          "Creative Intelligence"),
]
for i, (category, prompt, specialists) in enumerate(examples):
    row = i % 5
    col = i // 5
    lx = Inches(0.28 + col * 6.55)
    ty = Inches(1.75 + row * 1.09)
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(s, lx, ty, Inches(6.3), Inches(1.02), bg)
    txt(s, category, lx + Inches(0.12), ty + Inches(0.06), Inches(2.0), Inches(0.38),
        size=11.5, bold=True, color=PURPLE)
    txt(s, prompt, lx + Inches(0.12), ty + Inches(0.42), Inches(6.05), Inches(0.38),
        size=11, color=NAVY, italic=True)
    txt(s, f"→ {specialists}", lx + Inches(0.12), ty + Inches(0.72), Inches(6.05), Inches(0.28),
        size=10, color=MID_GRAY)

slide_number(s, 13, TOTAL)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Slide 14 — CTA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
s = add_slide()
rect(s, 0, 0, W, H, NAVY)
rect(s, 0, Inches(3.5), W, Inches(0.06), PURPLE)

txt(s, "Ready to Ship Better Software?",
    Inches(0.5), Inches(0.8), Inches(12.3), Inches(1.1),
    size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

txt(s, "3 steps. 0 dependencies. 23 specialists on your team from day one.",
    Inches(1.0), Inches(2.0), Inches(11.3), Inches(0.65),
    size=20, color=RGBColor(0xD0, 0xC0, 0xFF), align=PP_ALIGN.CENTER)

steps_cta = [
    "1  /plugin marketplace add rhorba/CTS",
    "2  /plugin install cts@rhorba-cts",
    "3  Open Claude Code and start describing work",
]
for i, step in enumerate(steps_cta):
    txt(s, step, Inches(3.0), Inches(3.8 + i * 0.72), Inches(7.3), Inches(0.6),
        size=17, color=WHITE, align=PP_ALIGN.LEFT)

rect(s, Inches(3.8), Inches(6.25), Inches(5.75), Inches(0.7), PURPLE)
txt(s, "github.com/rhorba/CTS",
    Inches(3.8), Inches(6.27), Inches(5.75), Inches(0.65),
    size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

txt(s, "Claude Team Skills v2.0.0-beta.1 · MIT License · 23 specialists · 59 skill files · 10,754 lines",
    Inches(0.5), Inches(7.1), Inches(12.3), Inches(0.35),
    size=10, color=MID_GRAY, align=PP_ALIGN.CENTER)

slide_number(s, 14, TOTAL)


# ── Save ─────────────────────────────────────────────────────────────────────
out = str(Path(__file__).resolve().parent.parent / "claude-team-skills-pitch.pptx")
prs.save(out)
print(f"Saved {TOTAL} slides -> {out}")
