import ranking_aggregation.preferences.ranking as ranking
import numpy as np
# Print ranking recieves an array with the position of each alternative
print(ranking.print_ranking(np.array([0, 2, 3, 1]), np.array(['a', 'b', 'c', 'd'])))
print(ranking.print_ranking(np.array([1, 0, 2, 4, 3])))

print()
ranking.print_ints_as_rankings(np.array([3, 22, 1]), nalternatives=4)