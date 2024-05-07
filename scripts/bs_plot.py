from pymatgen.io.vasp import BSVasprun
from pymatgen.electronic_structure.plotter import BSPlotter

def get bs_plot(vasprun_file = 'bs_vasprun.xml', kpoints_file = 'KPOINTS_bs', ylim  = (-1,1)):
 
	v = BSVasprun(vasprun_file)
	bs = v.get_band_structure(kpoints_filename = kpoints_file, line_mode = True)
	plt = BSPlotter(bs)
	p = plt.get_plot(vbm_cbm_marker = True, ylim = ylim,bs_labels = ["spin"])
	p.tick_params(axis='x',labelsize=24)
	p.tick_params(axis='y',labelsize=24)
	p.xlabel('Wave Vector',fontsize=24)
	p.ylabel('Energy(eV)',fontsize=24)
	
	return p
