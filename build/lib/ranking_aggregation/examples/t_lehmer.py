import math
import ranking_aggregation.preferences.lehmer as lehmer

# Example of how to obtain the factorial representation for all the possible
# permutations of 4 alternatives
print("Factorial representation of all the possible permutations:")
n = 4
for i in range(math.factorial(n)):
    print(lehmer.from_int_to_factoradic(i, n))