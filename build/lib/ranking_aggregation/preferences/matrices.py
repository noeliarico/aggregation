import numpy as np

def copeland_matrix(profile, win = 1., lose = 0., ties = 0.5):
    half = (profile[0,1]+profile[1,0])/2
    def f(x):
        if x > half: return win
        if x < half: return lose
        if x == half: return ties
    f = np.vectorize(f)
    return(f(profile))