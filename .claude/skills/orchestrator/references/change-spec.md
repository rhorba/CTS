# Change-Spec Workflow (existing codebases)

Use this when a Standard or Full track task changes the behaviour of code that already exists. It keeps a written record of what the system is supposed to do, and makes each change a reviewable delta against that record instead of a diff nobody can check against intent.

Skip it for Quick track work, for pure refactors (behaviour does not change), and for new projects, which use the document chain in `document-chain.md` instead.

## Layout

```
docs/
├── specs/                         ← what the system does NOW (source of truth)
│   └── [capability].md            ← one file per capability, e.g. password-reset.md
└── changes/
    ├── [change-id]/               ← one folder per change in flight, e.g. add-reset-expiry
    │   ├── proposal.md            ← why, what, impact
    │   ├── spec-delta.md          ← ADDED / MODIFIED / REMOVED requirements
    │   └── tasks.md               ← the plan, one task per line
    └── archive/
        └── [YYYY-MM-DD]-[change-id]/   ← shipped changes, moved here unchanged
```

A `change-id` is a short kebab-case verb phrase: `add-reset-expiry`, `fix-duplicate-refund`.

## The loop

```
UNDERSTAND   Find the capability's spec in docs/specs/.
             None yet? Write a baseline first (see "No spec yet").
BRAINSTORM   Options as usual. The chosen option becomes proposal.md.
PLAN         Write spec-delta.md and tasks.md. User confirms the delta
             along with the plan — the delta is what they are agreeing to.
EXECUTE      Build to the delta. Each scenario in it gets a test.
VERIFY       Spec check (below), then the normal tests + security + coverage.
SHIP         Merge the delta into docs/specs/, move the change folder to
             archive/, commit both with the code, push.
```

Two changes that touch the same capability are fine while both are in flight. Whichever ships second re-reads the updated spec and adjusts its delta before merging.

## No spec yet

Most existing codebases have no `docs/specs/`. Do not try to spec the whole system. Write a baseline for only the capability you are about to change:

1. Read the code and tests for that capability.
2. Write `docs/specs/[capability].md` describing what the code does today, including behaviour you think is wrong. The baseline records reality; the delta is where it changes.
3. Mark anything you inferred but could not confirm from code or tests as `(unverified)`.
4. Show the user the baseline before writing the delta. They often know behaviour the code does not make obvious.

The spec grows one capability at a time, as changes touch them.

## Templates

### docs/specs/[capability].md

```markdown
# [Capability name]

## Purpose
[One or two sentences: what this capability is for.]

## Requirements

### Requirement: [short name]
The system SHALL [observable behaviour].

#### Scenario: [short name]
- GIVEN [starting state]
- WHEN [action]
- THEN [observable result]
```

Every requirement has at least one scenario. A requirement with no scenario cannot be tested, so it is not finished.

### docs/changes/[change-id]/proposal.md

```markdown
# [change-id]

## Why
[The problem, and who has it.]

## What changes
[The chosen approach in a few lines. Name the option picked in BRAINSTORM.]

## Impact
- Specs: [capability files affected]
- Code: [modules or areas affected]
- Data: [migrations, or "none"]
- Risk: [what could break, and for whom]
```

### docs/changes/[change-id]/spec-delta.md

```markdown
# Delta for [capability]

## ADDED Requirements

### Requirement: [short name]
The system SHALL [new behaviour].

#### Scenario: [short name]
- GIVEN ...
- WHEN ...
- THEN ...

## MODIFIED Requirements

### Requirement: [existing name, exactly as in the spec]
[The full new text of the requirement and all its scenarios — not just the changed lines.]

## REMOVED Requirements

### Requirement: [existing name]
Reason: [why it is going away]
```

Omit a section that would be empty. A MODIFIED requirement is written out in full so that merging it is a replacement, not an edit.

### docs/changes/[change-id]/tasks.md

```markdown
# Tasks for [change-id]

- [ ] 1.1 [task] — [specialist] — covers: [requirement or scenario names]
- [ ] 1.2 ...
```

Each task names the scenarios it covers. A scenario that no task covers is a gap in the plan.

## Spec check (VERIFY)

Before the normal VERIFY steps, check the code against the delta. When CTS is installed as a plugin, dispatch `cts:spec-reviewer` with `spec-delta.md` as the brief; otherwise do it yourself, scenario by scenario:

| Delta section | What must be true |
|---|---|
| ADDED | Every scenario has code that implements it and a test that would fail without it |
| MODIFIED | The new behaviour is implemented and tested; tests for the old behaviour are updated or removed, not left failing or skipped |
| REMOVED | The behaviour is gone from the code, and so are its tests |
| Not in the delta | Behaviour did not change. Anything that changed outside the delta is either a bug or a missing delta entry |

Add the result to the `[VERIFY]` log entry:

```
- Spec check: [N scenarios checked / M failing] — [change-id]
```

A failing spec check means VERIFY is `Status: fail`.

## Merging the delta (SHIP)

1. ADDED: append each requirement to `docs/specs/[capability].md`.
2. MODIFIED: replace the requirement of the same name with the full text from the delta.
3. REMOVED: delete the requirement.
4. Move `docs/changes/[change-id]/` to `docs/changes/archive/[YYYY-MM-DD]-[change-id]/` without editing it.
5. Commit the spec, the archive move, and the code together, so any commit on the main branch has a spec that matches its code.
