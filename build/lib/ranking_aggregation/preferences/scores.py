import numpy as np
from ranking_aggregation.preferences.matrices import copeland_matrix

def borda_score(profile):
    """Return the Borda score of each alternative

    :param profile: Profile of rankings represented by the outranking matrix
    :type profile: np.array
    
    :return: Borda score of each alternative
    :rtype: np.array
    """
    return profile.sum(axis=1) # return row sums

def azzini_score(profile):
    """Return the Azzini score of each alternative

    :param profile: Profile of rankings represented by the outranking matrix
    :type profile: np.array

    :return: Azzini score of each alternative
    :rtype: np.array
    """
    return profile.sum(axis=1) > profile.sum(axis=0) # boolean

def copeland_score(profile, win = 1., lose = 0., ties = 0.5):
    """Return the Copeland score of each alternative

    :param profile: Profile of rankings represented by the outranking matrix
    :type profile: np.array

    :return: Copeland score of each alternative
    :rtype: np.array
    """
    return np.sum(copeland_matrix(profile), axis = 1, dtype=np.uint16)

def condorcet_score(profile):
    """Return the Condorcet score of each alternative

    :param profile: Profile of rankings represented by the outranking matrix
    :type profile: np.array

    :return: Condorcet score of each alternative
    :rtype: np.array
    """
    half = (profile[0,1]+profile[1,0])/2
    return np.sum(profile > half, axis = 1)

def scores_to_ranking(scores, the_higher_the_better = True):
    """Get the scores given by some scoring method and returns a ranking

    :param scores: array containing in the i-th position the score obtained
                    by the i-th alternative
    :type scores: np.array
    :param the_higher_the_better: sort the scores decreasingly when it is True
                    and increasingly otherwise, defaults to True
    :type the_higher_the_better: bool, optional
    :return: a ranking
    :rtype: np.array
    """
    # sort: puts in the first position the index with the best value, in
    # the second position the index of the second best value and so on
    order = scores.argsort() 
    if the_higher_the_better: # sort alternatives decreasingly
        order = np.flip(order)
    # get in the i-th element the position of the i-th alternative in
    # the ranking 
    order = order.argsort() 
    return(order)