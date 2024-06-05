#!/usr/bin/env python
# coding: utf-8

# In[10]:


#General ase calculation setup script, use as per requirement
from ase.calculators.vasp import Vasp
import ase.io
from get_kpts import get_kpts_array
import os
import numpy as np

xtl = ase.io.read('POSCAR')

######### General settings for Vasp ###########
calc = Vasp()

kpar=6
npar=4

encut = 650

kpts = get_kpts_array(xtl, 4000) 

static = True
relax = False
is_dos = False
is_bs_run1 = False
is_bs_run2 = False
is_spin_polarized = True
is_phonon = True

#INCAR tags
calc.set(xc='PBE', setups= 'recommended', prec='Accurate', algo = 'Normal', encut = encut, kpts = kpts, gamma=True,
        kpar = kpar, npar = npar, sigma = 0.05, lmaxmix = 4,lasph = True,lorbit = 11, enaug = 4*encut, ediff = 10**(-6), ediffg = -5*10**(-4))

#DFT+U settings

calc.set(ldau = True, ldautype = 2, ldauu = [0.5, 0.0, 0.0])

if is_spin_polarized:
    
    calc.set(ispin=2)
    magmom_values = np.zeros(len(xtl.get_chemical_symbols()))

    for symbol,index in zip(xtl.get_chemical_symbols(),range(0,len(xtl.get_chemical_symbols()))):
    
    	if symbol is 'Ti':
        	magmom_values[index] = 2
        
    	else:
        	magmom_values[index] = 0
    
    xtl.set_initial_magnetic_moments(magmom_values)


if is_dos:
        static = True
        calc.set(ismear = -5, sigma = 0.150, isym = 1, nedos = 4001, emin = -20, emax = 20) #dos calculations are static so remember to set static as true

if is_bs_run1:
        static = True
        calc.set(lreal = False, lwave = True, lcharge = True)

if is_bs_run2:
        static = True
        calc.set(algo ='Normal',lreal = False, icharg = 11,lcharg = False)
        bl=xtl.cell.get_bravais_lattice()
        path= bl.bandpath(npoints = 112)
        calc.set(kpts=path.kpts, reciprocal = True)
        

if is_phonon:
        static = True
        scell = [2,2,2]
        kpts = [i/j for i,j in zip(kpts,scell)]
        calc.set(enaug=1, kpts=kpts, ismear = 1, addgrid = True)

if static:
    calc.set(nsw=0)

if relax:
    calc.set(nsw=100,isif=3, ibrion=AAA)





xtl.calc=calc #or you could use calc = xtl.calc
xtl.get_potential_energy()

if not(is_bs_run1 or is_bs_run2):
    if os.path.isfile('WAVECAR'):
        os.remove('WAVECAR')


# In[ ]:





# In[ ]:




