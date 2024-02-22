import numpy as np
import pandas as pd
import pickle
import os
from fnmatch import fnmatch

from ranking_aggregation.preflib_compatibility.preflib_utils import *
from ranking_aggregation.indexes.indexes_for_position_matrix import *
from ranking_aggregation.ranking_rules.scores import copeland_score, borda_score
from ranking_aggregation.ranking_rules.condorcet import condorcet_winner, condorcet_loser, condorcet_winner_weak
from ranking_aggregation.disk_operations.disk_operations import get_disk_path


# Load list of profiles from object
def load_list_of_profiles(file_name):
    file_handler = open(file_name, "rb")
    profiles = pickle.load(file_handler)
    return profiles


# Function to get info about the filename
def get_info_from_name(text):
    text = text.replace(".obj", "")
    result = text.split("_")
    culture = result[1]
    dictionary = {"culture": result[1], "num_alternatives": result[2], "num_voters": result[3]}
    if culture == "mallow":
        dictionary.update(
            {
                "distance": result[4],
                "p1": result[5],
                "p2": result[6],
                "dispersion1": result[7],
                "dispersion2": result[8],
            }
        )
    return dictionary


# Two examples:
## result = get_info_from_name("/Users/noeliarico/Desktop/Toulouse/profiles/mallow/objects/profile_M_20_100_0.75_0.4_0.6_0.1_0.1.obj")
## result = get_info_from_name("/Users/noeliarico/Desktop/Toulouse/profiles/ic/objects/profiles_IC_20_500.obj")
## print("Result: {}".format(result))  # Output: "ghi"


# Get all the files with extension .obj
def generate_obj_indexes_files(path_folder):
    pattern = "*.obj"
    for path, subdirs, files in os.walk(path_folder):
        evaluated = 1

        for name in files:
            if fnmatch(name, pattern):
                file_name = os.path.join(path, name)

                profiles = load_list_of_profiles(file_name)

                info = get_info_from_name(file_name)

                print("--> {} ({}/{})".format(name, evaluated, len(files)))

                evaluated += 1

                df = pd.DataFrame(
                    columns=(
                        "num_alternatives",
                        "num_voters",
                        "culture",  # how the profile has been generated
                        # Scoring rules
                        "borda_score",
                        "borda_score_normalized",
                        "borda_sd",
                        "borda_best",
                        "borda_worst",
                        "copeland_score",
                        "copeland_score_normalized",
                        # Variation in the positions of the alternatives
                        "dispersion_min",
                        "dispersion_max",
                        "dispersion_mean",
                        "dispersion_median",
                        # Frequency in the different possible positions
                        "freq_min",
                        "freq_max",
                        "freq_median",
                        "freq_sd",
                        "freq_of_each_alternative_sd",
                        "freq_of_each_alternative_in_first_pos",
                        "freq_of_each_alternative_in_last_pos",
                        "freq_of_each_alternative_in_upper_half",
                        "weighted_sum_of_frequencies",
                        "best_pos_of_each_alternative",
                        "worst_pos_of_each_alternative",
                        # Number of times that the alterantives don't appear in some position
                        "number_of_zeros_total",
                        "number_of_most_frequent_alternatives_in_first_pos",
                        "most_frequent_alternative_in_first_pos",
                        "relevance_of_each_alternative",
                        # Condorcet properties of the profile
                        "condorcet_winner",
                        "condorcet_loser",
                        "condorcet_weak_winner",
                        # Info about the profile
                        "unique_rankings",
                        "most_common_ranking_freq",
                        "name",
                    )
                )

                for i in range(len(profiles)):
                    om = preflib_to_pairwise_preferences_matrix(profiles[i][0], profiles[i][1])

                    posm = preflib_to_positions_matrix(profiles[i][0], profiles[i][1])

                    df.loc[i] = [
                        info["num_alternatives"],
                        info["num_voters"],
                        info["culture"],
                        borda_score(om),
                        borda_score(om, normalized=True),
                        borda_sd(om),
                        borda_best(om),
                        borda_worst(om),
                        copeland_score(om),
                        copeland_score(om, normalized=True),
                        dispersion_global(posm, "min"),
                        dispersion_global(posm, "max"),
                        dispersion_global(posm, "mean"),
                        dispersion_global(posm, "median"),
                        freq_global(posm, "min"),
                        freq_global(posm, "max"),
                        freq_global(posm, "median"),
                        freq_global(posm, "sd"),
                        freq_of_each_alternative(posm, "sd"),
                        freq_of_each_alternative_in_first_pos(posm),
                        freq_of_each_alternative_in_last_pos(posm),
                        freq_of_each_alternative_in_upper_half(posm),
                        weighted_sum_of_frequencies(posm),
                        best_pos_of_each_alternative(posm),
                        worst_pos_of_each_alternative(posm),
                        number_of_zeros_total(posm),
                        number_of_most_frequent_alternatives_in_first_pos(posm),
                        most_frequent_alternative_in_first_pos(posm),
                        relevance_of_each_alternative(posm),
                        condorcet_winner(om),
                        condorcet_loser(om),
                        condorcet_winner_weak(om),
                        len(profiles[i][1]),
                        np.max(profiles[i][1]),
                        name.replace(".obj", ""),
                    ]

                df.to_csv(path_folder + "metrics/metrics_" + name.replace(".obj", "") + ".csv", index=False)


if __name__ == "__main__":
    path_folder = f"{get_disk_path()}/profiles/mallow/"

    generate_obj_indexes_files(path_folder)
