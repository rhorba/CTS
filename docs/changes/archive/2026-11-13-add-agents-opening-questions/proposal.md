# Proposal: add-agents-opening-questions

## Why

Under GitHub Copilot CLI, a plain feature request got a reply that asked no opening questions. The
AGENTS.md rules gate BRAINSTORM and PLAN but never state the UNDERSTAND questions.

## What

Add one rule to the fixed text in `scripts/build-agents-md.py` and regenerate the template.

## Impact

Rules 2 to 7 become 3 to 8. No skill, hook or plugin file changes. Whether Copilot now asks the
questions is checked by the user in Copilot CLI; it is not covered by an automated eval.
