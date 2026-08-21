#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
fail=0
need() { if [[ ! -e "$1" ]]; then echo "MISSING $1"; fail=1; else echo "OK $1"; fi; }

echo "== canon =="
need "$ROOT/character/references/alice-master-face.jpg"
need "$ROOT/GROK_CONTEXT_AND_LOG.md"
need "$ROOT/PROJECT_INSTRUCTIONS.md"
need "$ROOT/character/visual-rules.md"
need "$ROOT/prompts/identity-lock.md"

declare -a REELS=(
  "001-first-date:001"
  "002-bad-date-home:002"
  "003-morning-after:003"
  "004-who-knows:004"
)

for item in "${REELS[@]}"; do
  dir="${item%%:*}"
  num="${item##*:}"
  echo "== reels $num =="
  base="$ROOT/content/reels/$dir"
  need "$base/output/approved/reels-${num}-approved.mp4"
  need "$base/concept.md"
  need "$base/prompt-grok.md"
  need "$base/storyboard.md"
  need "$base/result-notes.md"
  mp4="$base/output/approved/reels-${num}-approved.mp4"
  if [[ -f "$mp4" ]] && command -v ffprobe >/dev/null; then
    ffprobe -v error -show_entries format=duration -show_entries stream=width,height -of default=nw=1 "$mp4" || true
    sha256sum "$mp4"
  fi
done

if grep -q 'alice-master-face-v2' "$ROOT/character/visual-rules.md" && grep -q 'alice-master-face.jpg' "$ROOT/GROK_CONTEXT_AND_LOG.md"; then
  echo "WARN canon conflict: visual-rules v2 vs GROK_CONTEXT v1"
  fail=1
fi

exit "$fail"
