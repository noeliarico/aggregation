import numpy as np
from ranking_aggregation.preferences.matrices import copeland_matrix


def borda_score(profile, normalized=False):
    """Return the Borda score of each alternative

    The Borda score of an alternative is the sum of the scores it gets from
    each voter. The score of an alternative from an specific voter is the
    number of alternatives it beats in the pairwise comparison.

    :param profile: Profile of rankings represented by the outranking matrix
    :type profile: np.array

    :param normalized: if True, the score is divided by the maximum possible score
    :type normalized: bool

    :return: Borda score of each alternative
    :rtype: np.array
    """
    if not normalized:
        return profile.sum(axis=1)  # return row sums
    else:  # return row sums divided by max possible score
        num_alternatives = profile.shape[0]
        num_voters = profile[0, 1] + profile[1, 0]
        return profile.sum(axis=1) / ((num_alternatives - 1) * num_voters)


def azzini_score(profile):
    """Return the Azzini score of each alternative

    :param profile: Profile of rankings represented by the outranking matrix
    :type profile: np.array

    :return: Azzini score of each alternative
    :rtype: np.array
    """
    return profile.sum(axis=1) > profile.sum(axis=0)  # boolean


def copeland_score(profile, normalized=False, win=1.0, lose=0.0, ties=0.5):
    """Return the Copeland score of each alternative

    The Copeland score of an alternative is the number of alternatives it beats
    in a pairwise comparison.

    :param profile: Profile of rankings represented by the outranking matrix
    :type profile: np.array

    :param normalized: if True, the score is divided by the number of alternatives
    :type normalized: bool

    :param win: score for winning
    :type win: float

    :param lose: score for losing
    :type lose: float

    :param ties: score for ties
    :type ties: float

    :return: Copeland score of each alternative
    :rtype: np.array
    """
    if not normalized:
        return np.sum(copeland_matrix(profile, win=win, lose=lose, ties=ties), axis=1, dtype=np.uint16)
    else:
        num_alternatives = profile.shape[0]
        return np.sum(copeland_matrix(profile, win=win, lose=lose, ties=ties), axis=1, dtype=np.uint16) / (
            num_alternatives - 1
        )


def condorcet_score(profile):
    """Return the Condorcet score of each alternative.

    The Condorcet score of an alternative is the number of alternatives it beats
    in a pairwise comparison.

    :param profile: Profile of rankings represented by the outranking matrix
    :type profile: np.array

    :return: Condorcet score of each alternative
    :rtype: np.array
    """
    half = (profile[0, 1] + profile[1, 0]) / 2
    return np.sum(profile > half, axis=1)


def scores_to_ranking(scores, the_higher_the_better=True):
    """Get the scores given by some scoring method and returns the corresponding ranking.

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
    if the_higher_the_better:  # sort alternatives decreasingly
        order = np.flip(order)
    # get in the i-th element the position of the i-th alternative in
    # the ranking
    order = order.argsort()
    return order


def scores_to_ranking_with_ties(scores, the_higher_the_better=True):
    order = np.unique(np.sort(scores))
    if the_higher_the_better:
        order = np.flip(order)
