import ranking_aggregation.benchmarking_kemeny.kemeny_bfs1 as bfs1
import numpy as np

om = np.array([ [0,9,9,6],
                [1,0,8,3],
                [1,2,0,3],
                [4,7,7,0]])

results = bfs1.kemeny(om)
print(results)