#!/bin/sh
# SessionEnd hook. If the session was opened in .logs/sessions.md but never closed,
# append a placeholder SESSION_END so the next session knows the summary is missing
# instead of resuming from a stale one.

project=${CLAUDE_PROJECT_DIR:-.}
sessions="$project/.logs/sessions.md"

[ -f "$sessions" ] || exit 0

last_heading=$(grep '^### ' "$sessions" | tail -n 1)
case "$last_heading" in
  *SESSION_START*) ;;
  *) exit 0 ;;
esac

{
  echo
  echo "### [$(date '+%Y-%m-%d %H:%M')] SESSION_END (auto)"
  echo "- Completed: not recorded — the session closed before a summary was written"
  echo "- Next: rebuild the state from .logs/activity.md and .logs/issues.md before continuing"
} >> "$sessions"
