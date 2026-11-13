#!/bin/sh
# PreToolUse hook for `git push`. Exit 2 blocks the push; stderr is shown to Claude.
#
# The gate applies only to projects that use CTS logging (a .logs/ directory exists).
# It passes when:
#   1. the most recent [VERIFY] entry in .logs/issues.md has "Status: pass", and
#   2. there are more passing [VERIFY] entries than [SHIP] entries in .logs/activity.md
#      (each ship consumes one verification), and
#   3. the latest coverage line in .logs/metrics.md is >= 80%, or is "n/a".

project=${CLAUDE_PROJECT_DIR:-.}
logs="$project/.logs"
min_coverage=80

[ -d "$logs" ] || exit 0

block() {
  echo "CTS push gate: $1" >&2
  echo "Complete the VERIFY phase, log it, then push again. See the cts:orchestrator skill, Phase 5." >&2
  exit 2
}

issues="$logs/issues.md"
[ -f "$issues" ] || block "no .logs/issues.md, so VERIFY has not been logged."

# Prints "<passing VERIFY count> <status of the last VERIFY entry>".
verify=$(awk '
  /^### /                   { in_verify = ($0 ~ /\[VERIFY\]/) }
  in_verify && /^- Status:/ {
    last = ($0 ~ /Status:[ \t]*pass/) ? "pass" : "fail"
    if (last == "pass") passes++
    in_verify = 0
  }
  END { print passes + 0, (last == "" ? "none" : last) }
' "$issues")
passes=${verify% *}
last=${verify#* }

[ "$last" = "none" ] && block "no [VERIFY] entry with a Status line in .logs/issues.md."
[ "$last" = "pass" ] || block "the latest [VERIFY] entry is not 'Status: pass'. Fix the failures and re-verify."

ships=0
if [ -f "$logs/activity.md" ]; then
  ships=$(grep -c '^### .*\[SHIP\]' "$logs/activity.md")
fi
[ "$passes" -gt "$ships" ] || block "the last passing VERIFY was already used by a previous SHIP. Verify the new changes."

metrics="$logs/metrics.md"
line=""
if [ -f "$metrics" ]; then
  line=$(grep -i 'coverage' "$metrics" | tail -n 1)
fi
[ -n "$line" ] || block "no coverage logged in .logs/metrics.md. Log 'Coverage: N%' or 'Coverage: n/a — reason'."

case "$line" in
  *[Nn]/[Aa]*) exit 0 ;;
esac

percent=$(printf '%s\n' "$line" | sed -n 's/.*[Cc]overage[^0-9]*\([0-9][0-9]*\).*/\1/p')
[ -n "$percent" ] || block "could not read a percentage from the latest coverage line: $line"
[ "$percent" -ge "$min_coverage" ] || block "coverage is ${percent}%, below the ${min_coverage}% gate. Add tests and re-run coverage."

exit 0
