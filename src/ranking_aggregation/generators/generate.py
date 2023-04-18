import numpy as np
from math import factorial
from ranking_aggregation.preferences.ranking import from_int_to_ranking

def generate_profile_factoradic(n, m):
    num_rankings = np.math.factorial(n)
    rankings = np.zeros((m, n), dtype=int)
    random_indices = np.random.choice(num_rankings, m)
    for i in range(m):
        rankings[i] = from_int_to_ranking(random_indices[i], n)
    return rankings

def preference_matrix(rankings):
    """Calcula la matriz de preferencias a partir de una matriz de rankings"""
    m, n = rankings.shape
    pref_matrix = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            count = 0
            for k in range(m):
                if rankings[k, i] < rankings[k, j]:
                    count += 1
            pref_matrix[i, j] = count
    return pref_matrix

def position_matrix(rankings):
    """Calcula la matriz de posiciones a partir de una matriz de rankings"""
    num_columns = rankings.shape[1]
    counts = []
    for i in range(num_columns):
        # if the rankings start in 1 use the following line:
        #col_counts = np.bincount(rankings[:, i], minlength=num_columns+1)[1:]
        # if the rankings start in 0:
        col_counts = np.bincount(rankings[:, i], minlength=num_columns)
        counts.append(col_counts)
    return np.array(counts)


"""

import random
import math

def mallow_distribution_permutation(base_permutation, n, alpha, theta):
    Genera una permutación aleatoria utilizando la distribución de Mallow
    
    current_permutation = base_permutation[:]
    for i in range(n):
        # Selecciona dos elementos aleatorios para intercambiar
        swap_indices = random.sample(range(len(current_permutation)), 2)
        i, j = swap_indices[0], swap_indices[1]
        
        # Intercambia los elementos seleccionados
        current_permutation[i], current_permutation[j] = current_permutation[j], current_permutation[i]
        
        # Calcula la probabilidad de aceptar la nueva permutación
        distance = kendall_tau_distance(current_permutation, base_permutation)
        acceptance_probability = alpha**n * math.exp(-theta * distance)
        
        # Acepta la permutación con la probabilidad calculada
        if random.uniform(0, 1) > acceptance_probability:
            current_permutation[i], current_permutation[j] = current_permutation[j], current_permutation[i]
    
    return current_permutation

def kendall_tau_distance(perm1, perm2):
    Calcula la distancia de Kendall-Tau entre dos permutaciones
    
    distance = 0
    for i in range(len(perm1)):
        for j in range(i+1, len(perm1)):
            if (perm1[i] < perm1[j] and perm2[i] > perm2[j]) or
               (perm1[i] > perm1[j] and perm2[i] < perm2[j]):
                distance += 1
    
    return distance

# Ejemplo de uso
base_permutation = [1, 2, 3, 4, 5]
n = 1000  # Número de intercambios aleatorios
alpha = 0.9  # Parámetro alpha
theta = 0.5  # Parámetro theta

random_permutation = mallow_distribution_permutation(base_permutation, n, alpha, theta)

print("Permutación base:", base_permutation)
print("Permutación aleatoria generada:", random_permutation)

"""