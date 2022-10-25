#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import DosPlotter
from pymatgen.electronic_structure.core import Orbital,OrbitalType
from pymatgen.electronic_structure.dos import Dos


def get_total_dos(v):
    
    tdos=v.tdos
    return tdos


def get_elem_pdos(element,orbital_name,v):
    
    cdos = v.complete_dos
    
    for orb_type in OrbitalType:
        if orb_type is OrbitalType[orbital_name]:
            elem_dos=cdos.get_element_spd_dos(element)
            proj_dos=elem_dos[orb_type]
            
    return proj_dos


def get_elem_orb_pdos(element,orbital_name,v):
    
    cdos = v.complete_dos
    orb_pdos_list = []
    
    
    for site_finder_flag in cdos.structure:
            for elem_name in site_finder_flag.species.elements:
                if elem_name.name is element:
                    site=site_finder_flag
     
    
    for orb_finder_flag in Orbital:
            if orb_finder_flag.orbital_type.name is orbital_name:
                projected_orbital=orb_finder_flag
                orbital_dos = cdos.get_site_orbital_dos(site,projected_orbital)
                orb_pdos_list.append(orbital_dos)   
           
    return orb_pdos_list
    
   

    

# In[ ]:



