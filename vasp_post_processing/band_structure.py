#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
from ase.calculators.vasp import Vasp
from ase.spectrum.band_structure import get_band_structure
import ase.io


calc_nscf = Vasp(restart=True, directory='./bs_nscf')
calc_scf = Vasp(restart=True, directory='./bs_scf')
efermi=calc_scf.fermi

atoms = ase.io.read('./bs_nscf/POSCAR')
bl = atoms.cell.get_bravais_lattice()
path = bl.special_path


def plot_bs(calc_nscf,calc_scf,efermi):
   
    emin,emax=-7,7 #whatever you need this value to be
    
    ## Read the bands from the NSCF

    bs_raw = get_band_structure(calc=calc_nscf,reference=efermi)
    # adjust eigenvalues to be relative to the fermi level
    bs = bs_raw.subtract_reference()

    
    #bs=calc_nscf.band_structure()
    #bs._energies-=efermi
    #bs._reference=0
    
    fig, ax = plt.subplots(figsize=(8,6), dpi=192)

    bs.plot(ax = ax, show = False, emin=emin, emax=emax)

    ax.minorticks_on()
    ax.tick_params(axis = 'x', which = 'minor', bottom = False)
    ax.tick_params(axis = 'y', which = 'minor', left = True)
    fig.tight_layout(pad = 0.2)

    return fig, ax, bs








