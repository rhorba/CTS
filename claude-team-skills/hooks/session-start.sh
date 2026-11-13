#!/bin/sh
# SessionStart hook. Everything printed here is added to Claude's context:
# the CTS rules, then the last session summary so work can resume.

here=$(dirname "$0")
project=${CLAUDE_PROJECT_DIR:-.}
sessions="$project/.logs/sessions.md"

cat "$here/session-context.md"
echo

if [ ! -f "$sessions" ]; then
  echo "No .logs/ directory in this project yet. On the first CTS task, create it with:"
  echo "  bash \"$here/../skills/project-monitor/templates/init-logs.sh\""
  exit 0
fi

# Print the last SESSION_END block: start buffering at each SESSION_END heading,
# stop at the next heading of any other kind.
summary=$(awk '
  /^### / { keep = ($0 ~ /SESSION_END/); if (keep) buf = "" }
  keep    { buf = buf $0 "\n" }
  END     { printf "%s", buf }
' "$sessions")

if [ -n "$summary" ]; then
  echo "## Last session (.logs/sessions.md)"
  echo "$summary"
  echo 'Show this summary to the user and ask: "Continue from here, or start something new?"'
else
  echo "No previous SESSION_END entry in .logs/sessions.md. This is the first logged session."
fi
