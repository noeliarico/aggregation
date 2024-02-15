import numpy as np
import math

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