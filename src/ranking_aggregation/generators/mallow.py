import random
import math


def mallow_distribution_ranking(base_ranking, m, alpha, theta):
    """

    Genera una permutación aleatoria utilizando la distribución de Mallow

    :param base_ranking: _description_
    :type base_ranking: _type_
    :param m: _description_
    :type m: _type_
    :param alpha: _description_
    :type alpha: _type_
    :param theta: _description_
    :type theta: _type_
    :return: _description_
    :rtype: _type_
    """

    current_permutation = base_ranking[:]
    for i in range(n):
        # Select to random elements to permute them
        swap_indices = random.sample(range(len(current_permutation)), 2)
        i, j = swap_indices[0], swap_indices[1]

        # Permute the selected indexes
        current_permutation[i], current_permutation[j] = current_permutation[j], current_permutation[i]

        # Compute the probability of accept the new permutation
        distance = kendall_tau_distance(current_permutation, base_ranking)
        acceptance_probability = alpha**n * math.exp(-theta * distance)

        # Acepta la permutación con la probabilidad calculada
        if random.uniform(0, 1) > acceptance_probability:
            current_permutation[i], current_permutation[j] = current_permutation[j], current_permutation[i]

    return current_permutation


def kendall_tau_distance(perm1, perm2):
    """Computer the distance between two permutations

    :param perm1: _description_
    :type perm1: _type_
    :param perm2: _description_
    :type perm2: _type_
    :return: _description_
    :rtype: _type_
    """

    distance = 0
    for i in range(len(perm1)):
        for j in range(i + 1, len(perm1)):
            if (perm1[i] < perm1[j] and perm2[i] > perm2[j]) or (perm1[i] > perm1[j] and perm2[i] < perm2[j]):
                distance += 1

    return distance


if __name__ == "__main__":
    # Ejemplo de uso
    base_permutation = [1, 2, 3, 4, 5]
    n = 1000  # Número de intercambios aleatorios
    alpha = 0.9  # Parámetro alpha
    theta = 0.5  # Parámetro theta

    random_permutation = mallow_distribution_permutation(base_permutation, n, alpha, theta)

    print("Permutación base:", base_permutation)
    print("Permutación aleatoria generada:", random_permutation)
