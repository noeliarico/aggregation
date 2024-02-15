# distance_from_ranking_to_profile()
def distance_from_ranking_to_profile(ranking, profile):

    n = ranking.shape[0]
    dist = 0    
    for i in range(n): # for each alternative in a row
        # for each alternative in col (consider only elements over diagonal)
        for j in range(i+1, n): 
            # alternative j in the column is preferred over the alternative i in
            # the row, which means thapython3 -m buildt the position of i in the ranking i.e.
            # ranking[i] is greater than the position of j in the ranking, which
            # in ranking[j] thus ranking[i] > ranking[j] means j succ i
            if ranking[i] > ranking[j]:
                # the amount added to the distance is the number of times
                # that the voters disagrees with j succ i, which is the number 
                # of times than i succ j appear on the profile, stored in the
                # ith row and jth column of the outranking matrix
                dist += profile[i,j]  
            else: # ranking[i] < ranking[j] then i succ j 
                # the amount of voters that prefer j over i is added to the dist
                dist += profile[j,i]

    return dist


# distance_between_rankings()

import ranking_aggregation.preferences.ranking as rank
import math
import numpy as np

def kemeny(profile, debug = False):
    """Brute force Kemeny algorithm (for testing of correct solutions)

    :param profile: outranking matrix
    :type profile: np.array
    :param debug: print rankings, defaults to False
    :type debug: bool, optional
    :return: a dictionary with:
        - distances
        - best_distance
        - winners
    :rtype: dict
    """
    n = profile.shape[0]
    distances = np.zeros(math.factorial(n), dtype=np.int32)
    for i in range(math.factorial(n)):
        factoradic = rank.from_int_to_factoradic(i, n)
        ranking = rank.from_factoradic_to_ranking(factoradic)
        dist = distance_from_ranking_to_profile(factoradic, profile)
        if debug: print("{})\t {} -- {} -- {} -- {}".format(i, factoradic, ranking, rank.print_ranking(ranking), dist))
        distances[i] = dist
    results = {}
    results['distances'] = distances
    best_distance = distances.min()
    results['best_distance'] = best_distance
    # winners = np.argmin(distances) # solo devuelve el primero
    winners = np.where(distances == best_distance)
    results['winners'] = winners[0] # because where returns a tuple
    return results