---
tags: [core]
description: With UNDERSTAND already answered, BRAINSTORM must present three ranked options and wait for a pick.
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

What: a new feature, password reset by email. Where: an existing Express and PostgreSQL codebase that already has login with bcrypt and sessions. How big: medium. Email goes out through an SMTP_URL environment variable that is already configured. That is everything you need to know, so move on to the approaches.
