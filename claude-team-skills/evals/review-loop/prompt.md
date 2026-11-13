---
description: The three CTS agents run in order on a real code task and the task ends up implemented and tested.
tags: [sandbox]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Agent, Write, Edit, Bash]
---

Run the CTS review loop on the task below. Dispatch `cts:implementer` with the brief, then `cts:spec-reviewer` with the brief and the implementer's report, then `cts:quality-reviewer` once the spec review passes. If a review fails, send the findings back to the implementer once and re-review. Finish by reporting each reviewer's verdict.

TASK BRIEF
Task: add discount codes to the pricing module.
Acceptance criteria:
  - Given a total of 100.00 and the code "SAVE10", when apply_discount is called, then it returns 90.00
  - Given any total and an unknown code, when apply_discount is called, then it raises ValueError
  - Given a total of 0, when apply_discount is called with "SAVE10", then it returns 0
Files / area: pricing.py and tests/test_pricing.py
Specialist skill: backend-dev
Constraints: Python standard library only; tests use unittest and run with `python3 -m unittest discover -s tests`
Out of scope: the existing total() function
