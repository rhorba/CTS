"""Rebuild bmad-vs-cts-comparison.pdf from project source of truth."""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUT = r"C:\Users\moham\OneDrive - um5.ac.ma\Desktop\CTS\bmad-vs-cts-comparison.pdf"

# ── Palette ───────────────────────────────────────────────────────────────────
PURPLE      = colors.HexColor("#6B4EFF")
DARK        = colors.HexColor("#1A1A2E")
MID_GRAY    = colors.HexColor("#555566")
LIGHT_BG    = colors.HexColor("#F5F5F7")
GREEN_BG    = colors.HexColor("#E6FFF0")
RED_BG      = colors.HexColor("#FFF0F0")
GREEN_TEXT  = colors.HexColor("#1A6B4E")
RED_TEXT    = colors.HexColor("#CC2200")
WHITE       = colors.white

doc = SimpleDocTemplate(
    OUT,
    pagesize=letter,
    leftMargin=0.75 * inch,
    rightMargin=0.75 * inch,
    topMargin=0.75 * inch,
    bottomMargin=0.75 * inch,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title", parent=styles["Normal"],
    fontSize=26, fontName="Helvetica-Bold",
    textColor=PURPLE, alignment=TA_CENTER,
    spaceAfter=6,
)
subtitle_style = ParagraphStyle(
    "Subtitle", parent=styles["Normal"],
    fontSize=13, fontName="Helvetica",
    textColor=MID_GRAY, alignment=TA_CENTER,
    spaceAfter=4,
)
h2_style = ParagraphStyle(
    "H2", parent=styles["Normal"],
    fontSize=14, fontName="Helvetica-Bold",
    textColor=DARK, spaceBefore=14, spaceAfter=4,
)
body_style = ParagraphStyle(
    "Body", parent=styles["Normal"],
    fontSize=10, fontName="Helvetica",
    textColor=DARK, spaceAfter=4,
)
note_style = ParagraphStyle(
    "Note", parent=styles["Normal"],
    fontSize=9, fontName="Helvetica-Oblique",
    textColor=MID_GRAY, alignment=TA_CENTER, spaceAfter=6,
)
section_style = ParagraphStyle(
    "Section", parent=styles["Normal"],
    fontSize=11, fontName="Helvetica-Bold",
    textColor=PURPLE, spaceBefore=10, spaceAfter=3,
)

story = []

# ── Cover ─────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.3 * inch))
story.append(Paragraph("BMAD Method vs Claude Team Skills", title_style))
story.append(Paragraph("Side-by-Side Feature Comparison", subtitle_style))
story.append(Paragraph(
    "Version 1.0  ·  21 specialists  ·  52 files  ·  9,503 lines  ·  MIT License",
    note_style
))
story.append(HRFlowable(width="100%", thickness=2, color=PURPLE, spaceAfter=14))

# ── Overview ──────────────────────────────────────────────────────────────────
story.append(Paragraph("Overview", h2_style))
story.append(Paragraph(
    "BMAD Method and Claude Team Skills (CTS) both aim to bring structured, specialist-driven "
    "workflows to AI-assisted software development. They share a common philosophy but diverge "
    "significantly in design priorities. This document compares them feature-by-feature so teams "
    "can make an informed choice.",
    body_style,
))
story.append(Spacer(1, 0.1 * inch))

# ── At-a-Glance table ─────────────────────────────────────────────────────────
story.append(Paragraph("At a Glance", section_style))

glance_data = [
    ["Metric", "BMAD Method", "Claude Team Skills"],
    ["Specialists / roles", "~10-15 personas", "21 specialists"],
    ["Installation", "npm package", "Copy markdown — zero deps"],
    ["Platform", "ChatGPT, Gemini, Claude, 10+ IDEs", "Claude Code native"],
    ["Config format", "YAML (Agent-as-Code)", "Plain markdown"],
    ["Total files", "Varies by bundle", "52 .md files"],
    ["Total lines", "Varies", "9,503 lines"],
    ["License", "MIT", "MIT"],
]
glance_table = Table(
    glance_data,
    colWidths=[1.7 * inch, 2.7 * inch, 2.7 * inch],
    repeatRows=1,
)
glance_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
    ("TEXTCOLOR",  (0, 0), (-1, 0), WHITE),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",   (0, 0), (-1, 0), 10),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_BG, WHITE]),
    ("FONTNAME",   (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",   (0, 1), (-1, -1), 9),
    ("TEXTCOLOR",  (0, 1), (-1, -1), DARK),
    ("FONTNAME",   (0, 1), (0, -1), "Helvetica-Bold"),
    ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCDD")),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 7),
]))
story.append(glance_table)
story.append(Spacer(1, 0.15 * inch))

# ── Feature Comparison ────────────────────────────────────────────────────────
story.append(Paragraph("Feature-by-Feature Comparison", section_style))

comparison_rows = [
    ["Feature", "BMAD Method", "Claude Team Skills", "CTS Rationale"],
    [
        "Installation",
        "npm installer required",
        "Copy markdown — zero deps",
        "No Node.js, no build step. Works in any editor.",
    ],
    [
        "IDE / platform support",
        "10+ IDEs (VS Code, Cursor, Windsurf, ChatGPT, Gemini, Claude...)",
        "Claude Code native only",
        "One platform done exceptionally well beats many done passably.",
    ],
    [
        "Agent style",
        "Named personas (characters with backstories)",
        "Role-based skills (function defines the specialist)",
        "Role-based uses fewer tokens and is easier to maintain.",
    ],
    [
        "Multi-agent debate",
        "Party Mode — agents debate simultaneously",
        "Sequential handoffs with written notes",
        "Sequential saves ~70% tokens vs loading all agents.",
    ],
    [
        "Bundle structure",
        "Modular expansion packs (install what you need)",
        "Single download — everything included",
        "One bundle = no dependency hell, simpler onboarding.",
    ],
    [
        "Complexity control",
        "Scale-adaptive intelligence (auto-detects)",
        "YAGNI gates — user explicitly picks complexity",
        "Explicit choice prevents over-engineering by default.",
    ],
    [
        "Config format",
        "YAML compilation (Agent-as-Code)",
        "Plain markdown — editable in any text editor",
        "Markdown is universal, requires no build step.",
    ],
    [
        "Session memory",
        "Context within session",
        "8 append-only .logs/ files — persist across sessions",
        "Decisions and bugs survive session resets.",
    ],
    [
        "Workflow phases",
        "Task-based (flexible)",
        "6 mandatory phases with hard gates",
        "Non-negotiable gates prevent code shipping before VERIFY.",
    ],
    [
        "Coverage gate",
        "Not enforced by framework",
        ">=80% combined unit + integration — hard gate before SHIP",
        "Coverage is a quality invariant, not a suggestion.",
    ],
    [
        "CI monitoring",
        "Not built-in",
        "DevOps watches every push — CI red = stop all work",
        "CI red is a blocker, not a background event.",
    ],
    [
        "Security integration",
        "Optional security persona",
        "Security Engineer engaged at DESIGN phase + VERIFY gate",
        "Security at design time is cheaper than security at ship time.",
    ],
    [
        "Token efficiency",
        "Varies by persona count loaded",
        "~3-5K for routing (1 specialist at a time)",
        "vs 35K+ if all 21 skills loaded simultaneously.",
    ],
    [
        "KPI tracking",
        "Not built-in",
        "10 KPIs tracked across every sprint (velocity, coverage, etc.)",
        "Data-driven decisions require persistent metrics.",
    ],
    [
        "Document-first",
        "Not enforced",
        "PRD -> Architecture -> Stories chain enforced for large features",
        "Prevents code-before-requirements anti-pattern.",
    ],
    [
        "Adversarial review",
        "Not built-in",
        "Test Architect runs adversarial review for auth/payments/data",
        "SQLi, XSS, IDOR, CSRF, race conditions tested systematically.",
    ],
    [
        "Creative/marketing",
        "Not included",
        "5 creative specialists: Digital Marketer, Copywriter, Content, Creative Intelligence",
        "Full-stack product team, not just engineering.",
    ],
]

# Split into header + data
col_w = [1.5 * inch, 1.65 * inch, 1.65 * inch, 2.3 * inch]
comp_table = Table(comparison_rows, colWidths=col_w, repeatRows=1)
comp_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), PURPLE),
    ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, 0), 9),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_BG, WHITE]),
    ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",      (0, 1), (-1, -1), 8),
    ("TEXTCOLOR",     (0, 1), (-1, -1), DARK),
    ("FONTNAME",      (0, 1), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 1), (0, -1), 8),
    # CTS column: green tint
    ("TEXTCOLOR",     (2, 1), (2, -1), GREEN_TEXT),
    ("FONTNAME",      (2, 1), (2, -1), "Helvetica-Bold"),
    ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCDD")),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 5),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ("WORDWRAP",      (0, 0), (-1, -1), True),
]))
story.append(comp_table)
story.append(Spacer(1, 0.2 * inch))

# ── CTS 21 Specialists ────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=1, color=PURPLE, spaceAfter=8))
story.append(Paragraph("The 21 CTS Specialists", section_style))

specialists = [
    ["#", "Specialist", "Group", "Unique Capabilities vs Generic AI"],
    ["1",  "Orchestrator",         "Routing",     "Routes every request; enforces 6 phases, handoffs, coverage gate"],
    ["2",  "Project Manager",      "Management",  "Charter, WBS, risk matrix, PERT, PRD, Green/Amber/Red status"],
    ["3",  "Scrum Master",         "Management",  "MoSCoW backlog, Fibonacci points, Given/When/Then stories"],
    ["4",  "Tech Lead",            "Management",  "ADRs, YAGNI gate, SOLID/DRY/KISS, debt triage"],
    ["5",  "System Designer",      "Architecture","NFR capture, capacity planning, topology, SLA/SLO, SDRs"],
    ["6",  "Software Architect",   "Architecture","Clean/Hexagonal/DDD, CQRS, fitness functions, dependency rules"],
    ["7",  "UX Designer",          "Design",      "3-tier flows, wireframe states, personas, Nielsen heuristics"],
    ["8",  "UI Designer",          "Design",      "Design tokens, 4px grid, 12-col layout, dark mode rules"],
    ["9",  "Security Engineer",    "Security",    "STRIDE model, auth decision tree, SOC2/HIPAA/PCI-DSS, IR template"],
    ["10", "DBA",                  "Data",        "PostgreSQL-default, 4 index types, EXPLAIN ANALYZE, backup strategy"],
    ["11", "Backend Dev",          "Dev",         "RESTful checklist, Route→Controller→Service→Repository pattern"],
    ["12", "Frontend Dev",         "Dev",         "State management decision table, a11y checklist, breakpoints"],
    ["13", "Tester",               "Quality",     "Testing pyramid, AAA, >=80% coverage gate (non-negotiable)"],
    ["14", "Test Architect",       "Quality",     "Risk scoring, ATDD, adversarial review, edge case hunter"],
    ["15", "Deployment",           "Operations",  "Rolling/Blue-Green/Canary procedures, pre/post checklists"],
    ["16", "DevOps/DevSecOps",     "Operations",  "Semgrep/Trivy/Checkov/Gitleaks, hardened Dockerfile, CI monitoring"],
    ["17", "Creative Intelligence","Creative",    "7 ideation frameworks (SCAMPER, Design Thinking, First Principles)"],
    ["18", "Digital Marketer",     "Marketing",   "SEO checklist, funnel, GA4 events, A/B testing rules"],
    ["19", "Copywriter",           "Marketing",   "AIDA/PAS/BAB, 5 headline types, 8-section landing page"],
    ["20", "Content Marketer",     "Marketing",   "Pillars, calendar, repurposing chain blog→LinkedIn→email→video"],
    ["21", "Project Monitor",      "Memory",      "8 append-only logs, 10 KPIs, status reports, session resumption"],
]

spec_table = Table(
    specialists,
    colWidths=[0.25 * inch, 1.3 * inch, 0.9 * inch, 4.65 * inch],
    repeatRows=1,
)
spec_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), PURPLE),
    ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, 0), 9),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_BG, WHITE]),
    ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",      (0, 1), (-1, -1), 8),
    ("TEXTCOLOR",     (0, 1), (-1, -1), DARK),
    ("FONTNAME",      (0, 1), (1, -1), "Helvetica-Bold"),
    ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCDD")),
    ("TOPPADDING",    (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("LEFTPADDING",   (0, 0), (-1, -1), 4),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(spec_table)
story.append(Spacer(1, 0.2 * inch))

# ── YAGNI & Why CTS ──────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=1, color=PURPLE, spaceAfter=8))
story.append(Paragraph("Why CTS Skips These BMAD Features", section_style))
story.append(Paragraph(
    "CTS intentionally excludes several BMAD features. These are design choices, not gaps. "
    "Each exclusion serves the core principle: one platform, done exceptionally well, "
    "with the minimum complexity needed.",
    body_style,
))

skips = [
    ["Skipped Feature", "BMAD Has", "CTS Position"],
    ["NPM installer",         "✓ Required",   "Zero-dependency is non-negotiable. Copy markdown, start working."],
    ["10+ IDE support",       "✓ Available",  "Claude Code native — deeper integration beats broader coverage."],
    ["Named agent personas",  "✓ Included",   "Role-based skills use fewer tokens and are easier to audit."],
    ["Party Mode debate",     "✓ Included",   "Sequential handoffs save ~70% tokens with no quality loss."],
    ["Expansion packs",       "✓ Available",  "Single bundle — one download, no dependency management."],
    ["Auto complexity scale", "✓ Included",   "Explicit YAGNI gates — user chooses, AI doesn't assume."],
    ["YAML Agent-as-Code",    "✓ Included",   "Plain markdown is universal, editable, versionable by anyone."],
    ["ChatGPT / Gemini web",  "✓ Available",  "Claude Code native — one tool, maximum depth."],
]

skip_table = Table(
    skips,
    colWidths=[1.55 * inch, 1.0 * inch, 4.55 * inch],
    repeatRows=1,
)
skip_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), DARK),
    ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, 0), 9),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_BG, WHITE]),
    ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",      (0, 1), (-1, -1), 8),
    ("TEXTCOLOR",     (0, 1), (-1, -1), DARK),
    ("FONTNAME",      (0, 1), (0, -1), "Helvetica-Bold"),
    ("TEXTCOLOR",     (1, 1), (1, -1), GREEN_TEXT),
    ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#CCCCDD")),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 5),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
]))
story.append(skip_table)
story.append(Spacer(1, 0.2 * inch))

# ── Footer ────────────────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=2, color=PURPLE, spaceAfter=6))
story.append(Paragraph(
    "Claude Team Skills v1.0  ·  21 specialists  ·  52 files  ·  9,503 lines  ·  MIT License  ·  github.com/rhorba/CTS",
    note_style,
))

doc.build(story)
print(f"Saved -> {OUT}")
