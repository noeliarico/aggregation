import numpy as np
from ranking_aggregation.ranking_rules.scores import borda_score


# Docs generadas con Copilot


# Alternativa más frecuente en cada posición
# alpha1
def most_frequent_alternative_in_each_position(posm):
    """
    Returns for each position the index of the alternative that
    appears most frequently in the position.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: The most frequent alternative
    :rtype: 1D NumPy array
    """
    return np.argmax(posm, axis=0)


def least_frequent_alternative_in_each_position(posm):
    """
    Returns for each position the index of the alternative that
    appears less frequently in the position.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    """
    return np.argmin(posm, axis=0)


def num_of_alternatives_with_max_freq_in_each_pos(posm):
    """
    Returns the number of alternatives with maximum frequency in each position.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Number of alternatives with maximum frequency in each position
    :rtype: 1D NumPy array
    """
    max_values = np.max(posm, axis=0)
    return np.sum(posm == max_values, axis=0)


def num_of_alternatives_with_min_freq_in_each_pos(posm):
    """
    Returns the number of alternatives with minimum frequency in each position.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Number of alternatives with minimum frequency in each position
    :rtype: 1D NumPy array
    """
    min_values = np.min(posm, axis=0)
    return np.sum(posm == min_values, axis=0)


def freq_of_each_alternative_in_first_pos(posm):
    """
    Returns the frequency of each alternative in the first position.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Frequency of each alternative in the first position
    :rtype: 1D NumPy array
    """
    return posm[:, 0]


def freq_of_each_alternative_in_last_pos(posm):
    """
    Returns the frequency of each alternative in the last position.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Frequency of each alternative in the last position
    :rtype: 1D NumPy array
    """
    return posm[:, -1]


def freq_of_each_alternative_in_upper_half(posm):
    """
    Returns the frequency of each alternative in the upper half of the position matrix.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Frequency of each alternative in the upper half
    :rtype: 1D NumPy array
    """
    return posm[:, 0 : (posm.shape[0] // 2)].sum(axis=1)


def best_pos_of_each_alternative(posm):
    """
    Returns the best position of each alternative.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Best position of each alternative
    :rtype: 1D NumPy array
    """
    return np.argmax(posm > 0, axis=1)


def worst_pos_of_each_alternative(posm):
    """
    Returns the worst position of each alternative.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Worst position of each alternative
    :rtype: 1D NumPy array
    """
    return posm.shape[1] - 1 - np.argmax(np.flip(posm > 0, axis=1), axis=1)


def freq_of_each_alternative(posm, statistic):
    """
    Returns the frequency of each alternative based on the specified statistic.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :param statistic: Statistic to compute (min, max, median, sd)
    :type statistic: str
    :return: Frequency of each alternative based on the specified statistic
    :rtype: 1D NumPy array or None
    """
    if statistic == "min":
        return np.min(posm, axis=0)
    if statistic == "max":
        return np.max(posm, axis=0)
    if statistic == "median":
        return np.median(posm, axis=0)
    if statistic == "sd":
        return np.std(posm, axis=0)
    return None


def freq_global(posm, statistic):
    """
    Returns the global frequency based on the specified statistic.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :param statistic: Statistic to compute (min, max, median, sd, range)
    :type statistic: str
    :return: Global frequency based on the specified statistic
    :rtype: float or None
    """
    if statistic == "min":
        return np.min(posm)
    if statistic == "max":
        return np.max(posm)
    if statistic == "median":
        return np.median(posm)
    if statistic == "sd":
        return np.std(posm)
    if statistic == "range":
        return np.max(posm) - np.min(posm)
    return None


def dispersion_of_each_alternative(posm):
    """
    Returns the dispersion of each alternative.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Dispersion of each alternative
    :rtype: 1D NumPy array
    """
    return worst_pos_of_each_alternative(posm) - best_pos_of_each_alternative(posm)


def dispersion_global(posm, statistic):
    """
    Returns the global dispersion based on the specified statistic.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :param statistic: Statistic to compute (min, max, mean, median)
    :type statistic: str
    :return: Global dispersion based on the specified statistic
    :rtype: float or None
    """
    if statistic == "min":
        return np.min(dispersion_of_each_alternative(posm))
    if statistic == "max":
        return np.max(dispersion_of_each_alternative(posm))
    if statistic == "mean":
        return np.mean(dispersion_of_each_alternative(posm))
    if statistic == "median":
        return np.median(dispersion_of_each_alternative(posm))
    return None


def alternative_with_max_dispersion(posm):
    """
    Returns the alternative with the maximum dispersion.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Alternative with the maximum dispersion
    :rtype: int
    """
    return np.argmax(dispersion_of_each_alternative(posm))


def alternative_with_min_dispersion(posm):
    """
    Returns the alternative with the minimum dispersion.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Alternative with the minimum dispersion
    :rtype: int
    """
    return np.argmin(dispersion_of_each_alternative(posm))


def number_of_zeros_of_each_pos(posm):
    """
    Returns the number of zeros in each position.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Number of zeros in each position
    :rtype: 1D NumPy array
    """
    return np.sum(posm == 0, axis=0)


def number_of_zeros_total(posm):
    """
    Returns the total number of zeros in the position matrix.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Total number of zeros
    :rtype: int
    """
    return np.sum(number_of_zeros_of_each_pos(posm))


def most_frequent_alternative_in_first_pos(posm):
    """
    Returns the indices of the most frequent alternative(s) in the first position.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Indices of the most frequent alternative(s) in the first position
    :rtype: 1D NumPy array
    """
    max_index = np.argmax(posm[:, 0])
    max_value = posm[max_index, 0]
    return np.where(posm[:, 0] == max_value)[0]


def number_of_most_frequent_alternatives_in_first_pos(posm):
    """
    Returns the number of most frequent alternatives in the first position.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Number of most frequent alternatives in the first position
    :rtype: int
    """
    return len(most_frequent_alternative_in_first_pos(posm))


def relevance_of_each_alternative(posm):
    """
    Returns the relevance of each alternative.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Relevance of each alternative
    :rtype: 1D NumPy array
    """
    differences = posm.max(axis=1).reshape(posm.shape[0], 1) - posm
    results = np.ma.masked_array(differences, mask=differences == 0).min(axis=1).data
    results[results == 999999] = 0
    return results


def weighted_sum_of_frequencies(posm):
    """
    Returns the weighted sum of frequencies for each alternative.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: Weighted sum of frequencies for each alternative
    :rtype: 1D NumPy array
    """
    return (posm * (np.arange(posm.shape[0]) + 1)).sum(axis=1)


def borda_sd(om):
    """
    Returns the standard deviation of the Borda score.

    :param om: Order matrix
    :type om: 2D NumPy array
    :return: Standard deviation of the Borda score
    :rtype: float
    """
    return np.std(borda_score(om, normalized=True))


def borda_best(om):
    return np.max(borda_score(om, normalized=True))


def borda_worst(om):
    """
    Returns the worst Borda score.

    :param om: Order matrix
    :type om: 2D NumPy array
    :return: Worst Borda score
    :rtype: float
    """
    return np.min(borda_score(om, normalized=True))
