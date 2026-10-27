#!/usr/bin/env bash
#SBATCH --job-name=water_opt
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=01:00:00
#SBATCH --output=slurm-%j.out
#
# Example SLURM job script showing how to record the Git commit that produced
# a result. Adapt the module names and program call for your cluster.
#
# Submit from the repository root:   sbatch scripts/submit_job.sh

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"

RUN_DIR="runs/water_opt"
mkdir -p "$RUN_DIR"

# 1. Record exactly which code version is being used
bash scripts/record_provenance.sh "$RUN_DIR"

# 2. Load software (names differ between clusters)
# module load orca

# 3. Run the calculation
# orca "$RUN_DIR/water_opt.inp" > "$RUN_DIR/water_opt.log"
echo "This is a template: uncomment the module and program lines for a real run."
