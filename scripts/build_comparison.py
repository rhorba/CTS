"""Build cts-comparison.pdf: CTS v2 against five agent-workflow frameworks.

Run from the repo root:  python scripts/build_comparison.py

Competitor descriptions are summarised from public documentation and third-party
reviews read in November 2026 (listed on the last page). They describe what each
project is known for, not an audit of everything it can do.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "cts-comparison.pdf"
VERSION = "2.0.0-beta.1"
AS_OF = "November 2026"

INK = colors.HexColor("#16202A")
MUTED = colors.HexColor("#5B6770")
ACCENT = colors.HexColor("#0B6E4F")
ACCENT_TINT = colors.HexColor("#E7F3EE")
RULE = colors.HexColor("#C9D1D6")
BAND = colors.HexColor("#F4F6F7")

base = getSampleStyleSheet()["Normal"]


def style(name, **kw):
    return ParagraphStyle(name, parent=base, **{"fontName": "Helvetica", "textColor": INK, **kw})


TITLE = style("title", fontName="Helvetica-Bold", fontSize=24, leading=28, spaceAfter=4)
SUB = style("sub", fontSize=11, leading=15, textColor=MUTED, spaceAfter=10)
H2 = style("h2", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceBefore=12, spaceAfter=6, textColor=ACCENT)
BODY = style("body", fontSize=9.5, leading=13, spaceAfter=5)
CELL = style("cell", fontSize=8, leading=10.5)
CELL_B = style("cellb", fontSize=8, leading=10.5, fontName="Helvetica-Bold")
HEAD = style("head", fontSize=8.5, leading=11, fontName="Helvetica-Bold", textColor=colors.white)
NOTE = style("note", fontSize=8, leading=11, textColor=MUTED)
FOOT = style("foot", fontSize=8, leading=11, textColor=MUTED, alignment=TA_CENTER)


def table(rows, widths, highlight_col=None):
    """rows[0] is the header. Every cell is wrapped in a Paragraph so text wraps."""
    data = [[Paragraph(c, HEAD) for c in rows[0]]]
    for row in rows[1:]:
        data.append([Paragraph(c, CELL_B if i == 0 else CELL) for i, c in enumerate(row)])
    t = Table(data, colWidths=widths, repeatRows=1)
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BAND]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    if highlight_col is not None:
        commands.append(("BACKGROUND", (highlight_col, 1), (highlight_col, -1), ACCENT_TINT))
        commands.append(("BACKGROUND", (highlight_col, 0), (highlight_col, 0), ACCENT))
    t.setStyle(TableStyle(commands))
    return t


LANDSCAPE = [
    ["", "Claude Team Skills", "Superpowers", "ECC", "BMAD Method", "Spec Kit", "OpenSpec"],
    ["GitHub stars",
     "0 (0 forks)", "317,000", "302,000", "55,000", "150,000", "75,000"],
    ["Latest release",
     "v2.0.0-beta.1, Nov 2026", "v7.0.2, Nov 2026", "v2.2.3, Oct 2026", "v6.12.4, Oct 2026",
     "v1.4.0, Nov 2026", "v2.0.0, Nov 2026"],
    ["Known for",
     "A 23-role team (engineering, design, security, marketing) run through six gated phases",
     "An engineering methodology: brainstorm, plan, then test-driven work with review",
     "A large ready-made configuration: agents, skills, hooks, security scanning and memory",
     "The full agile lifecycle, from ideation to deployment, with many workflows",
     "Spec-driven development for new work: spec, plan, tasks",
     "Lightweight spec tracking for changes to existing code"],
    ["How you get it",
     "Claude Code plugin, or copy the markdown; AGENTS.md for other agents",
     "Claude Code plugin; in Anthropic's official marketplace",
     "Plugin for Claude Code, Cursor, Codex and OpenCode",
     "npx installer with selectable modules",
     "Command-line toolkit",
     "Command-line toolkit"],
    ["Roles beyond engineering",
     "UX, UI, motion, copy, content, marketing, project management",
     "Engineering focused",
     "Engineering focused: planning, review, security, testing agents",
     "Analyst, product and agile roles; creative module",
     "Not role based",
     "Not role based"],
    ["Hooks and memory",
     "Push gate, session resume and session close hooks; eight project log files",
     "Not covered in the sources reviewed",
     "Hooks across many events; memory persistence",
     "Not covered in the sources reviewed",
     "Not its focus",
     "Not its focus"],
    ["Fresh-context execution",
     "Implementer subagent per task, then spec review, then quality review",
     "Subagent per task with spec-compliance and code-quality review",
     "Specialised agents per activity",
     "Party mode: several personas discuss in one session",
     "Not its focus",
     "Not its focus"],
    ["Specs for existing code",
     "Change-spec workflow: baseline, proposal, delta, spec check, merge",
     "Plans per task",
     "Not its focus",
     "Planning documents per track",
     "Aimed at new work",
     "Its core purpose"],
    ["Scaling the ceremony",
     "Three tracks: Quick, Standard, Full",
     "One workflow",
     "Not covered in the sources reviewed",
     "Tracks from quick flow to enterprise",
     "One workflow",
     "Deliberately lightweight"],
    ["Common criticism in reviews",
     "No users yet; small eval suite (see page 2)",
     "Overhead and latency from mandatory steps",
     "No independent critical review found",
     "Setup effort; heavy for teams under five",
     "Heavy for small changes",
     "Less guidance for building new systems"],
]

DIFFERENTIATORS = [
    ["What CTS does", "How it is backed", "Where to look"],
    ["Blocks a push until verification is logged",
     "A hook stops <b>git push</b> unless the latest VERIFY entry is a pass, is newer than the last SHIP, "
     "and logged coverage is at least 80%. The same script works as a plain git pre-push hook under any agent.",
     "hooks/push-gate.sh, 13 behaviour tests"],
    ["Covers the whole product, not only the code",
     "23 specialists, including UX, UI, motion, security, DBA, copy, content and marketing, "
     "loaded one at a time. This is the clearest gap in the engineering-focused alternatives.",
     "skills/"],
    ["Remembers the project between sessions",
     "Eight append-only log files. A hook loads the last session summary at start and closes sessions "
     "that ended without one.",
     "hooks/session-start.sh, session-end.sh"],
    ["Scales effort to the request",
     "Quick answers come straight from one specialist; Standard and Full add gates, documents and subagents. "
     "All six phases are logged on every track.",
     "skills/orchestrator/SKILL.md"],
    ["Reviews with fresh eyes",
     "Code tasks go to an implementer, then a spec reviewer, then a quality reviewer, none of which saw "
     "the conversation. Visual work goes through three independent design critics.",
     "agents/, skills/design-loop/"],
    ["Publishes its own test results",
     "Behavioural evals run with Claude Code's built-in eval command; results and known gaps are in the repo.",
     "evals/README.md"],
]

LIMITS = [
    "<b>No adoption yet.</b> On 13 November 2026 the repository had 0 stars, 0 forks and 5 unique cloners in "
    "14 days. Every project in the table has between 55,000 and 317,000 stars.",
    "<b>Hooks, memory and subagents are not unique.</b> ECC ships hooks and memory, and Superpowers ships "
    "per-task subagents with two-stage review. What CTS combines them with is the non-engineering team "
    "and a gate on the push itself.",
    "<b>Evals are small.</b> Four core cases pass, one run each. A fifth check, that the orchestrator loads when "
    "a user demands to ship untested code, failed in 6 of 6 runs and was removed from scoring: Claude holds "
    "the gate, but on its own.",
    "<b>The review loop has not been run end to end.</b> Its eval case is written but needs a sandbox "
    "(WSL2 or Linux) that was not available when this was published.",
    "<b>The push gate checks the log, not the tests.</b> It catches a skipped VERIFY phase. It cannot tell "
    "whether a logged pass was earned.",
    "<b>Hooks and subagents need the plugin install,</b> and AGENTS.md is untested outside Claude Code.",
]

SOURCES = [
    "GitHub API, 13 November 2026 (stars, forks, releases)",
    "rywalker.com/research/agentic-skills-frameworks",
    "dailyaiworld.com/blogs/ai-agent-skills-frameworks-comparison-2026",
    "mintlify.com/bmad-code-org/BMAD-METHOD",
    "mintlify.com/obra/superpowers/concepts/workflow",
    "kunalganglani.com/blog/superpowers-agentic-skills-framework",
    "augmentcode.com/learn/everything-claude-code-github",
    "mintlify.com/affaan-m/everything-claude-code",
    "dabase.com/blog/2026/sdd-framework-comparison",
    "codemyspec.com/blog/openspec-vs-spec-kit",
]


def build(out=OUT):
    doc = SimpleDocTemplate(
        str(out), pagesize=landscape(letter),
        leftMargin=0.6 * inch, rightMargin=0.6 * inch, topMargin=0.45 * inch, bottomMargin=0.4 * inch,
        title="Claude Team Skills: how it compares", author="CTS",
    )
    width = landscape(letter)[0] - 1.2 * inch
    story = [
        Paragraph("Claude Team Skills: how it compares", TITLE),
        Paragraph(
            f"CTS v{VERSION} beside the five most-starred agent-workflow frameworks. Competitor columns summarise public "
            f"documentation and reviews read in {AS_OF}; they describe what each project is known for.", SUB),
        HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=8),
        table(LANDSCAPE, [1.05 * inch] + [(width - 1.05 * inch) / 6] * 6, highlight_col=1),
        PageBreak(),
        Paragraph("What sets CTS apart", H2),
        table(DIFFERENTIATORS, [2.1 * inch, width - 2.1 * inch - 2.3 * inch, 2.3 * inch]),
        Paragraph("Known limits", H2),
    ]
    story += [Paragraph(f"• {item}", BODY) for item in LIMITS]
    story += [
        Paragraph("Sources for the competitor columns", H2),
        Paragraph(" · ".join(SOURCES), NOTE),
        Paragraph(
            "Star counts are rounded and come from the GitHub API on the date shown. Two other large projects "
            "are not in the table: anthropics/skills (194,000 stars, a skill catalogue with no workflow) and "
            "get-shit-done (64,000 stars, no commits since May 2026).", NOTE),
        Spacer(1, 4),
        Paragraph(f"Claude Team Skills v{VERSION} · MIT License · github.com/rhorba/CTS", FOOT),
    ]
    doc.build(story)
    return out


if __name__ == "__main__":
    print(f"Wrote {build()}")
