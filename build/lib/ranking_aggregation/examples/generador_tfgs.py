import numpy as np
import sys
sys.path.append('./preferences')
sys.path.append('./generators')
sys.path.append('./ranking_rules')
from generate import preference_matrix, position_matrix, generate_profile_factoradic
from ranking import from_int_to_ranking, print_ranking
from condorcet import condorcet, condorcet_winner
from kemeny import kemeny


ns = [4,5,6]
ms = [10,11,49,50,99,100]
total = 50

for n in ns:
    for m in ms:
        
        types = np.empty(total*3, dtype="S2")
        
        total_cr = 0
        total_cw = 0
        total_nc = 0

        list_cr_om = []
        list_cw_om = []
        list_nc_om = []
        list_cr_pm = []
        list_cw_pm = []
        list_nc_pm = []
        list_cr_rankings = []
        list_cw_rankings = []
        list_nc_rankings = []

        the_seed = 0
        created = 0

        while total_cr<total or total_cw<total or total_nc<total:
            np.random.seed(the_seed)
            
            rankings = generate_profile_factoradic(n, m)
            
            om = preference_matrix(rankings)
            cw = condorcet_winner(om)
            c = condorcet(om)
            
            if not cw:
                if total_nc<total:
                    list_nc_om.append(om)
                    pm = position_matrix(rankings)
                    list_nc_pm.append(pm)
                    list_nc_rankings.append(rankings)
                    total_nc+=1
                    types[created] = 'nc'
                    created+=1
            else:
                if c is None:
                    if total_cw<total:
                        list_cw_om.append(om)
                        pm = position_matrix(rankings)
                        list_cw_pm.append(pm)
                        list_cw_rankings.append(rankings)
                        total_cw+=1
                        types[created] = 'cw'
                        created+=1
                else:
                    if total_cr<total:
                        list_cr_om.append(om)
                        pm = position_matrix(rankings)
                        list_cr_pm.append(pm)
                        list_cr_rankings.append(rankings)
                        total_cr+=1
                        types[created] = 'cr'
                        created+=1
            the_seed+=1

        print(types)

        with open('perfiles_tfg_rankings_'+str(n)+'_'+str(m)+'_nc.npy', 'wb') as f:
            np.save(f, np.array(list_nc_rankings))
        with open('perfiles_tfg_om_'+str(n)+'_'+str(m)+'_nc.npy', 'wb') as f:
            np.save(f, np.array(list_nc_om))
        with open('perfiles_tfg_pm_'+str(n)+'_'+str(m)+'_nc.npy', 'wb') as f:
            np.save(f, np.array(list_nc_pm))
            
        with open('perfiles_tfg_rankings_'+str(n)+'_'+str(m)+'_cw.npy', 'wb') as f:
            np.save(f, np.array(list_cw_rankings))
        with open('perfiles_tfg_om_'+str(n)+'_'+str(m)+'_cw.npy', 'wb') as f:
            np.save(f, np.array(list_cw_om))
        with open('perfiles_tfg_pm_'+str(n)+'_'+str(m)+'_cw.npy', 'wb') as f:
            np.save(f, np.array(list_cw_pm))
          
        with open('perfiles_tfg_rankings_'+str(n)+'_'+str(m)+'_cr.npy', 'wb') as f:
            np.save(f, np.array(list_cr_rankings))  
        with open('perfiles_tfg_om_'+str(n)+'_'+str(m)+'_cr.npy', 'wb') as f:
            np.save(f, np.array(list_cr_om))
        with open('perfiles_tfg_pm_'+str(n)+'_'+str(m)+'_cr.npy', 'wb') as f:
            np.save(f, np.array(list_cr_pm))