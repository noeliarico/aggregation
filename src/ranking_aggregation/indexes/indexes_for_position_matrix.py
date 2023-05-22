import numpy as np

# Alternativa más frecuente en cada posición
# alpha1
def most_frequent_alternative_in_each_position(posm):
    """Returns for each position the index of the alternative that
    appears most frequently in the position.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    :return: The most frequent alternative
    :rtype: 1D NumPy array
    """
    return(np.argmax(posm, axis=0))

# Alternativa menos frecuente en cada posición
# alpha2
def least_frequent_alternative_in_each_position(posm):
    """Returns for each position the index of the alternative that
    appears less frequently in the position.

    :param posm: Position matrix
    :type posm: 2D NumPy array
    """
    return(np.argmin(posm, axis=0))

# Número de alternativas con frecuencia máxima en cada posición
# n1
def num_of_alternatives_with_max_freq_in_each_pos(posm):
    max_values = np.max(posm, axis=0)
    return(np.sum(posm == max_values, axis = 0))

# Número de alternativas con frecuencia mínima en cada posición
# n2
def num_of_alternatives_with_min_freq_in_each_pos(posm):
    min_values = np.min(posm, axis=0)
    return(np.sum(posm == min_values, axis = 0))

def freq_of_each_alternative_in_first_pos(posm):
    return posm[:, 0]

def freq_of_each_alternative_in_last_pos(posm):
    return posm[:, -1]

def freq_of_each_alternative_in_upper_half(posm):
    return posm[:, 0:(posm.shape[0]//2)].sum(axis = 1)

# Mejor posicion de cada alternativa
# beta1
def best_pos_of_each_alternative(posm):
    return(np.argmax(posm > 0, axis=1))

# Peor posiciond e cada alternativa
# beta2
def worst_pos_of_each_alternative(posm):
    return(posm.shape[1] - 1 - np.argmax(np.flip(posm > 0, axis=1), axis=1))

def freq_of_each_alternative(posm, statistic):
    if statistic == "min":
        return(np.min(posm, axis=0))
    if statistic == "max":
        return(np.max(posm, axis=0))
    if statistic == "median":
        return(np.median(posm, axis=0))
    if statistic == "sd":
        return(np.std(posm, axis=0))
    # mean always equal to m, because it's the sum of the row
    return None

def freq_global(posm, statistic):
    if statistic == "min":
        return(np.min(posm))
    if statistic == "max":
        return(np.max(posm))
    if statistic == "median":
        return(np.median(posm))
    if statistic == "sd":
        return(np.std(posm))
    # mean always equal to (m*n)/(n*n), because it's the sum of all the elements
    if statistic == "range":
        return(np.max(posm)-np.min(posm))
    return None

# d
def dispersion_of_each_alternative(posm):
    return(worst_pos_of_each_alternative(posm)-best_pos_of_each_alternative(posm))

def dispersion_global(posm, statistic):
    if statistic == "min":
        return(np.min(dispersion_of_each_alternative(posm)))
    if statistic == "max":
        return(np.max(dispersion_of_each_alternative(posm)))
    if statistic == "mean":
        return(np.mean(dispersion_of_each_alternative(posm)))
    if statistic == "median":
        return(np.median(dispersion_of_each_alternative(posm)))

def alternative_with_max_dispersion(posm):
    return(np.argmax(dispersion_of_each_alternative(posm)))

def alternative_with_min_dispersion(posm):
  return(np.argmin(dispersion_of_each_alternative(posm)))

def number_of_zeros_of_each_pos(posm):
  return(np.sum(posm == 0, axis = 0))

def number_of_zeros_total(posm):
  return(np.sum(number_of_zeros_of_each_pos(posm)))



def most_frequent_alternative_in_first_pos(posm):
    # Find the index of the highest value in the first column
    max_index = np.argmax(posm[:, 0])
    # Find the value of the highest value in the first column
    max_value = posm[max_index, 0]
    # Return the indices of all rows that have the highest value in the first column
    return np.where(posm[:, 0] == max_value)[0]

def number_of_most_frequent_alternatives_in_first_pos(posm):
    return len(most_frequent_alternative_in_first_pos(posm))

def relevance_of_each_alternative(posm):
    differences = posm.max(axis=1).reshape(posm.shape[0],1) - posm
    results = np.ma.masked_array(differences, mask=differences==0).min(axis = 1).data
    results[results == 999999] = 0
    return results

def weighted_sum_of_frequencies(posm):
    return (posm * (np.arange(posm.shape[0])+1)).sum(axis = 1)
