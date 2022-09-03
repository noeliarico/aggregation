om = np.array([[0,  3,  2,  4],
               [7,  0,  3,  5],
               [8,  7,  0,  6],
               [6,  5,  4,  0]])
om = np.array([ [0,8,8,  5,  9,  6, 8],
                [2,0,4,  2,  5,  2, 7],
                [2,6,0,  3,  6,  4, 8],
                [5,8,7,  0,  7,  8, 8],
                [1,5,4,  3,  0,  2, 8],
                [4,8,6,  2,  8,  0, 8],
                [2,3,2,  2,  2,  2, 0]])
# Get coopeland

def f(x, half = 5):
  if x > half: return 1.
  if x < half: return 0.
  if x == half: return 0.5

f = np.vectorize(f)
om = f(om)
logging.debug(om)

values = om.sum(axis=1)
logging.debug(values)
order = values.argsort() # in the first position the index with the best value
logging.debug(order)
order = np.flip(order)
logging.debug(order)

om = om[order,:]
om = om[:,order]
logging.debug(om)