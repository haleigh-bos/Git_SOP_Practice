#!/usr/bin/env bash
# Pretend to run a quantum chemistry job so you can practice with .gitignore.
# It creates the kinds of files a real calculation leaves behind: an input
# (worth tracking) plus logs, checkpoints, scheduler output, and scratch files
# (usually NOT worth tracking).
#
# Usage (from the repository root):
#     bash scripts/fake_calculation.sh

set -euo pipefail

RUN_DIR="runs/water_opt"
mkdir -p "$RUN_DIR/scratch"

# The input file: small, human-written, and essential for reproducibility -> TRACK
cat > "$RUN_DIR/water_opt.inp" << 'INP'
! B3LYP D3BJ 6-31G(d) Opt TightSCF
* xyzfile 0 1 ../../data/molecules/water.xyz
INP

# Outputs and scratch: regenerable, often large -> IGNORE
echo "FINAL SINGLE POINT ENERGY      -76.408953 (fake value for practice)" > "$RUN_DIR/water_opt.log"
head -c 524288 /dev/zero > "$RUN_DIR/water_opt.chk"      # 512 KB fake checkpoint
head -c 262144 /dev/zero > "$RUN_DIR/water_opt.gbw"      # 256 KB fake wavefunction
echo "Job 123456 finished" > "$RUN_DIR/slurm-123456.out"
for i in 1 2 3; do head -c 65536 /dev/zero > "$RUN_DIR/scratch/tmp_integrals_$i.tmp"; done

echo "Fake calculation finished. Files created in $RUN_DIR:"
ls -lh "$RUN_DIR" "$RUN_DIR/scratch"
echo
echo "Now run:  git status"
