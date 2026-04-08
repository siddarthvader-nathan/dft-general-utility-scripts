#!/usr/bin/env python3
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import sys

def vasp_to_symmetrized_cif(input_vasp, output_cif, symprec=1e-3, angle_tolerance=5.0):
    # Read structure from VASP file
    structure = Structure.from_file(input_vasp)

    # Analyze symmetry and get standardized symmetrized structure
    sga = SpacegroupAnalyzer(
        structure,
        symprec=symprec,
        angle_tolerance=angle_tolerance,
    )
    symmetrized = sga.get_refined_structure()

    # Write CIF
    symmetrized.to(filename=output_cif)

    print(f"Wrote symmetrized CIF to: {output_cif}")
    print(f"Space group: {sga.get_space_group_symbol()} ({sga.get_space_group_number()})")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python vasp_to_cif.py input.vasp output.cif [symprec]")
        sys.exit(1)

    input_vasp = sys.argv[1]
    output_cif = sys.argv[2]
    symprec = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-3

    vasp_to_symmetrized_cif(input_vasp, output_cif, symprec=symprec)
