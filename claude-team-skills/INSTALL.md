# Claude Team Skills — Installation Guide

## Option A: Install as a plugin (recommended)

In a Claude Code session:

```
/plugin marketplace add rhorba/CTS
/plugin install cts@rhorba-cts
```

The 23 specialists load as plugin skills (`cts:orchestrator`, `cts:tester`, …). Nothing is copied into your project, and updates arrive with the plugin.

The plugin also installs three hooks: one loads the CTS rules and your last session summary at session start, one blocks `git push` until VERIFY and coverage are logged, and one closes unfinished sessions in `.logs/sessions.md`. They are POSIX shell scripts; on Windows they need Git Bash, which Claude Code uses by default when it is installed. Option B does not include the hooks.

## Option B: Copy the files

### Step 1: Copy the skills folder
Place the entire `skills/` directory in your project root:

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
│   ├── motion-designer/          ← animation, transitions, promo video, generative visuals
│   │   └── references/
│   ├── design-loop/              ← One-shot design quality via independent critics
│   │   └── references/
│   ├── backend-dev/
│   ├── frontend-dev/
│   ├── tester/
│   ├── deployment/
│   ├── devops-devsecops/
│   │   └── references/        ← 5 deep-dive security files
│   ├── digital-marketer/
│   ├── copywriter/
│   ├── content-marketer/
│   ├── creative-intelligence/   ← Brainstorming, design thinking, innovation
│   ├── test-architect/          ← Test strategy, ATDD, adversarial review
│   └── project-monitor/         ← Logging, KPIs, status reports
│       ├── references/
│       └── templates/         ← init-logs.sh script
├── .logs/                     ← Auto-created on first session
│   ├── activity.md
│   ├── decisions.md
│   ├── issues.md
│   ├── risks.md
│   ├── corrections.md
│   ├── communications.md
│   ├── sessions.md
│   └── metrics.md
├── CLAUDE.md                  ← Copy this to project root
├── QUICKSTART.md              ← Your cheat sheet
└── ... your project files
```

### Step 2: Add CLAUDE.md to project root
Copy `templates/CLAUDE.md` to your project root. This is the entry point that tells Claude Code how to use the skills.

### Step 3: Start working
Open Claude Code and just describe what you need:
- "I need to build a user authentication feature"
- "There's a bug in the payment flow"
- "Set up CI/CD for this project"
- "Write a blog post about our new release"

The orchestrator handles the rest.

---

## How It Works

```
You say something
       │
       ▼
 CLAUDE.md loads → reads orchestrator
       │
       ▼
 Orchestrator identifies the task type
       │
       ▼
 Loads ONLY the needed specialist
       │
       ▼
 Interactive work: options → pick → execute → verify
       │
       ▼
 Switches specialist if needed (with handoff summary)
```

## Token Usage

This setup is designed to be lean:
- Session context (plugin): ~0.5K tokens, or CLAUDE.md (copy install): ~2K tokens (always loaded)
- Orchestrator: ~4K tokens (loaded for Standard and Full track work)
- Each specialist: ~1-3K tokens (loaded one at a time)
- Reference files: ~3-5K tokens each (loaded only for deep dives)

**Typical routing cost**: ~2-4K tokens on the Quick track and ~6-8K on Standard, plus whatever the actual work costs.
Loading everything at once would cost ~37K tokens. These are estimates at about 4 characters per token.

## Customization

### Add your project's conventions
Edit `CLAUDE.md` to include:
- Your tech stack specifics
- Naming conventions
- Deployment URLs
- Team contacts
- Any project-specific rules

### Disable skills you don't need
Remove or comment out rows in the CLAUDE.md skill locations table.
If you're purely a backend project, you can skip: frontend-dev, copywriter, content-marketer, digital-marketer.

### Add new specialists
Create a new folder in `skills/` with a `SKILL.md` following the same pattern:
1. YAML frontmatter with name + description
2. Role definition
3. Key templates/checklists
4. Handoff points to other specialists
5. Add it to the orchestrator's routing table + CLAUDE.md

---

## FAQ

**Q: Does Claude really load skills one at a time?**
A: Yes. The orchestrator tells Claude which skill to read for the current step. It never loads all 23 at once.

**Q: What if I need two specialists at the same time?**
A: The orchestrator handles this with the handoff protocol — it summarizes context in 2-3 lines when switching, so no tokens are wasted repeating full history.

**Q: Can I use these with Claude.ai (not Claude Code)?**
A: The skills are optimized for Claude Code, but you can paste individual SKILL.md content into Claude.ai conversations as needed. The orchestrator workflow works in any Claude interface.

**Q: How do I update a skill?**
A: Just edit the SKILL.md file. Changes take effect on the next session.

**Q: How does project logging work?**
A: On first session, Claude creates a `.logs/` directory with 8 structured log files (activity, decisions, issues, risks, corrections, communications, sessions, metrics). Every significant action gets appended as a log entry. You can ask for "status report", "KPIs", or "retro" at any time. Logs persist across sessions, so Claude can resume where you left off. You can also run `bash skills/project-monitor/templates/init-logs.sh` to initialize logs manually.

**Q: Should I commit `.logs/` to git?**
A: Up to you. The init script adds `.logs/` to `.gitignore` by default (keeps logs private). Remove that line if you want logs in version control for team visibility.

## How CTS Compares

CTS is one of several free agent-workflow frameworks, and the established ones (Superpowers, ECC, Spec Kit, OpenSpec, BMAD Method) have far larger communities. Hooks, session memory, per-task subagents and spec deltas all exist elsewhere. What CTS adds is a team beyond engineering (UX, UI, motion, copy, content, marketing, project management) in the same gated workflow, and a hook that blocks `git push` until verification is logged.

CTS's design choices: plain markdown and POSIX shell with no build step, role-based skills rather than personas, one specialist loaded at a time, and a single bundle.

The repository README has the comparison table, and `cts-comparison.pdf` has the feature-by-feature detail and known limits.
