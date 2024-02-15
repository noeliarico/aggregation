import numpy as np
import sys
sys.path.append('./preferences')
sys.path.append('./generators')
sys.path.append('./ranking_rules')
from generate import preference_matrix, generate_profile_factoradic
from ranking import from_int_to_ranking, print_ranking
from condorcet import condorcet
from kemeny import kemeny

# a2>a3>a1>a4
# a4>a1>a2>a3
# a4>a2>a1>a3
# a4>a2>a1>a3
# a1>a2>a3>a4
# a3>a4>a1>a2
# a3>a4>a1>a2
# a2>a1>a3>a4
# a1>a3>a2>a4

pm = np.array([
    [0, 5, 6, 4],
    [4, 0, 6, 4],
    [3, 3, 0, 6],
    [5, 5, 3, 0]])
print(condorcet(pm))
k = kemeny(pm)
print(k)
print(from_int_to_ranking(k['winners'], nalternatives = 4))
