import numpy as np


def preflib_divide(preflib_profile):
    """Divides the profile of rankings into a 2-D numpy array with a number
    of columns equal to the number of alternatives, where each row represents
    a unique ranking in the profile. It also returns a 1-D numpy array
    containing the number of voters that chose the ranking in the first index.

    :param preflib_profile: Profile of rankings.
    :type preflib_profile: list of tuples
    :return: Rankings array and weights array.
    :rtype: tuple of (numpy.ndarray, numpy.ndarray)
    """

    initial_list = preflib_profile.flatten_strict()
    # Extract the rankings from the first element of each tuple
    rankings = np.array([item[0] for item in initial_list])
    # Extract the weights from the second element of each tuple
    weights = np.array([item[1] for item in initial_list])

    return rankings, weights


def preflib_to_pairwise_preferences_matrix(rankings, weights):
    """Computes for each pair of alternatives that number of voters that 
    prefer one over the other in any ranking
    """
    
    # rankings, weights = preflib_divide(preflib_profile)
    num_unique_rankings, num_alternatives = rankings.shape
    # Initialize the matrix
    pref_matrix = np.zeros((num_alternatives, num_alternatives), dtype=int)
    # Do the counting
    for i in range(num_alternatives):  # alternative i
        for j in range(i+1, num_alternatives):  # alternative j
            # for each pair of alternatives i,j count the number of times that
            # i is in a better position than j
            # i is in a worse position than j
            # both are tied
            i_better_than_j = 0
            i_worse_than_j = 0
            # check it in each ranking...
            for k in range(num_unique_rankings):
                r = rankings[k, :]
                pos_i = np.argwhere(r == i)[0][0]
                pos_j = np.argwhere(r == j)[0][0]
                if pos_i < pos_j:  # i in a better position than j
                    i_better_than_j += 1*weights[k]
                elif pos_j < pos_i:  # i in a worse position than j
                    i_worse_than_j += 1*weights[k]
                else:  # they are in the same position
                    i_better_than_j += 0.5*weights[k]
                    i_worse_than_j += 0.5*weights[k]
            # After checking all the rankings update the matrix
            pref_matrix[i, j] = i_better_than_j
            pref_matrix[j, i] = i_worse_than_j
    return pref_matrix


def preflib_to_positions_matrix(rankings, weights):
    """Computes for each alternatives its frequency in each position"""
    #rankings, weights = preflib_divide(preflib_profile)
    num_unique_rankings, num_alternatives = rankings.shape

    pos_matrix = np.zeros((num_alternatives, num_alternatives), dtype=int)
    for ranking in range(num_unique_rankings):
        for alternative in range(num_alternatives):
            r = rankings[ranking, :]
            pos = np.argwhere(r == alternative)[0][0]
            pos_matrix[alternative, pos] += 1*weights[ranking]
    return pos_matrix
