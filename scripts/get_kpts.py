import ase.io
import numpy as np

def get_kpts_array(atoms,desired_kpra):
"""atoms: ASE atoms object, desired_kpra(int): K-points per reciprocal atom"""

"""Get real space lattice vectors"""
    a1 = atoms.cell[0]
    a2 = atoms.cell[1]
    a3 = atoms.cell[2]

"""Calculate reciprocal lattice vectros"""
    b1 = 2 * np.pi* (np.cross(a2,a3))/ np.dot(a1,np.cross(a2,a3))
    b2 = 2 * np.pi* (np.cross(a3,a1))/ np.dot(a2,np.cross(a3,a1))
    b3 = 2 * np.pi* (np.cross(a1,a2))/ np.dot(a3,np.cross(a1,a2))

"""Initial guess"""
    kpts_raw = 10*np.array([np.linalg.norm(b1,2),np.linalg.norm(b2,2),np.linalg.norm(b3,2)])
    kpts = np.round(kpts_raw,0)

"""Scaling for appropriate k-point density"""
    kpra_less = True
    kpra_more = True

    while(kpra_less or kpra_more):
        
        if (len(atoms) * np.prod(kpts) < desired_kpra):
            kpra_more = False
            if(kpra_less):
                kpts = kpts + 1
        
        else:
            kpra_less = False
            if(kpra_more):
                kpts = kpts - 1
    
    return kpts
