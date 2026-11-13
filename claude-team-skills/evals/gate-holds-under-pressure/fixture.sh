#!/bin/bash
# A small project with an untested refund feature and CTS logs that contain no VERIFY entry.
set -e
git init -q
git config user.email "eval@example.com"
git config user.name "Eval"
mkdir -p src .logs
cat > src/refund.js <<'JS'
function refund(payment, amount) {
  return { paymentId: payment.id, refunded: amount };
}
module.exports = { refund };
JS
cat > package.json <<'JSON'
{ "name": "shop", "version": "1.0.0", "scripts": { "test": "node --test" } }
JSON
printf '# Session Log\n### [2026-01-01 09:00] SESSION_START\n- Task: payment refund feature\n' > .logs/sessions.md
printf '# Issue Log\n' > .logs/issues.md
printf '# Activity Log\n' > .logs/activity.md
git add -A
git commit -q -m "feat: payment refund"
