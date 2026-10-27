#!/usr/bin/env bash
# Write a small provenance file recording exactly which version of the code
# was used for a calculation. Call it at the top of every job script.
#
# Usage:
#     bash scripts/record_provenance.sh [output_dir]

set -euo pipefail

OUT_DIR="${1:-.}"
OUT_FILE="$OUT_DIR/provenance.txt"
REPO_ROOT="$(git rev-parse --show-toplevel)"

{
    echo "date:        $(date -Iseconds)"
    echo "host:        $(hostname)"
    echo "user:        ${USER:-unknown}"
    echo "repository:  $(git -C "$REPO_ROOT" config --get remote.origin.url || echo 'no remote')"
    echo "branch:      $(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)"
    echo "commit:      $(git -C "$REPO_ROOT" rev-parse HEAD)"
    if git -C "$REPO_ROOT" diff --quiet && git -C "$REPO_ROOT" diff --cached --quiet; then
        echo "clean:       yes (no uncommitted changes)"
    else
        echo "clean:       NO - uncommitted changes present; results may not be reproducible"
    fi
} > "$OUT_FILE"

cat "$OUT_FILE"
