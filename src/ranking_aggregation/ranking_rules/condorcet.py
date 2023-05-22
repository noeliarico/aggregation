import numpy as np

# def betas(om, to_lineal = True):
#     n = om.shape[0]
#     m = om[0,1]+om[1,0]
#     ombool = (np.where(om > (m//2), 1, 0)).sum(axis=1)
#     if to_lineal:
#         return betas_to_lineal(n-1-ombool)
#     else:
#         return n-1-ombool

# ranking
# scores
# there_is_condorcet_ranking
# there_is_condorcet_winner
# there_is_condorcet_loser
# to_lineal
def condorcet(om, see_points = False):
    n = om.shape[0]
    m = om[0,1]+om[1,0]
    ombool = (np.where(om > (m//2), 1, 0)).sum(axis=1)
    if see_points: 
        print(ombool)
    thereis = np.all(np.in1d(np.arange(n), ombool))
    return None if not thereis else n-1-ombool

def condorcet_winner(om, see_points = False):
    n = om.shape[0]
    m = om[0,1]+om[1,0]
    ombool = (np.where(om > (m//2), 1, 0)).sum(axis=1)
    return (n-1) in ombool

def condorcet_winner_weak(om, see_points = False):
    n = om.shape[0]
    m = om[0,1]+om[1,0]
    ombool = (np.where(om >= (m//2), 1, 0)).sum(axis=1)
    return (n-1) in ombool


def condorcet_loser(om, see_points = False):
    n = om.shape[0]
    m = om[0,1]+om[1,0]
    ombool = (np.where(om <= (m//2), 1, 0)).sum(axis=1)
    return n in ombool

def condorcet_loser_weak(om, see_points = False):
    n = om.shape[0]
    m = om[0,1]+om[1,0]
    ombool = (np.where(om < (m//2), 1, 0)).sum(axis=1)
    return n in ombool

# def betas_to_lineal(r):
#     pos = np.argsort(r)
#     res = np.zeros(r.size)
#     for i in range(r.size):
#         res[pos[i]] = i
#     res = r.size - 1 - res
#     return np.array(res, dtype=np.int)