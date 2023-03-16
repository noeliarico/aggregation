.. Ranking aggregation documentation master file, created by
   sphinx-quickstart on Mon May 30 17:40:23 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Common ranking aggregation functionalities
===============================================

.. autosummary::
   :toctree: _autosummary
      :maxdepth: 4
   :recursive:


Useful links
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

All the information of tha package can be found in:

ranking aggregation

Modules available in this package
========================================

:fa:`bars`
:fa:`spinner,text-white bg-primary fa-2x,style=fa`

- ``data``  contains files with different outranking matrices to use for testing.
   These matrices are stored in different files under the structure name of ``om_n_m.py``
   `n` number of alternatives and `m` number of voters.

- ``preferences`` contains function related to the ouranking matrices

   - ``matrices``
   - ``profiles``
   - ``ranking``
   - ``scores``
   - ``smith``

- ``ranking_rules`` contain the functions related to obtain a consensus ranking from a profile.

   - List of rules that do not require the complete profiles, only the outranking matrices:
      - ``condorcet``
      - ``kemeny``
      - ``scoring``

Integers to rankings using Lehmer's code
========================================

The steps required to obtain a ranking from an integer number are the following:

- Use the ``from_int_to_factoradic`` function to obtain the factorial representation
- Use the 


An example of how to obtain the factorial representation for all the possible
permutations of 4 alternatives is shown below:

.. code-block:: python

   import math
   import ranking_aggregation.preferences.ranking as lehmer

   # Example of how to obtain the factorial representation for all the possible
   # permutations of 4 alternatives
   print("Factorial representation of all the possible permutations:")
   n = 4 # fix the number of alternatives
   for i in range(math.factorial(n)):
      print(lehmer.from_int_to_factoradic(i, n))

Some code:

.. literalinclude:: /../../src/examples/t_lehmer.py

Application of ranking rules
=============================

**Borda**

.. code-block:: python

   # some code here


**Kemeny**

.. code-block:: python

   import ranking_aggregation.ranking_rules.kemeny as k
   kemeny_result = k.kemeny(profile, debug = False)
   ranking.print_ints_as_rankings(kemeny_result['winners'], 
                                    alternatives = np.array(['a0', 'a1', 'a2', 'a3', 'a4']), 
                                    nalternatives = 5)
