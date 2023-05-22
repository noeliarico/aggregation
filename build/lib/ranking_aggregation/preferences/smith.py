import numpy as np
import ranking_aggregation.ranking_rules.scores as scores
import ranking_aggregation.preferences.matrices as matrices

def _boolean_matrix(profile):
    half = (profile[0,1]+profile[1,0])/2
    return (profile > half).astype(np.uint8)

def smith_matrix(profile):
    """Recibes a profile of rankings and computes the Smith matrix. This matrix
    is the one necessary for computing the Smith set. It is a pairwise 
    comparison matrix where the alternatives are ordered according to their
    Copeland score. The alternative in the first row is the one with the highest
    Copeland score.
    
    The return has two objects:
    - matrix,   that is the Smith matrix
    - ids,   that is a np.array of n elements thaat contains ni the i-th element
            the index of the candidate in the i-th row

    :param profile: Profile of rankings (outranking matrix)
    :type profile: np.array
    :return: Smith matrix
    :rtype: dict
    """
    s = scores.copeland_score(profile) # get the score for each row
    s = np.flip(np.argsort(s)) # sort the scores in descending order
    cm = matrices.copeland_matrix(profile) # get the copeland matrix
    # reorder the alternatives of the Copeland matrix according to their 
    # Copeland score in descending order
    cm = cm[s,:]
    cm = cm[:,s]
    # Return info
    result = {}
    result['matrix'] = cm
    result['ids'] = s
    return result

def smith_set(profile):
    """Computes the Smith Set of the given profile of rankings

    :param profile: _description_
    :type profile: _type_
    :return: _description_
    :rtype: _type_
    """
    the_matrix = smith_matrix(profile)
    alt_names = the_matrix['ids']
    the_matrix = the_matrix['matrix']
    for i in range(1,profile.shape[0]):
        # print("Evaluating row {}".format(i))
        total = 0
        for j in range(i):
            # print("Evaluating column {}".format(j))
            # print(the_matrix[i:,j])
            total += the_matrix[i:,j].sum()
        if total == 0: 
            break
    result = {}
    if i != (profile.shape[0]-1):
        result['winners'] = alt_names[:i]
        result['losers'] = alt_names[i:]
    else:
        result['winners'] = alt_names
        result['losers'] = []
    return result


def schwartz_matrix(profile):
    bm = _boolean_matrix(profile) # get the copeland matrix
    s = bm.sum(axis=1)
    s = np.flip(np.argsort(s)) # sort the scores in descending order
    # reorder the alternatives of the Copeland matrix according to their 
    # Copeland score in descending order
    bm = bm[s,:]
    bm = bm[:,s]
    # Return info
    result = {}
    result['matrix'] = bm
    result['ids'] = s
    return result

def schwartz_set(profile):
    """Computes the Schwartz Set of the given profile of rankings

    :param profile: _description_
    :type profile: _type_
    :return: _description_
    :rtype: _type_
    """
    the_matrix = schwartz_matrix(profile)
    alt_names = the_matrix['ids']
    the_matrix = the_matrix['matrix']
    for i in range(1,profile.shape[0]):
        # print("Evaluating row {}".format(i))
        total = 0
        for j in range(i):
            # print("Evaluating column {}".format(j))
            # print(the_matrix[i:,j])
            total += the_matrix[i:,j].sum()
        if total == 0: 
            break
    result = {}
    if i != (profile.shape[0]-1):
        result['winners'] = alt_names[:i]
        result['losers'] = alt_names[i:]
    else:
        result['winners'] = alt_names
        result['losers'] = []
    return result