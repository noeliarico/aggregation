import numpy as np
import time

om = np.array([ [0,9,9,6],
                [1,0,8,3],
                [1,2,0,3],
                [4,7,7,0]])

# este tiene 2 ganadores, sin condorcet winner
om = np.array([ [0, 6, 3, 2, 7],
                [4, 0, 6, 5, 6],
                [7, 4, 0, 7, 5],
                [8, 5, 3, 0, 6],
                [3, 4, 5, 4, 0]])
# es este:
#   numberOfVoters                ranking
# 1              1 C5 ≻ C4 ≻ C3 ≻ C1 ≻ C2
# 2              4 C2 ≻ C3 ≻ C4 ≻ C1 ≻ C5
# 3              1 C5 ≻ C3 ≻ C1 ≻ C4 ≻ C2
# 4              1 C1 ≻ C5 ≻ C3 ≻ C2 ≻ C4
# 5              2 C4 ≻ C1 ≻ C2 ≻ C5 ≻ C3
# 6              1 C3 ≻ C5 ≻ C4 ≻ C1 ≻ C2
#   C1 C2 C3 C4 C5
# 1  4  5  3  2  1
# 2  4  1  2  3  5
# 3  3  5  2  4  1
# 4  1  4  3  5  2
# 5  2  3  5  1  4
# 6  4  5  1  3  2

# Este otro no tiene Condorcet winner y tiene un solo ganador de Kemeny
om = np.array([ [0, 7, 2, 7, 6],
                [3, 0, 5, 3, 3],
                [8, 5, 0, 6, 5],
                [3, 7, 4, 0, 6],
                [4, 7, 5, 4, 0]])
# Es este:
#   numberOfVoters                ranking
# 1              1 C3 ≻ C5 ≻ C1 ≻ C4 ≻ C2
# 2              2 C4 ≻ C5 ≻ C2 ≻ C3 ≻ C1
# 3              2 C3 ≻ C1 ≻ C4 ≻ C2 ≻ C5
# 4              2 C1 ≻ C5 ≻ C2 ≻ C4 ≻ C3
# 5              1 C2 ≻ C5 ≻ C3 ≻ C4 ≻ C1
# 6              2 C3 ≻ C1 ≻ C4 ≻ C5 ≻ C2
#   C1 C2 C3 C4 C5
# 1  3  5  1  4  2
# 2  5  3  4  1  2
# 3  2  4  1  3  5
# 4  1  3  5  4  2
# 5  5  1  3  4  2
# 6  2  5  1  3  4



om    = np.array([  [0,5,7,4,6],
                    [5,0,6,6,4],
                    [3,4,0,3,5],
                    [6,4,7,0,5],
                    [4,6,5,5,0]])


om = np.array([     [0, 7, 5,  8, 6, 6],
                    [3, 0, 2,  4, 3, 2],
                    [5, 8, 0, 10, 9, 7],
                    [2, 6, 0,  0, 6, 4],
                    [4, 7, 1,  4, 0, 7],
                    [4, 8, 3,  6, 3, 0]])
# 7
om    = np.array([  [0,8,8,5,9,6,8],
                    [2,0,4,2,5,2,7],
                    [2,6,0,3,6,4,8],
                    [5,8,7,0,7,8,8],
                    [1,5,4,3,0,2,8],
                    [4,8,6,2,8,0,8],
                    [2,3,2,2,2,2,0]])
# 8 - 11.15801477432251s
om    = np.array([  [0,  2,  4,  2,  4, 10,  5,  7],
                    [8,  0,  8,  2,  7,  8,  5,  5],
                    [6,  2,  0,  0,  2, 10,  5,  5],
                    [8,  8, 10,  0,  5, 10,  8, 10],
                    [6,  3,  8,  5,  0,  8,  5,  5],
                    [0,  2,  0,  0,  2,  0,  0,  0],
                    [5,  5,  5,  2,  5, 10,  0,  7],
                    [3,  5,  5,  0,  5, 10,  3,  0]])

start = time.time()
import ranking_aggregation.ranking_rules.kemeny as k
results = k.kemeny(om)
print(results)
print(time.time() - start) # 11.15 con print y 2.41 sin

# import ranking_aggregation.preferences.scores as scores
# print(scores.scores_to_ranking(np.array([21, 24, 22, 23]), the_higher_the_better=False))

# import ranking_aggregation.ranking_rules.scoring as srr
# b = srr.borda(om)
# print(b)
# print(b['ranking'])

# import ranking_aggregation.preferences.smith as smith
# print("Smith set")
# print(smith.smith_matrix(om))

# import ranking_aggregation.preferences.profiles as profiles

# start = time.time()
# print(profiles.reorder_outranking_matrix(om))
# print(time.time() - start)