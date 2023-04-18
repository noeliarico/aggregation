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

# Mejor posicion de cada alternativa
# beta1
def best_pos_of_each_alternative(posm):
    return(np.argmax(posm > 0, axis=1))

# Peor posiciond e cada alternativa
# beta2
def worst_pos_of_each_alternative(posm):
    return(posm.shape[1] - 1 - np.argmax(np.flip(posm > 0, axis=1), axis=1))

# f1
def max_freq_of_each_alternative(posm):
    return(np.max(posm, axis=0))

# f2
def min_freq_of_each_alternative(posm):
    return(np.min(posm, axis=0))

def median_freq_of_each_alternative(posm):
    return(np.median(posm, axis=0))

def median_freq(posm):
    return(np.median(median_freq_of_each_alternative(posm)))

# d
def dispersion_of_each_alternative(posm):
    return(worst_pos_of_each_alternative(posm)-best_pos_of_each_alternative(posm))

def dispersion_avg(posm):
    return(np.mean(dispersion_of_each_alternative(posm)))

def alternative_with_max_dispersion(posm):
    return(np.argmax(dispersion_of_each_alternative(posm)))

def alternative_with_min_dispersion(posm):
  return(np.argmin(dispersion_of_each_alternative(posm)))

def number_of_zeros_of_each_pos(posm):
  return(np.sum(posm == 0, axis = 0))

def number_of_zeros_total(posm):
  return(np.sum(number_of_zeros_of_each_pos(posm)))
