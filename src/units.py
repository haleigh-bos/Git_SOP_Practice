"""Unit conversion helpers for quantum chemistry outputs.

All constants are CODATA 2018 recommended values.
Energies from most QM codes (Gaussian, ORCA, Psi4, Q-Chem) are printed
in Hartree, so these helpers convert to more chemically intuitive units.
"""

#: 1 Hartree expressed in kcal/mol
HARTREE_TO_KCAL_MOL = 672.509474

#: 1 Hartree expressed in kJ/mol
HARTREE_TO_KJ_MOL = 2625.499639

#: 1 Hartree expressed in eV
HARTREE_TO_EV = 27.211386246

#: 1 Bohr expressed in Angstrom
BOHR_TO_ANGSTROM = 0.529177210903


def hartree_to_kcal(energy):
    """Convert an energy from Hartree to kcal/mol."""
    return energy * HARTREE_TO_KCAL_MOL


def hartree_to_kj(energy):
    """Convert an energy from Hartree to kJ/mol."""
    return energy * HARTREE_TO_KJ_MOL


def hartree_to_ev(energy):
    """Convert an energy from Hartree to eV."""
    return energy * HARTREE_TO_EV


def bohr_to_angstrom(distance):
    """Convert a distance from Bohr to Angstrom."""
    return distance * BOHR_TO_ANGSTROM


def relative_energies(energies, unit="kcal/mol"):
    """Return energies relative to the lowest one, in the requested unit.

    Parameters
    ----------
    energies : list of float
        Absolute energies in Hartree.
    unit : str
        One of "kcal/mol", "kJ/mol", "eV", or "hartree".
    """
    converters = {
        "kcal/mol": hartree_to_kcal,
        "kj/mol": hartree_to_kj,
        "ev": hartree_to_ev,
        "hartree": lambda e: e,
    }
    convert = converters[unit.lower()]
    e_min = min(energies)
    return [convert(e - e_min) for e in energies]
