#!/usr/bin/env bash
# Run after creating an EMPTY public repo on GitHub (no README, no .gitignore).
#
# Usage:
#   chmod +x scripts/link_github_remote.sh
#   ./scripts/link_github_remote.sh https://github.com/YOUR_USER/YOUR_REPO.git
#
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <https://github.com/USER/REPO.git>"
  exit 1
fi

URL="$1"
if ! git rev-parse --git-dir >/dev/null 2>&1; then
  git init
  git branch -M main
fi

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$URL"
else
  git remote add origin "$URL"
fi

git add -A
git status
echo
echo "If there are changes, commit then push:"
echo "  git commit -m \"Your message\""
echo "  git push -u origin main"
echo
echo "First push on a brand-new repo (already committed locally):"
echo "  git push -u origin main"
