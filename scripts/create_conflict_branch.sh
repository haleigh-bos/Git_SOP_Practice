#!/usr/bin/env bash
# Backup setup for Exercise 6 (merge conflict), for copies of the repository
# that were created without the exercise/conflict branch.
#
# It creates a local branch that changes the basis set one way, then changes
# main a different way, so merging the two produces a conflict.
#
# Usage (from the repository root, on a clean working tree):
#     bash scripts/create_conflict_branch.sh

set -euo pipefail

if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "You have uncommitted changes. Commit them or run 'git restore .' first."
    exit 1
fi

CFG="config/calc_settings.yaml"

git switch main
git switch -c exercise/conflict-local
sed -i.bak 's/^basis: .*/basis: def2-TZVP/' "$CFG"
sed -i.bak 's/^max_scf_cycles: .*/max_scf_cycles: 500/' "$CFG"
rm -f "$CFG.bak"
git commit -q -am "Use larger def2-TZVP basis for production runs"

git switch main
sed -i.bak 's/^basis: .*/basis: def2-SVP/' "$CFG"
rm -f "$CFG.bak"
git commit -q -am "Use def2-SVP for quick screening runs"

echo
echo "Ready. Now run:   git merge exercise/conflict-local"
