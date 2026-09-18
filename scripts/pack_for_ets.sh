#!/usr/bin/env bash
# Build a single ZIP for ETS-Data upload (excludes .git and caches).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$(cd "$ROOT/.." && pwd)"
ZIP_NAME="JICV-2026-0031_AHP_analyse_replication.zip"
cd "$ROOT"
rm -f "$OUT_DIR/$ZIP_NAME"
zip -r "$OUT_DIR/$ZIP_NAME" . \
  -x "./.git/*" \
  -x "./.venv/*" \
  -x "./venv/*" \
  -x "./__pycache__/*" \
  -x "./src/__pycache__/*" \
  -x "./scripts/__pycache__/*" \
  -x "./.DS_Store" \
  -x "./output/images/*.pdf" \
  -x "./output/images/*.png"
echo "Created: $OUT_DIR/$ZIP_NAME"
ls -lh "$OUT_DIR/$ZIP_NAME"
echo "Remember to fill author emails in REPLICATION_EXPLANATORY_FILE.md before upload."
