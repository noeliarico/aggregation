import numpy as np
import ranking_aggregation.preferences.scores as scores

# create random profile of rankings

# first: generate rankings
# then, create matrix

####
# print profile of rankings
    
def reorder_outranking_matrix(profile):
    s = scores.borda_score(profile)
    # s = scores.scores_to_ranking(s)
    s = np.flip(np.argsort(s))
    print(s)
    profile = profile[s,:]
    profile = profile[:,s]
    result = {}
    result['matrix'] = profile
    result['ids'] = s
    return result