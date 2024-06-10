# Setup and utility scripts for DFT calculations

Makes use of  the following libraries:
1. https://wiki.fysik.dtu.dk/ase/index.html
2. https://pymatgen.org

Vasp_post_processing:
1. dos_plotting: Contains helper functions for plotting total, site and orbital projected density of states 
2. band_structure: Band structure plotting using atomic smulation environment (ASE)
3. bs_plot: Band structure plot of a line mode VASP non self consistent field calculation using pymatgen

Calc-seed_script
1. get_kpts: Gets a gamma centered kmesh of required kpoint density, measured by kpoints per reciprocal atom (KPRA).
2. job scripts for different compute clusters
3. calc: ASE VASP setup script, flexible to customization of strutures using ASE, as well as VASP calculation parameters such as individual magnetic moments.
