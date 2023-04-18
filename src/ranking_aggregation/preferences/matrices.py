import numpy as np


def preference_matrix(rankings):
    """Calcula la matriz de preferencias a partir de una matriz de rankings"""
    m, n = rankings.shape
    pref_matrix = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            count = 0
            for k in range(m):
                if rankings[k, i] < rankings[k, j]:
                    count += 1
            pref_matrix[i, j] = count
    return pref_matrix


def position_matrix(rankings):
    """Calcula la matriz de posiciones a partir de una matriz de rankings"""
    num_columns = rankings.shape[1]
    counts = []
    for i in range(num_columns):
        # if the rankings start in 1 use the following line:
        # col_counts = np.bincount(rankings[:, i], minlength=num_columns+1)[1:]
        # if the rankings start in 0:
        col_counts = np.bincount(rankings[:, i], minlength=num_columns)
        counts.append(col_counts)
    return np.stack(counts)


##################### MATRICES FOR SCORES #####################


def copeland_matrix(profile, win = 1., lose = 0., ties = 0.5):
    half = (profile[0,1]+profile[1,0])/2
    def f(x):
        if x > half: return win
        if x < half: return lose
        if x == half: return ties
    f = np.vectorize(f)
    return(f(profile))