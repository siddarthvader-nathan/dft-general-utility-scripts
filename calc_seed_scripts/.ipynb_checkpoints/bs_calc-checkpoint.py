
from ase.calculators.vasp import Vasp
import ase.io
#from ase.lattice import ORC

xtl = ase.io.read('POSCAR')

######### General settings for Vasp ###########
calc = Vasp()

kpar=4 
npar=1 

encut = 650            
kpts=[4,4,6] 


#specify type of calculation here
static = True
relax = not(static)
is_dos = False
is_bs_run1 = False
is_bs_run2 = True
is_spin_polarized = True


#INCAR tags
calc.set(xc='PBE', setups= 'recommended', prec='Accurate', algo = 'Normal', encut = encut, gamma=True,
        kpar = kpar, npar = npar, sigma = 0.05, lmaxmix = 4,lasph = True,lorbit = 11, enaug = 4*encut, ediff = 10**(-6)) 

if static:
    calc.set(nsw=0)

if relax:
	calc.set(isif=3, ibrion=2)

    
if is_dos:
    calc.set(ismear = -5, sigma = 0.150, isym = 1, nedos = 4001, emin = -20, emax = 20) #dos calculations are static so remember to set static as true

if is_bs_run1:
    calc.set(lreal = False, lwave = True, lcharg = True)

if is_bs_run2:
	calc.set(algo ='Normal',lreal = False, icharg = 11,lcharg = False, ismear = 0,kpar = 7)
	bl=xtl.cell.get_bravais_lattice()   
	path= bl.bandpath(npoints = 112)
	calc.set(kpts=path.kpts, reciprocal = True)
	#path=ORC(2.9976080230344935,4.8664940093990419,4.8720565709930632).bandpath()
	#kpts = path.kpts
	#calc.set(kpts=kpts)



if is_spin_polarized:
    calc.set(ispin=2)
    xtl.set_initial_magnetic_moments([2,2,0,0,0,0])


xtl.calc = calc
xtl.get_potential_energy()










