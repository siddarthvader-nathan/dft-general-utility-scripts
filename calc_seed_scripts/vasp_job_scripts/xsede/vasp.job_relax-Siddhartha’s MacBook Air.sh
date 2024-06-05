#!/bin/bash
#SBATCH -J TiOF             # job name
#SBATCH -o TiOF_fac.o%j           # output and error file name (%j expands to jobID) 
#SBATCH -e TiOF_fac.e%j           # output and error file name (%j expands to jobID)
#SBATCH -N 4
#SBATCH --ntasks-per-node 48                  # total number of mpi tasks requested
#SBATCH -p skx-dev              # queue (partition) -- normal, development, etc.
#SBATCH -t 2:00:00            # wall time (hh:mm:ss)
#SBATCH -A TG-MAT220044         # which account to debit hours from
#SBATCH --mail-user=siddharthanathan2026@u.northwestern.edu
#SBATCH --mail-type=begin      # email when job starts
#SBATCH --mail-type=end        # email when job ends


module load vasp/5.4.4

export VASP_COMMAND="ibrun vasp_std"
export VASP_PP_PATH="/home1/09029/tg883286/pseudopotentials"
 
cp POSCAR POSCAR.orig
mkdir std_outs


        for j in 2 1; do
                cp calc.py calc_ib${j}.py

                sed -i -e "s/AAA/$j/g" calc_ib${j}.py

                if [ $j == 1 ]; then
                        sed -i -e "s/10**(-8)/10**(-6)/g" calc_ib${j}.py

                fi

                python3 calc_ib${j}.py
                cp CONTCAR POSCAR
                cp vasp.out vasp.out_ib${j}
                mv vasp.out_ib${j} ./std_outs
        done
