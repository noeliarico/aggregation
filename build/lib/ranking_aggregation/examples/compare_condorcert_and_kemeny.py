from ranking_aggregation.data.script_om4 import *
from ranking_aggregation.ranking_rules.scoring import borda
from ranking_aggregation.ranking_rules.kemeny import kemeny
import ranking_aggregation.preferences.ranking as ranking

def compare(profile):
    print("BORDA")
    print(borda(profile))
    print("KEMENY")
    result_kemeny = kemeny(profile)
    print(result_kemeny)
    #print(ranking.from_factoradic_to_ranking(ranking.from_int_to_factoradic(result_kemeny['winners'][3])))
    ranking.print_ints_as_rankings(result_kemeny['winners'], alternatives = np.array(['a0','a1','a2','a3']))
    print(ranking.from_ints_to_ranking(result_kemeny['winners'], nalternatives=4))

# om_4_2 da diferente Borda y Kemeny
p = om_4_2
compare(p)
print(p)