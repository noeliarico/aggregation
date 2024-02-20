import numpy as np

# def betas(om, to_lineal = True):
#     n = om.shape[0]
#     m = om[0,1]+om[1,0]
#     ombool = (np.where(om > (m//2), 1, 0)).sum(axis=1)
#     if to_lineal:
#         return betas_to_lineal(n-1-ombool)
#     else:
#         return n-1-ombool


# ranking
# scores
# there_is_condorcet_ranking
# there_is_condorcet_winner
# there_is_condorcet_loser
# to_lineal


def condorcet(om, see_points=False):
    """
    Determines if there is a Condorcet winner in the given preference matrix.

    Parameters:
    - om (numpy.ndarray): The preference matrix representing the pairwise comparison of alternatives.
    - see_points (bool): Whether to print the points for each alternative.

    Returns:
    - int or None: The index of the Condorcet winner if one exists, otherwise None.
    """
    n = om.shape[0]
    m = om[0, 1] + om[1, 0]
    ombool = (np.where(om > (m // 2), 1, 0)).sum(axis=1)
    if see_points:
        print(ombool)
    thereis = np.all(np.in1d(np.arange(n), ombool))
    return None if not thereis else n - 1 - ombool


def condorcet_winner(om, see_points=False):
    """
    Determines if there is a Condorcet winner in the given preference matrix.

    A Condorcet winner is an alternative that wins in a pairwise comparison against every other alternative.

    Parameters:
    - om (numpy.ndarray): The preference matrix representing the pairwise comparison of alternatives.
    - see_points (bool): Whether to print the points for each alternative.

    Returns:
    - bool: True if there is a Condorcet winner, False otherwise.
    """
    n = om.shape[0]
    m = om[0, 1] + om[1, 0]
    ombool = (np.where(om > (m // 2), 1, 0)).sum(axis=1)
    return (n - 1) in ombool


def condorcet_winner_weak(om, see_points=False):
    """
    Determines if there is a weak Condorcet winner in the given preference matrix.

    A Condorcet winner is an alternative that wins or ties in a pairwise comparison against every other alternative.

    Parameters:
    - om (numpy.ndarray): The preference matrix representing the pairwise comparison of alternatives.
    - see_points (bool): Whether to print the points for each alternative.

    Returns:
    - bool: True if there is a weak Condorcet winner, False otherwise.
    """
    n = om.shape[0]
    m = om[0, 1] + om[1, 0]
    ombool = (np.where(om >= (m // 2), 1, 0)).sum(axis=1)
    return (n - 1) in ombool


def condorcet_loser(om, see_points=False):
    """
    Determines if there is a Condorcet loser in the given preference matrix.

    A Condorcet winner is an alternative that looses in a pairwise comparison against every other alternative.

    Parameters:
    - om (numpy.ndarray): The preference matrix representing the pairwise comparison of alternatives.
    - see_points (bool): Whether to print the points for each alternative.

    Returns:
    - bool: True if there is a Condorcet loser, False otherwise.
    """
    n = om.shape[0]
    m = om[0, 1] + om[1, 0]
    ombool = (np.where(om <= (m // 2), 1, 0)).sum(axis=1)
    return n in ombool


def condorcet_loser_weak(om, see_points=False):
    """
    Determines if there is a weak Condorcet loser in the given preference matrix.

    A Condorcet winner is an alternative that looses or ties in a pairwise comparison against every other alternative.

    Parameters:
    - om (numpy.ndarray): The preference matrix representing the pairwise comparison of alternatives.
    - see_points (bool): Whether to print the points for each alternative.

    Returns:
    - bool: True if there is a weak Condorcet loser, False otherwise.
    """
    n = om.shape[0]
    m = om[0, 1] + om[1, 0]
    ombool = (np.where(om < (m // 2), 1, 0)).sum(axis=1)
    return n in ombool
