import numpy as np
import sys
sys.path.append('./preferences')
sys.path.append('./generators')
sys.path.append('./ranking_rules')
from generate import preference_matrix, generate_profile_factoradic
from ranking import from_int_to_ranking, print_ranking
from condorcet import condorcet
from kemeny import kemeny

# Ejemplo de uso
rankings = np.array([
    [0, 2, 1], 
    [2, 1, 0], 
    [0, 1, 2], 
    [1, 0, 2]])
for i in range(rankings.shape[0]):
    print(print_ranking(rankings[i,:]))
pref_matrix = preference_matrix(rankings)
print(pref_matrix)

# np.random.seed(10)
# rankings = generate_profile_factoradic(4, 5)
# a4>a1>a2>a3
# a1>a3>a4>a2
# a4>a2>a1>a3
# a1>a2>a3>a4
# a4>a3>a1>a2
# 0 4 4 2
# 1 0 3 1
# 1 2 0 2
# 3 4 3 0



# Semillas que no dan rankings de Condorcet
# 0, 2, 3, 4, 15, 17, 21, 22, 27
# np.random.seed(0)
# Tienen solo una solución: 3, 4, 15, 17
np.random.seed(110) # 4, 23
rankings = generate_profile_factoradic(4, 9)
for i in range(rankings.shape[0]):
    print(print_ranking(rankings[i,:]))
print(preference_matrix(rankings))
print(condorcet(preference_matrix(rankings)))
k = kemeny(preference_matrix(rankings))
print(k)
print(from_int_to_ranking(k['winners'], nalternatives = 4))

# print("Buscando....")
# for i in range(500):
#     np.random.seed(i)
#     rankings = generate_profile_factoradic(4, 9)
#     if condorcet(preference_matrix(rankings)) is None:
#         k = kemeny(preference_matrix(rankings))
#         if len(k['winners']) == 1:
#             print(i)
#             print(from_int_to_ranking(k['winners'], nalternatives = 4))