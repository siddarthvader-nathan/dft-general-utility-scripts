
# coding: utf-8

# In[10]:


#General ase calculation setup script, use as per requirement
from ase.calculators.vasp import Vasp
import ase.io
from get_kpts import get_kpts_array
import os
import numpy as np
import shutil


######### General settings for Vasp ###########

kpar=8
ncore=8

encut = 650


static = False
relax = True
is_dos = False
is_bs_run1 = False
is_bs_run2 = False
is_spin_polarized = True
is_phonon = False
is_ib1 = tbd

if is_ib1:
    calc_run = Vasp(restart = True)
    xtl = calc_run.get_atoms()
    xtl.set_initial_magnetic_moments(calc_run.get_magnetic_moments())
    ase.io.write("POSCAR_after_ib2",xtl,direct=True)
    shutil.copy('POSCAR_after_ib2','POSCAR')
    calc = Vasp()
    calc.set(icharg=1)
else:
    ref_atoms = ase.io.read('POSCAR.orig')
    xtl = ase.io.read('POSCAR')
    calc = Vasp()

kpts = get_kpts_array(xtl, 4000) 

#INCAR tags
calc.set(xc='PBESOL', setups= 'recommended', nelmin = 5, prec='Accurate', 
         algo = 'Normal', encut = encut, kpts = kpts, gamma=True, kpar = kpar, 
         ncore = ncore, sigma = 0.05, lmaxmix = 4,lasph = True,lorbit = 11, enaug = 4*encut,
           ediff = 10**(CCC), ediffg = -5*10**(-3), amix = 0.2, bmix = 0.0001, amix_mag = 0.8, 
           bmix_mag = 0.0001, icharg=1)

#DFT+U settings
#calc.set(ldau = True, ldautype = 2, ldauu = [0.2, 0.0, 0.0])

if is_spin_polarized:    
    calc.set(ispin=2)
    if not is_ib1:
        magmoms = np.zeros(len(xtl))  # Initialize all magnetic moments to 0
        symbols = np.array(xtl.get_chemical_symbols())
        Fe_pos = np.argwhere(symbols == 'Fe').flatten()  # Find positions of Fe atoms    
        magmoms[Fe_pos[::2]] = 3  # Even-indexed Fe atoms
        magmoms[Fe_pos[1::2]] = -3 # Odd-indexed Fe atoms3
        xtl.set_initial_magnetic_moments(magmoms)

if is_dos:
        static = True
        calc.set(ismear = -5, sigma = 0.150, isym = 1, nedos = 4001, emin = -20, emax = 20) #dos calculations are static so remember to set static as true

if is_bs_run1:
        static = True
        calc.set(lreal = False, lwave = True, lcharg = True)

if is_bs_run2:
        static = True
        calc.set(algo ='Normal',lreal = False, icharg = 11,lcharg = False)
        bl=xtl.cell.get_bravais_lattice()
        path= bl.bandpath(npoints = 112)
        calc.set(kpts=path.kpts, reciprocal = True)
        

if is_phonon:
        static = True
        calc.set(enaug=1, kpts=kpts, ismear = 1, addgrid = True,ediff = 10**(-8), ediffg = None)

if static:
    calc.set(nsw=0)

if relax:
    calc.set(nsw=100,isif=3, ibrion=AAA)

xtl.calc=calc #or you could use calc = xtl.calc
xtl.get_potential_energy()

if not(is_bs_run1 or is_bs_run2):
    if os.path.isfile('WAVECAR'):
        os.remove('WAVECAR')
