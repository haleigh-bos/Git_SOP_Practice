"""Tests for src/units.py.

Run either way from the repository root:
    python tests/test_units.py
    python -m pytest tests/        (if pytest is installed)
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

import units  # noqa: E402


def test_hartree_to_kcal():
    # CODATA 2018: 1 Eh = 627.509474 kcal/mol
    assert math.isclose(units.hartree_to_kcal(1.0), 627.509474, rel_tol=1e-6)


def test_hartree_to_kj():
    assert math.isclose(units.hartree_to_kj(1.0), 2625.499639, rel_tol=1e-6)


def test_hartree_to_ev():
    assert math.isclose(units.hartree_to_ev(1.0), 27.211386246, rel_tol=1e-6)


def test_bohr_to_angstrom():
    assert math.isclose(units.bohr_to_angstrom(1.0), 0.529177210903, rel_tol=1e-9)


def test_relative_energies_zero_for_minimum():
    rel = units.relative_energies([-1.0, -1.001, -0.999])
    assert min(rel) == 0.0
    assert math.isclose(rel[0], 0.001 * 627.509474, rel_tol=1e-6)


if __name__ == "__main__":
    tests = [obj for name, obj in sorted(globals().items()) if name.startswith("test_")]
    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASS  {test.__name__}")
        except AssertionError:
            failures += 1
            print(f"FAIL  {test.__name__}")
    print(f"\n{len(tests) - failures} passed, {failures} failed")
    sys.exit(1 if failures else 0)
