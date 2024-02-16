from preflibtools.instances import OrdinalInstance
from preflibtools.instances.sampling import *
from ranking_aggregation.preflib_compatibility.preflib_utils import *
import numpy as np
import pickle
import pandas as pd

# Definition of parameters
reps = 100
dispersions = [0.1, 0.4, 0.7, 1]
#dispersions = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
path_folder = "/Users/noeliarico/Desktop/Toulouse/code/profiles/mallow1/"

# Example on how to generate
## instance = OrdinalInstance()
## instance.populate_mallows(10, 4, [1], [0.2], [(0, 1, 2, 3)])
## print(instance.flatten_strict())
# will generate a profile with 4 voters and 10 alternatives
# Using Mallow with a dispersion parameter 0.2 and reference order 0 > 1 > 2 > 3

def create_profiles_using_mallow(num_alternatives, num_voters, reps, dispersions):
    # Initialize a dataframe to track the profiles generated
    df = pd.DataFrame()
    for d in dispersions:
        list_profiles = []  # empty the list of profiles
        for i in range(reps):
            np.random.seed(i)
            instance = OrdinalInstance()
            instance.populate_mallows(num_voters, num_alternatives,
                                        [1], [d],
                                        [tuple(np.arange(num_alternatives))])
            instance.flatten_strict()
            # From the instance generated by preflib, get two Numpy arrays
            # 1) a matrix where each row is a different ranking in the profile
            # 2) the number of voters that chose that ranking
            ranking, weights = preflib_divide(instance)
            # Add the profile in the format of a tuple (ranking, weights)
            # to the list of all the profiles
            list_profiles.append((ranking, weights))
            # Save the object in plain text using Preflib's format
            name = "profile_mallow_{}_{}_{}_{}.soc".format(
                num_alternatives,
                num_voters,
                d,
                i)
            instance.write(path_folder+name)
            # Create a new row with the info of the profile for the dataframe
            new_row = pd.Series([
                num_voters,
                num_alternatives,
                d,
                i,
                name])
            # Concatenate the new row to the existing DataFrame
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
            ## -> end of: for i in range(reps)
        # Save the list with all the profiles to an object
        name = "profile_Mallow1_{}_{}_{}.obj".format(
                num_alternatives,
                num_voters,
                d)
        file_obj = open(path_folder+"objects/"+name, 'wb')
        pickle.dump(list_profiles, file_obj)
    # Rename the columns of the dataframe
    df.columns = ['num_voters',
                'num_alternatives',
                'desired_distance',
                'id',
                'name']
    # print(df)
    # Save the specifications about how the datasets where generated
    df.to_csv(path_folder+'mallow1.csv', index=False, mode='w+')  # mode overwrite
    
    
nums_alternatives = [3,4] 
nums_voters = [10,100,500]
# Execute the function to create the profiles
for num_alternatives in nums_alternatives:
    for num_voters in nums_voters:
        create_profiles_using_mallow(num_alternatives, num_voters, reps, dispersions)
        print("{} alternatives, {} voters, DONE".format(num_alternatives, num_voters))
        