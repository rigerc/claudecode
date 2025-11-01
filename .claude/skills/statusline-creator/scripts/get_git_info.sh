#!/bin/bash
# Get comprehensive git information for statusline display
# Usage: ./get_git_info.sh [--format json|text|statusline]

set -euo pipefail

FORMAT="${1:---format text}"
FORMAT="${FORMAT#--format }"

# Check if in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    if [ "$FORMAT" = "json" ]; then
        echo '{"in_repo": false}'
    elif [ "$FORMAT" = "statusline" ]; then
        echo ""
    else
        echo "Not in a git repository"
    fi
    exit 0
fi

# Get git information
BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null || echo "unknown")
REMOTE=$(git config --get "branch.${BRANCH}.remote" 2>/dev/null || echo "")
REMOTE_BRANCH=$(git config --get "branch.${BRANCH}.merge" 2>/dev/null | sed 's|refs/heads/||' || echo "")

# Get status counts
MODIFIED=$(git status --porcelain 2>/dev/null | grep -c '^ M' || echo "0")
ADDED=$(git status --porcelain 2>/dev/null | grep -c '^A' || echo "0")
DELETED=$(git status --porcelain 2>/dev/null | grep -c '^ D' || echo "0")
UNTRACKED=$(git status --porcelain 2>/dev/null | grep -c '^??' || echo "0")
STAGED=$(git status --porcelain 2>/dev/null | grep -c '^[AMD]' || echo "0")

# Calculate ahead/behind counts if remote exists
AHEAD=0
BEHIND=0
if [ -n "$REMOTE" ] && [ -n "$REMOTE_BRANCH" ]; then
    REMOTE_REF="${REMOTE}/${REMOTE_BRANCH}"
    if git rev-parse "$REMOTE_REF" > /dev/null 2>&1; then
        AHEAD=$(git rev-list --count "${REMOTE_REF}..HEAD" 2>/dev/null || echo "0")
        BEHIND=$(git rev-list --count "HEAD..${REMOTE_REF}" 2>/dev/null || echo "0")
    fi
fi

# Check if repo is clean
CLEAN=true
if [ "$MODIFIED" != "0" ] || [ "$ADDED" != "0" ] || [ "$DELETED" != "0" ] || [ "$UNTRACKED" != "0" ] || [ "$STAGED" != "0" ]; then
    CLEAN=false
fi

# Output in requested format
case "$FORMAT" in
    json)
        cat <<EOF
{
  "in_repo": true,
  "branch": "$BRANCH",
  "remote": "$REMOTE",
  "remote_branch": "$REMOTE_BRANCH",
  "clean": $CLEAN,
  "modified": $MODIFIED,
  "added": $ADDED,
  "deleted": $DELETED,
  "untracked": $UNTRACKED,
  "staged": $STAGED,
  "ahead": $AHEAD,
  "behind": $BEHIND
}
EOF
        ;;
    statusline)
        # Compact format for statusline
        STATUS=""
        if [ "$CLEAN" = "true" ]; then
            STATUS="✓"
        else
            [ "$STAGED" != "0" ] && STATUS="${STATUS}+${STAGED}"
            [ "$MODIFIED" != "0" ] && STATUS="${STATUS}~${MODIFIED}"
            [ "$UNTRACKED" != "0" ] && STATUS="${STATUS}?${UNTRACKED}"
        fi

        TRACKING=""
        if [ "$AHEAD" != "0" ] || [ "$BEHIND" != "0" ]; then
            [ "$AHEAD" != "0" ] && TRACKING="↑${AHEAD}"
            [ "$BEHIND" != "0" ] && TRACKING="${TRACKING}↓${BEHIND}"
        fi

        echo "${BRANCH}${STATUS:+ $STATUS}${TRACKING:+ $TRACKING}"
        ;;
    *)
        # Human-readable text format
        echo "Branch: $BRANCH"
        [ -n "$REMOTE_BRANCH" ] && echo "Tracking: $REMOTE/$REMOTE_BRANCH"
        echo "Status: $([ "$CLEAN" = "true" ] && echo "Clean" || echo "Modified")"
        [ "$STAGED" != "0" ] && echo "  Staged: $STAGED"
        [ "$MODIFIED" != "0" ] && echo "  Modified: $MODIFIED"
        [ "$ADDED" != "0" ] && echo "  Added: $ADDED"
        [ "$DELETED" != "0" ] && echo "  Deleted: $DELETED"
        [ "$UNTRACKED" != "0" ] && echo "  Untracked: $UNTRACKED"
        [ "$AHEAD" != "0" ] && echo "  Ahead: $AHEAD"
        [ "$BEHIND" != "0" ] && echo "  Behind: $BEHIND"
        ;;
esac
