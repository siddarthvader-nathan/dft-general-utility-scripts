#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import ase.io
import numpy as np


def get_kpts_array(atoms,desired_kpra):
    
    #Args- atoms:ase.Atoms object, desired_kpra:int
    
    lcf = min(atoms.cell.lengths())
    kpts_raw = lcf/atoms.cell.lengths()
    
    #Initial guess
    kpts = 10 * np.array([round(i,1) for i in kpts_raw])

    kpra_less = 1
    kpra_more = 1

    while(kpra_less or kpra_more):
    
        if (len(atoms) * np.prod(kpts) < desired_kpra):
            kpra_more = 0
            kpts = kpts + 1
    
        else:
            kpra_less = 0
            kpts = kpts - 1
        
    return kpts

