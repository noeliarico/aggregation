from preflibtools.instances import OrdinalInstance
from preflibtools.instances.sampling import *
import numpy as np
import pickle
from preflibtools.properties.distances import kendall_tau_distance
import pandas as pd

from ranking_aggregation.preflib_compatibility.preflib_utils import *
from ranking_aggregation.disk_operations.disk_operations import get_disk_path


# Definition of parameters
reps = 100
prob_of_subpoblation = [0.1, 0.2, 0.3, 0.4, 0.5]
distance_between_the_base_rankings = [0.25, 0.5, 0.75, 1]
dispersion1 = 0.4
dispersion2 = 0.4

path_folder = f"{get_disk_path()}/profiles/mallow2/"


# Example on how to generate
## instance = OrdinalInstance()
## instance.populate_mallows(10, 4, [0.4, 0.6], [0.2, 0.3], [((0, 1, 2)), (1, 0, 2)])
## print(instance.flatten_strict())
# will generate a profile with 5 voters and 10 alternatives, according to a mixture using two Mallows model.
# One, selected with probability 0.4 has dispersion parameter 0.2 and reference order 0 > 1 > 2.
# The other one, selected with probability 0.6 has dispersion parameter 0.3 and reference order 1 > 0 > 2


# Given a base ranking, the aim is to generate a new ranking which is at
# a desired_distance (+- a threshold) from the original ranking
def generate_initialization(num_alternatives, desired_distance, threshold=0.05):
    base_ranking = tuple(np.arange(num_alternatives))

    new_ranking = np.arange(num_alternatives)

    distance_to_desired = 1

    while distance_to_desired >= threshold:
        np.random.shuffle(new_ranking)

        distance = kendall_tau_distance(base_ranking, tuple(new_ranking))

        distance_to_desired = abs(distance - desired_distance)
        # print("Created ranking {} with distance {} ({} to {})".format(new_ranking, distance, distance_to_desired, d))
    # print("Accepted --> ranking {} with distance {}".format(new_ranking, distance))

    return base_ranking, tuple(new_ranking), distance


# Example of use
## print(generate_initialization(10, 0.25))


def create_profiles_using_mallow(num_alternatives, num_voters):
    # Initialize a dataframe to track the profiles generated
    df = pd.DataFrame()

    for p1 in prob_of_subpoblation:
        for d in distance_between_the_base_rankings:
            list_profiles = []  # empty the list of profiles

            for i in range(reps):
                if d != 1:
                    # Create to base rankings that are separated by distance d
                    ranking1, ranking2, reald = generate_initialization(num_alternatives, d)
                else:  # Complete oposite orders
                    ranking1 = tuple(np.arange(num_alternatives))
                    ranking2 = tuple(np.arange(num_alternatives)[::-1])
                    reald = 1

                # Generate the new instance using Mallow's distribution
                np.random.seed(i)  # to ensure reproducibility

                instance = OrdinalInstance()

                instance.populate_mallows(
                    num_voters, num_alternatives, [p1, 1 - p1], [dispersion1, dispersion2], [ranking1, ranking2]
                )
                instance.flatten_strict()

                # From the instance generated by preflib, get two Numpy arrays
                # 1) a matrix where each row is a different ranking in the profile
                # 2) the number of voters that chose that ranking
                ranking, weights = preflib_divide(instance)

                # Add the profile in the format of a tuple (ranking, weights)
                # to the list of all the profiles
                list_profiles.append((ranking, weights))

                # Save the object in plain text using Preflib's format
                name = "profile_mallow_{}_{}_{}_{}_{}_{}_{}_{}.soc".format(
                    num_alternatives, num_voters, d, p1, 1 - p1, dispersion1, dispersion2, i
                )
                instance.write(path_folder + name)

                # Create a new row with the info of the profile for the dataframe
                new_row = pd.Series(
                    [
                        num_voters,
                        num_alternatives,
                        d,
                        i,
                        np.array(ranking1, dtype=np.uint),
                        np.array(ranking2, dtype=np.uint),
                        reald,
                        p1,
                        1 - p1,
                        dispersion1,
                        dispersion2,
                        name,
                    ]
                )

                # Concatenate the new row to the existing DataFrame
                df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

            ## -> end of: for i in range(reps)

            # Save the list with all the profiles to an object
            name = "profile_M_{}_{}_{}_{}_{}_{}_{}.obj".format(
                num_alternatives, num_voters, d, p1, 1 - p1, dispersion1, dispersion2
            )
            file_obj = open(path_folder + "objects/" + name, "wb")
            pickle.dump(list_profiles, file_obj)

        ## -> end of: for d in distance_between_the_base_rankings
        # Consider also distance 1, i.e. the subpoblation have max disagreement

    ## -> end of: for p1 in prob_of_subpoblation:
    # Rename the columns of the dataframe
    df.columns = [
        "num_voters",
        "num_alternatives",
        "desired_distance",
        "id",
        "base_pob1",
        "base_pob2",
        "real_distance",
        "prob_pob1",
        "prob_pob2",
        "dispersion_pob1",
        "dispersion_pob2",
        "name",
    ]
    # print(df)
    # Save the specifications about how the datasets where generated

    df.to_csv(path_folder + "mallow.csv", index=False, mode="w+")  # mode overwrite


nums_alternatives = [10, 15, 20]
num_voters = 100

# Execute the function to create the profiles
for num_alternatives in nums_alternatives:
    create_profiles_using_mallow(num_alternatives, num_voters)
    print("{} alternatives, DONE".format(num_alternatives))
