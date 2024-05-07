import ase.io
import numpy as np

def get_kpts_array(atoms,desired_kpra):

    a1 = atoms.cell[0]
    a2 = atoms.cell[1]
    a3 = atoms.cell[2]
    
    b1 = 2 * np.pi* (np.cross(a2,a3))/ np.dot(a1,np.cross(a2,a3))
    b2 = 2 * np.pi* (np.cross(a3,a1))/ np.dot(a2,np.cross(a3,a1))
    b3 = 2 * np.pi* (np.cross(a1,a2))/ np.dot(a3,np.cross(a1,a2))

    kpts_raw = 5*np.array([np.linalg.norm(b1,2),np.linalg.norm(b2,2),np.linalg.norm(b3,2)])
    kpts_orig = np.rint(kpts_raw)
    kpts = np.copy(kpts_orig)
   
    
    kpra_less = True
    kpra_more = True

    print(np.array([np.linalg.norm(b1,2),np.linalg.norm(b2,2),np.linalg.norm(b3,2)]),kpts_raw,kpts)    
   

    while(kpra_less or kpra_more):
        
        kpra_start = len(atoms) * np.prod(kpts)
        
        if (kpra_start < desired_kpra):
            kpra_more = False
            if np.abs(kpra_start - desired_kpra) <=500:
                kpra_less = False
            else:
                kpts = kpts + 1
        else:
            kpra_less = False
            if np.abs(kpra_start - desired_kpra) <=500:
                kpra_more = False
            else:
                kpts = kpts -1
        
    return kpts
