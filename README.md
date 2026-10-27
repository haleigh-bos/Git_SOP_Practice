# Git_SOP_Practice
A practice repository that teach the basics of how to use git for computational chemistry groups. 

## What's inside

| Path | What it is |
|---|---|
| `EXERCISES.md` | **Start here.** Step-by-step exercises, from your first commit to resolving a merge conflict |
| `src/units.py` | Hartree / kcal/mol / kJ/mol / eV conversion helpers (contains a deliberate bug for Exercise 3) |
| `src/xyz_tools.py` | Reads XYZ files and prints formula, mass, and center of mass |
| `src/analyze_energies.py` | Relative conformer energies and Boltzmann populations |
| `tests/test_units.py` | Tests for `units.py` (run with `python tests/test_units.py`) |
| `data/molecules/` | Example XYZ geometries |
| `data/energies.csv` | Example conformer energies in Hartree (illustrative values) |
| `config/calc_settings.yaml` | Calculation settings (used in the merge-conflict exercise) |
| `scripts/fake_calculation.sh` | Creates fake calculation outputs for the `.gitignore` exercise |
| `scripts/record_provenance.sh` | Records the exact Git commit used for a calculation |
| `scripts/submit_job.sh` | Example SLURM job script that records provenance |
| `scripts/create_conflict_branch.sh` | Backup way to set up the merge-conflict exercise |
| `members/` | Everyone adds a file about themselves here |

## Quick start

```bash
# 1. Get your own copy on GitHub (see EXERCISES.md, Exercise 0), then:
git clone git@github.com:YOUR-USERNAME/git-practice-compchem.git
cd git-practice-compchem

# 2. Try the tools
python src/xyz_tools.py data/molecules/*.xyz
python src/analyze_energies.py data/energies.csv
python tests/test_units.py        # two tests fail on purpose - see Exercise 3
```

Requirements: Git 2.23 or newer and Python 3.8 or newer. No extra Python
packages are needed.

## Branches and tags in this repository

- `main` is the default branch.
- `exercise/conflict` is a branch that deliberately conflicts with `main`
  (used in Exercise 6). Do not merge it into the group's shared copy.
- `v0.1` is a tag marking an early version of the project, before the bug in
  `units.py` was introduced (used in Exercises 3 and 8).

## Where to learn more

See the Liu group's Git SOP document for full explanations, conventions, and
troubleshooting help.

*This repository was developed by Haleigh Bos Muyskens. Claude was used to generate example data and files.*
