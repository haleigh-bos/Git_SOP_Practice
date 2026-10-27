"""Small utilities for reading and summarizing XYZ geometry files.

Usage (from the repository root):
    python src/xyz_tools.py data/molecules/water.xyz
    python src/xyz_tools.py data/molecules/*.xyz
"""

import sys

# Standard atomic weights (g/mol) for common elements
ATOMIC_MASSES = {
    "H": 1.008, "He": 4.0026, "Li": 6.94, "B": 10.81, "C": 12.011,
    "N": 14.007, "O": 15.999, "F": 18.998, "Na": 22.990, "Mg": 24.305,
    "Si": 28.085, "P": 30.974, "S": 32.06, "Cl": 35.45, "Br": 79.904,
    "I": 126.90,
}


def read_xyz(path):
    """Read an XYZ file and return (symbols, coordinates, comment)."""
    with open(path) as handle:
        lines = handle.read().splitlines()
    n_atoms = int(lines[0].strip())
    comment = lines[1].strip()
    symbols, coords = [], []
    for line in lines[2:2 + n_atoms]:
        parts = line.split()
        symbols.append(parts[0].capitalize())
        coords.append(tuple(float(x) for x in parts[1:4]))
    if len(symbols) != n_atoms:
        raise ValueError(f"{path}: expected {n_atoms} atoms, found {len(symbols)}")
    return symbols, coords, comment


def molecular_formula(symbols):
    """Return the formula in Hill order (C first, then H, then alphabetical)."""
    counts = {}
    for s in symbols:
        counts[s] = counts.get(s, 0) + 1
    order = []
    if "C" in counts:
        order += ["C"] + (["H"] if "H" in counts else [])
    order += sorted(k for k in counts if k not in order)
    return "".join(f"{el}{counts[el] if counts[el] > 1 else ''}" for el in order)


def molecular_mass(symbols):
    """Return the molecular mass in g/mol."""
    return sum(ATOMIC_MASSES[s] for s in symbols)


def center_of_mass(symbols, coords):
    """Return the center of mass (x, y, z) in the same units as coords."""
    total = molecular_mass(symbols)
    return tuple(
        sum(ATOMIC_MASSES[s] * c[i] for s, c in zip(symbols, coords)) / total
        for i in range(3)
    )


def summarize(path):
    """Print a short summary of one XYZ file."""
    symbols, coords, comment = read_xyz(path)
    com = center_of_mass(symbols, coords)
    print(f"File:      {path}")
    print(f"Comment:   {comment}")
    print(f"Atoms:     {len(symbols)}")
    print(f"Formula:   {molecular_formula(symbols)}")
    print(f"Mass:      {molecular_mass(symbols):.3f} g/mol")
    print(f"COM (A):   {com[0]:.4f} {com[1]:.4f} {com[2]:.4f}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/xyz_tools.py FILE.xyz [FILE2.xyz ...]")
        sys.exit(1)
    for xyz_file in sys.argv[1:]:
        summarize(xyz_file)
        print()
