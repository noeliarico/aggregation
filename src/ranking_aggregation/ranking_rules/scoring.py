import numpy as np

import ranking_aggregation.ranking_rules.scores as scores


def borda(profile):
    """Get the outranking matrix and returns the Borda Count winning ranking

    :param profile: Profile of rankings
    :type profile: np.array

    :return: Winning ranking
    :rtype: np.array
    """
    # noutranks = np.sum(om, axis=1)
    # # print(noutranks)
    # out = np.argsort(noutranks)
    # sorted_noutranks = noutranks[out]
    # sorted_index = np.searchsorted(sorted_noutranks, noutranks)
    # return (out.size - 1) - sorted_index
    s = scores.borda_score(profile)
    result = {}
    result["ranking"] = scores.scores_to_ranking(s)
    result["scores"] = s
    result["has_ties"] = True
    return result


def copeland(profile):
    """Get the outranking matrix and returns the Copeland winning ranking

    :param profile: Profile of rankings
    :type profile: np.array

    :return: Winning ranking
    :rtype: np.array
    """
    s = scores.copeland_score(profile)
    result = {}
    result["ranking"] = scores.scores_to_ranking(s)
    result["scores"] = s
    result["has_ties"] = np.unique(result["ranking"]) == profile.shape[0]
    return result
