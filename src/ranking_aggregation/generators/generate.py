import numpy as np
from math import factorial
from ranking_aggregation.preferences.ranking import from_int_to_ranking


def generate_profile_factoradic(n, m):
    """Create a profile of rankings

    :param n: _description_
    :type n: _type_
    :param m: _description_
    :type m: _type_
    :return: _description_
    :rtype: _type_
    """
    num_rankings = np.math.factorial(n)
    rankings = np.zeros((m, n), dtype=int)
    random_indices = np.random.choice(num_rankings, m)
    for i in range(m):
        rankings[i] = from_int_to_ranking(random_indices[i], n)
    return rankings
