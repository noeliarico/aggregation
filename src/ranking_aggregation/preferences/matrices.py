import numpy as np


def preference_matrix(rankings):
    """
    Calculates the preference matrix from a matrix of rankings.

    The preference matrix is a matrix where the (i, j) entry is the number of
    times alternative i is ranked higher than alternative j.

    Parameters:
    rankings (numpy.ndarray): Matrix of rankings.

    Returns:
    numpy.ndarray: Preference matrix.
    """
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
    """
    Calculates the position matrix from a matrix of rankings.

    The position matrix is a matrix where the (i, j) entry is the number of
    times alternative i is ranked in position j.

    Parameters:
    rankings (numpy.ndarray): Matrix of rankings.

    Returns:
    numpy.ndarray: Position matrix.
    """
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


def copeland_matrix(profile, win=1.0, lose=0.0, ties=0.5):
    """
    Calculates the Copeland matrix from a profile matrix.

    The Copeland matrix is a matrix where the (i, j) entry is the score of alternative
    i against alternative j. The score is win (default 1.0) if i wins over j, lose
    (default, 0.0) if i loses over j, and ties (default 0.5) if there is a tie.

    Parameters:
    profile (numpy.ndarray): Profile matrix.
    win (float): Score for winning.
    lose (float): Score for losing.
    ties (float): Score for ties.

    Returns:
    numpy.ndarray: Copeland matrix.
    """
    half = (profile[0, 1] + profile[1, 0]) / 2

    def f(x):
        if x > half:
            return win
        if x < half:
            return lose
        if x == half:
            return ties

    f = np.vectorize(f)
    return f(profile)
