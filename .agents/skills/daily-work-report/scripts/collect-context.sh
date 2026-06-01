#!/usr/bin/env bash
# collect-context.sh — Collect work context for a given date
# Usage: ./collect-context.sh <date YYYY-MM-DD> <workdir>
# Example: ./collect-context.sh 2026-05-08 /d/opc-workspace

set -euo pipefail

TARGET_DATE="${1:?Usage: $0 <YYYY-MM-DD> <workdir>}"
WORKDIR="${2:-.}"
HOME_DIR="${HOME:-$USERPROFILE}"

echo "=== Work Context for ${TARGET_DATE} ==="
echo ""

# 1. Memory files modified on target date
echo "--- Memory Files (modified ${TARGET_DATE}) ---"
find "$HOME_DIR/.claude/projects" -path "*/memory/*.md" -type f \
  -newermt "${TARGET_DATE}" ! -newermt "${TARGET_DATE} +1 day" 2>/dev/null | while read -r f; do
  echo "  [MEM] $f"
done
echo ""

# 2. Sub-project .claude directories
echo "--- Sub-project .claude dirs ---"
find "$WORKDIR" -maxdepth 3 -type d -name ".claude" -not -path "*/.git/*" 2>/dev/null | while read -r d; do
  echo "  [DIR] $d"
done
echo ""

# 3. Files changed on target date (excluding .git, node_modules, .claude)
echo "--- Files Changed (${TARGET_DATE}) ---"
find "$WORKDIR" -type f \
  -newermt "${TARGET_DATE}" ! -newermt "${TARGET_DATE} +1 day" \
  -not -path "*/.git/*" \
  -not -path "*/node_modules/*" \
  -not -path "*/.claude/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/.playwright-mcp/*" \
  2>/dev/null | sort | while read -r f; do
  ext="${f##*.}"
  case "$ext" in
    md)   tag="DOC" ;;
    py|js|ts|go|java) tag="CODE" ;;
    json|csv|xlsx) tag="DATA" ;;
    yaml|yml|toml) tag="CONFIG" ;;
    *) tag="FILE" ;;
  esac
  echo "  [${tag}] $f"
done
echo ""

# 4. Existing work diaries
echo "--- Existing Work Diaries ---"
DIARY_DIR="${WORKDIR}/工作日记"
if [ -d "$DIARY_DIR" ]; then
  find "$DIARY_DIR" -name "*.md" -type f 2>/dev/null | sort | while read -r f; do
    echo "  [DIARY] $f"
  done
else
  echo "  (no 工作日记 directory found)"
fi
echo ""

# 5. Git commits on target date (if git repo)
echo "--- Git Commits (${TARGET_DATE}) ---"
if [ -d "$WORKDIR/.git" ]; then
  git -C "$WORKDIR" log --oneline --after="${TARGET_DATE} 00:00:00" \
    --before="${TARGET_DATE} 23:59:59" --all 2>/dev/null | while read -r line; do
    echo "  [GIT] $line"
  done
else
  for sub in "$WORKDIR"/*/; do
    if [ -d "$sub/.git" ]; then
      proj=$(basename "$sub")
      git -C "$sub" log --oneline --after="${TARGET_DATE} 00:00:00" \
        --before="${TARGET_DATE} 23:59:59" --all 2>/dev/null | while read -r line; do
        echo "  [GIT:${proj}] $line"
      done
    fi
  done
fi

echo ""
echo "=== Collection Complete ==="
