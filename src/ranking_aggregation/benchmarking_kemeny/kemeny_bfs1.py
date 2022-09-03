import numpy as np
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

"""
Implementation that computes in batches
First it starts with one prefix for each of the alternatives

"""

def choose_alternative_to_add(thread, prefix, n):
    reach_thread = 0 
    for i in range(n):
        is_already_in_the_prefix = False
        for j in range(len(prefix)-1):
            if i == prefix[j]:
                is_already_in_the_prefix = True
                break  
        # if I'm here then i is not in the prefix
        if not is_already_in_the_prefix:
            if reach_thread == thread:
                return i
                break
            else:
                reach_thread+=1
        
def compute_distance(iter, prefix, current_distance, om, threshold):
    # logging.debug("Add to the prefix: {}".format(choose_alternative_to_add(iter, prefix, 4)))
    # prefix[prefix.shape[0]-1] = 1
    to_add = 0
    for i in range(om.shape[0]):
        consider = True
        for j in range(prefix.shape[0]-1):
            if prefix[j] == i:
                consider = False
                break
        if consider:
            # logging.debug("om[{},{}]".format(prefix[prefix.shape[0]-1],i))
            # logging.debug(om[i,prefix[prefix.shape[0]-1]])
            to_add += om[i,prefix[prefix.shape[0]-1]]
    if to_add > threshold:
        return(10000)
    else:
        return(current_distance + to_add)

def compute_all_distances(prefixes, distances, om, remaining):
    threshold = ((om[0,1]+om[1,0]) * (remaining-1))/2
    logging.debug("Candidates that add more than {} will not be considered".format(threshold))
    for i in range(prefixes.shape[0]):
        # logging.debug("Evaluating prefix {}...".format(prefixes[i,:]))
        iter = i//(prefixes.shape[0]//remaining)
        c = choose_alternative_to_add(iter, prefixes[i,:], om.shape[0])
        prefixes[i,prefixes.shape[1]-1] = c
        distances[i] = compute_distance(iter, prefixes[i,:], distances[i], om, threshold)
    return prefixes, distances

""" Main method
"""
def kemeny(om):
    n = om.shape[0] # get the number of alternatives
    half = ((om[0,1]+om[1,0]) * ((n*n)-n)/2) / 2
    # to store the points that make an alternative be discarded
    thresholds = np.zeros(n, dtype = np.uint8) + (((om[0,1]+om[1,0])/2)*(n-1))
    logging.debug(half)
    # Initial structure, array of n rows and one column
    prefixes = np.arange(n, dtype = np.uint8)[:, np.newaxis]
    remaining = n - 1
    # Initial distances
    distances = om.sum(axis = 0)
    # First filter
    filter = distances < ((om[0,1]+om[1,0])*remaining)/2
    distances = distances[filter]
    prefixes = prefixes[filter,:]
    while remaining > 0:
        logging.debug("----Remaining candidates: {}".format(remaining))
        logging.debug(prefixes)
        logging.debug(distances) 
        # New tentative prefixes
        prefixes = np.tile(prefixes,(remaining,1))
        prefixes = np.append(prefixes, np.zeros((prefixes.shape[0],1), dtype = np.uint8), axis = 1)
        # Enlarge the size of distances
        distances = np.tile(distances,remaining)
        logging.debug("New prefixes to complete:")
        logging.debug(prefixes)
        # Compute new distances
        prefixes, distances = compute_all_distances(prefixes, distances, om, remaining)
        logging.debug("New prefixes:")
        logging.debug(prefixes)
        logging.debug(distances) 
        # Decrease the number of alternatives remaining 
        remaining -= 1
        # Only the ones that pass the threshold
        # filter = distances >= half[n-remaining-1]
        # filter = distances <= half[n-remaining-1]
        filter = distances < half
        distances = distances[filter]
        prefixes = prefixes[filter,:]
        logging.debug("After filter:")
        logging.debug(prefixes)
        logging.debug(distances)
    return(prefixes, distances)

# import time
start = time.time()
p, d = kemeny(om)
end = time.time()
logging.debug(p)
logging.debug(d)
print("Execution time {}".format(end-start))