# ranking_to_linear

import numpy as np
import math


def print_ranking(ranking, alternatives = None):
    """Print a graphical representation of the ranking

    :param ranking: Ranking to print. Each element of the array contains the 
                    position of the i-th element of the ranking
    :type ranking: np.array

    :param alternatives: Names of the alternatives. If none is given alternatives
                    are named as a0, a1, a2...
    :type alternatives: np.array, optional

    :return: A string representing the ranking
    :rtype: np.array
    """

    if alternatives is None:
        alternatives = np.array(["{}{}".format('a',i) for i in list(np.arange(ranking.size)+1)])
    out=''
    # for n alternatives, x is a numpy array of length n with numbers in [0,n-1]
    for i in range(alternatives.size):
        itemindex, = np.where(ranking == i)
        out+=alternatives[itemindex][0]
        if i < alternatives.size-1:
            out+='>'
    return out

def ranking_to_linear(ranking):
    """Returns a linear extension of a ranking with ties. The extension is 
    done in lexicographic order.

    :param ranking: A ranking with ties
    :type ranking: np.array
    :return: A linear extension of the input ranking
    :rtype: np.array
    """
    for i in range(max(ranking)+1):
        # print(i)
        indexes = np.where(ranking == i)[0]
        # print(indexes)
        if indexes.size > 1: # there are tied candidates
            # Increment all the candidates that are later on the ranking
            # r[r > i] = r[r > i] + indexes.size-1
            # Untie
            values = i - np.arange(indexes.size) 
            values = values[::-1]
            # print("New values {}".format(values))
            ranking[indexes] = values
    return ranking

def print_ints_as_rankings(numbers, nalternatives = None, alternatives = None):
    """Recibes a lis of numbers and print the rankings related to them

    :param numbers: _description_
    :type numbers: _type_
    """
    if not alternatives is None:
        if nalternatives is None:
            nalternatives = alternatives.size
    for i in numbers:
        factorial = from_int_to_factoradic(i, nalternatives)
        ranking = from_factoradic_to_ranking(factorial)
        print("{})\t {}".format(i, print_ranking(ranking, alternatives)))
    
################### LEHMER'S CODE ##############################################

def from_int_to_factoradic(idx, n = None):
    """Get the factorial representation of an integer number

    :param idx: Integer number to be converted into a factorial representation
    :type idx: int

    :param idx: Number of digits used for the factorial represetnation
    :type idx: int

    :return: Factorial representation of the idx given as imput
    :rtype: np.array
    """
    if n is None:
        n = 2
        while idx > math.factorial(n):
            n+=1
    # array to store the factoradic representation of the number
    factoradic = np.zeros(n, dtype=np.uint8)
    quotient = idx # start dividing the number
    radix = 1
    while quotient != 0:
        quotient, remainder = divmod(quotient, radix)
        # fill the array from right to left
        factoradic[n - radix] = remainder
        radix += 1
    return factoradic


def from_factoradic_to_ranking(factorial_number):
    """Get the ranking associated with a factorial representation

    :param factorial_number: Integer number to be converted into a factorial representation
    :type factorial_number: np.array

    :return: Ranking associated with the factorial representation
    :rtype: np.array
    """

    # number of alternatives
    n = factorial_number.size

    # initialize an array of the same size to mark the
    # alternatives that have been already added to the
    # ranking during the exploration.
    # Initially all falso.
    # Important: boolean array to reduce memory
    alternatives = np.zeros(n, dtype=np.bool_)

    # for each position of the factorial representation
    for i in range(n):
        # count Falses until:
        until = factorial_number[i]+1
        # logging.debug("Let's count {} False(s)".format(until))
        # set initial counter to 0
        count = 0
        # iterator for each position of the boolean alternatives
        alt = 0
        # iterate
        while count < until:
            # logging.debug("Alternative {} is {}".format(alt, alternatives[alt]))
            if not alternatives[alt]:
                count += 1
            alt += 1
            # logging.debug("Count = {}, Alternative = {}".format(count, alt))
        # logging.debug("Count=Alternative, stop")
        # at this point count = until and alt has the alternative 
        # that is in the i position
        # mark the alternative that appears in the ranking
        alternatives[alt-1] = True
        # overwrite the ranking to save memory
        factorial_number[i] = alt-1   
    return factorial_number

def from_int_to_ranking(number, nalternatives):
    factoradic = from_int_to_factoradic(number, nalternatives)
    return from_factoradic_to_ranking(factoradic)

def from_ints_to_ranking(numbers, nalternatives):
    result = np.zeros(numbers.size*nalternatives, dtype = np.uint8).reshape((numbers.size, nalternatives))
    for i in range(numbers.size):
        result[i] = from_int_to_ranking(numbers[i], nalternatives)
    return result
# Related: scores_to_ranking in scores.py

# Common representation: Position of each alternative
# Another option: Alternative in each position