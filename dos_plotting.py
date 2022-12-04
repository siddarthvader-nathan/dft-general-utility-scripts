from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import DosPlotter
from pymatgen.electronic_structure.core import Orbital,OrbitalType,Spin
import sys
import numpy as np


class DosExtractor():
    
    def __init__(self,vasprun_file = 'vasprun.xml'):
    
        self.vasprun = Vasprun(vasprun_file)
    
        """
        Args:
        1. vasprun_file: vasprun.xml by default but whatever you named it to be        
        """

    def get_total_dos(self,scaling_factor=1):    
      
        """
        Extracts total density of states 
        Args: 
        1. factor(int): set by default to 1, if not, scales tdos to units of eV/FU
        Returns: 
        tdos: total density of states pymatgen dos object to add to self.dos_plotter"""

        tdos=self.vasprun.tdos
        
        if scaling_factor != 1:
          tdos = self.scale(scaling_factor)
        
        return tdos


    def get_elem_dos(self,element):

        """
        Extracts elemental contribution to dos.        

        Args:
        element(str): name of element we want to look at dos of 
        
        Returns:
        elem_dos: pymatgen dos object, e.g. Ti total contribution to dos

        """
        cdos = self.vasprun.complete_dos 

        for key in cdos.get_element_dos().keys():
            if key.name is element:
                elem_dos = cdos.get_element_dos()[key]
            
        return elem_dos

    

    def get_elem_pdos(self,element,orbital_name):

        """         
        Extracts orbital projection of elemental contribution to dos.
       
        Args:        
        1. element(str): name of element we want to look at dos of, eg. Ti
        2. orbital_name(str): name of atomic orbital e.g. 'd' 
        Returns:

        elem_proj_dos: pymatgen dos object, e.g. Ti-3d contribution
        """        

        cdos = self.vasprun.complete_dos   

        for orb_type in OrbitalType:
            if orb_type is OrbitalType[orbital_name]:
                elem_dos=cdos.get_element_spd_dos(element)
                elem_proj_dos=elem_dos[orb_type]
            
        return elem_proj_dos

       
    def get_elem_orb_pdos(self,element,orbital_name): 

        """returns individual orbital projection of elemental contribution to dos, e.g. Ti dxy,dyz etc.

        Args:
        1. element(str): name of element we want to look at dos of, eg. Ti
        2. orbital_name(str): name of atomic orbital e.g. 'd'   
        
        Returns:
        orb_pdos: np array of all projected individual orbutal contributions to dos e.g. Ti dxy,dyz,dxz,dz2,dx2-y2"""
            
        cdos = self.vasprun.complete_dos
        orb_pdos = np.zeros(len(Orbital))

        for site_finder_flag in cdos.structure:
                for elem_name in site_finder_flag.species.elements:
                    if elem_name.name is element:
                        site=site_finder_flag
         
        for idx,orb_finder_flag in enumerate(Orbital):
                if orb_finder_flag.orbital_type.name is orbital_name:
                    projected_orbital = orb_finder_flag
                    orbital_dos = cdos.get_site_orbital_dos(site,projected_orbital)
                    orb_pdos[idx] = orbital_dos   
        
        return orb_pdos
       
    def scale(self,scaling_factor):
     
     """Scales tdos to units of eV^{-1} FU^{-1}.
     
     Args:
     1. factor(int): scaling factor i.e. size of unit cell
     """
     
     tdos = self.vasprun.tdos     
     for key in tdos.densities.keys():
        tdos.densities[key]/= scaling_factor
       
     return tdos



