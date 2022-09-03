from turtle import end_fill
import numpy as np
import time

def sort_matrix(m):
    # Compute the scores
    s = m.sum(axis=1)
    s = np.flip(np.argsort(s)) # sort the scores in descending order
    print(s)
    # Sort the matrix
    m = m[s,:]
    m = m[:,s]
    return m

om14_3 = np.array([ [0,9,6,3,6,3,5,3,5,4,4,5,6,5],
                    [1,0,2,1,4,2,2,1,1,2,1,0,3,1],
                    [4,8,0,3,6,3,5,2,3,3,3,4,4,4],
                    [7,9,7,0,7,7,6,6,6,5,7,6,6,7],
                    [4,6,4,3,0,3,4,3,4,2,4,4,5,3],
                    [7,8,7,3,7,0,6,5,5,6,5,6,6,7],
                    [5,8,5,4,6,4,0,3,4,4,5,4,5,4],
                    [7,9,8,4,7,5,7,0,5,4,7,8,6,8],
                    [5,9,7,4,6,5,6,5,0,4,6,7,7,5],
                    [6,8,7,5,8,4,6,6,6,0,6,7,6,7],
                    [6,9,7,3,6,5,5,3,4,4,0,4,6,3],
                    [5,0,6,4,6,4,6,2,3,3,6,0,5,5],
                    [4,7,6,4,5,4,5,4,3,4,4,5,0,5],
                    [5,9,6,3,7,3,6,2,5,3,7,5,5,0]])

start = time.time()
sort_matrix(om14_3)
end = time.time()
print("Execution time {}".format(end-start))