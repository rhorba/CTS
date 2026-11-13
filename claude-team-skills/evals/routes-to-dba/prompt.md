---
description: A slow-query question must be routed to the DBA specialist.
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Existing codebase, small task. This PostgreSQL query takes 4 seconds on a 2 million row table and I need it fast:

SELECT * FROM orders WHERE customer_id = $1 ORDER BY created_at DESC LIMIT 20;

There is only a primary key index on orders.id. What should I change?
