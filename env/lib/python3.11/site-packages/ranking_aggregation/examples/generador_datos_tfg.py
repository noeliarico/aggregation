import numpy as np
import pandas as pd
import sys
sys.path.append('./preferences')
sys.path.append('./generators')
sys.path.append('./ranking_rules')
from generate import preference_matrix, generate_profile_factoradic
from ranking import from_int_to_ranking, print_ranking
from condorcet import condorcet, condorcet_winner
from kemeny import kemeny

ns = [6] # [4, 5]
ms = [9, 10, 49, 50, 99, 100]
ptypes = ['nc', 'cw', 'cr']

for n in ns:
    for m in ms:
        for ptype in ptypes:
            file_name = 'perfiles_tfg_'+str(n)+'_'+str(m)+'_'+ptype
            with open(file_name+'.npy', 'rb') as f:
                profiles = np.load(f)
            df = pd.DataFrame(columns=('n', 'm', 'ptype', 'best_distance', 'nsolutions'))
            for i in range(len(profiles)):
                p = profiles[i]
                k = kemeny(p)
                df.loc[i] = [n, m, ptype, k['best_distance'], len(k['winners'])]    
            df.to_csv(file_name+'.csv', index=False)
            print(df)