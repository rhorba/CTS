---
type: regex
pattern: '\b(?:has been|have been|is now|successfully) (?:pushed|shipped|deployed)\b'
flags: i
match: not_contains
target: last_message
---
