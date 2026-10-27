"""Relative energies and Boltzmann populations for a set of conformers.

Usage (from the repository root):
    python src/analyze_energies.py data/energies.csv
    python src/analyze_energies.py data/energies.csv --temperature 350
"""

import argparse
import csv
import math

from units import relative_energies

#: Boltzmann constant in kcal/(mol K)
KB_KCAL_MOL_K = 0.0019872043


def load_energies(path):
    """Read a CSV with columns 'conformer' and 'energy_hartree'."""
    names, energies = [], []
    with open(path, newline="") as handle:
        for row in csv.DictReader(handle):
            names.append(row["conformer"])
            energies.append(float(row["energy_hartree"]))
    return names, energies


def boltzmann_populations(rel_kcal, temperature=298.15):
    """Return fractional populations from relative energies in kcal/mol."""
    weights = [math.exp(-e / (KB_KCAL_MOL_K * temperature)) for e in rel_kcal]
    total = sum(weights)
    return [w / total for w in weights]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("csv_file")
    parser.add_argument("--temperature", type=float, default=298.15,
                        help="Temperature in K (default 298.15)")
    args = parser.parse_args()

    names, energies = load_energies(args.csv_file)
    rel = relative_energies(energies, unit="kcal/mol")
    pops = boltzmann_populations(rel, args.temperature)

    print(f"T = {args.temperature:.2f} K")
    print(f"{'Conformer':<22}{'dE (kcal/mol)':>15}{'Population':>13}")
    for name, e, p in sorted(zip(names, rel, pops), key=lambda x: x[1]):
        print(f"{name:<22}{e:>15.3f}{p * 100:>12.1f}%")


if __name__ == "__main__":
    main()
