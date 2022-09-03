import ranking_aggregation.preferences.smith as smith
import ranking_aggregation.preferences.ranking as ranking
import ranking_aggregation.preferences.matrices as matrices
import ranking_aggregation.examples.om as om
import numpy as np
from ranking_aggregation.data.script_om8 import *

#profile = om.om4_1 # [0], [3,1,2] hay condorcet winner
profile = om.om5_1
#profile = om.om8_1
#profile = om.om4_2

profile = om_8_15

print("\nThe profile of rankings:")
print(profile)

print("\nThe Copeland matrix:")
cm = matrices.copeland_matrix(profile)
print(cm)
print(cm.sum(axis=1))

print("\nThe smith matrix:")
sm = smith.smith_matrix(profile)
print(sm)
print(sm['matrix'].sum(axis=1))

print("\nThe smith set:")
print(smith.smith_set(profile))

print("\nThe schwartz set:")
print(smith.schwartz_set(profile))

import ranking_aggregation.ranking_rules.kemeny as k
print("\nThe result obtained with the Kemeny method:")
kemeny_result = k.kemeny(profile, debug = False)
ranking.print_ints_as_rankings(kemeny_result['winners'], 
                                #alternatives = np.array(['a0', 'a1', 'a2', 'a3']), 
                                nalternatives = 8)

