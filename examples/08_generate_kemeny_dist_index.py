import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from fnmatch import fnmatch
import os

from ranking_aggregation.disk_operations.disk_operations import get_disk_path
from ranking_aggregation.preflib_compatibility.preflib_utils import preflib_to_pairwise_preferences_matrix
from ranking_aggregation.ranking_rules.kemeny import distance_from_ranking_to_profile, max_kemeny_distance

from utils import load_list_of_profiles, load_df_metrics


def add_ind_kemeny_dist(path_folder: str, name: str, metrics_folder: str):
    """
    Add the Kemeny distances to an individual index file.

    Parameters
    ----------
    path : str
        The path to the folder where the file is located.
    name : str
        The name of the file.
    metrics_folder : str
        The path of the folder where the metrics are stored.
    """
    file_name = os.path.join(path_folder, name)
    csv_filename = metrics_folder + f"metrics_{name.replace('.obj', '')}.csv"

    profiles = load_list_of_profiles(file_name)

    df = pd.read_csv(csv_filename)

    n_alternatives = df.loc[0, "num_alternatives"]
    n_voters = df.loc[0, "num_voters"]

    # Load the central ranking (the sorted alternatives)
    central_rk = np.arange(n_alternatives)

    # Initialize array for the Kemeny distances (one for each profile)
    kemeny_dists = np.zeros(len(profiles))

    # Maximum possible Kemeny distance (used for normalization)
    max_kemeny_dist = max_kemeny_distance(n_alternatives=n_alternatives, n_voters=n_voters)

    for i in range(len(profiles)):
        om = preflib_to_pairwise_preferences_matrix(profiles[i][0], profiles[i][1])

        kemeny_dists[i] = distance_from_ranking_to_profile(central_rk, om)

    if not "kemeny_dist" in df.columns:
        df.insert(3, "kemeny_dist", kemeny_dists)
    else:
        df["kemeny_dist"] = kemeny_dists

    if not "kemeny_dist_norm" in df.columns:
        df.insert(4, "kemeny_dist_norm", kemeny_dists / max_kemeny_dist)
    else:
        df["kemeny_dist_norm"] = kemeny_dists / max_kemeny_dist

    df.to_csv(csv_filename, index=False)

    print(f"Finished --> {name}")


def add_kemeny_dist_to_index_files(path_folder: str, metrics_folder: str):
    """
    Add the Kemeny distance to the index files. This files should have been generated using
    the script 05_generate_indexes_mallow.py.

    Parameters
    ----------
    path_folder : str
        The path to the folder where the index files are stored.
    metrics_folder : str
        The path of the folder where the metrics are stored.
    """
    pattern = "*.obj"

    Parallel(n_jobs=-1)(
        delayed(add_ind_kemeny_dist)(path, name, metrics_folder)
        for path, subdirs, files in os.walk(path_folder)
        for name in files
        if fnmatch(name, pattern)
    )

    # for path, subdirs, files in os.walk(path_folder):
    #     for name in files:
    #         if fnmatch(name, pattern):
    #             add_ind_kemeny_dist(path, name, metrics_folder)


def update_ind_norm_dist(path_folder: str, name: str):
    csv_filename = os.path.join(path_folder, name)

    df = pd.read_csv(csv_filename)

    if not "kemeny_dist" in df.columns:
        raise ValueError("The Kemeny distance has not been computed yet.")

    n_alternatives = df.loc[0, "num_alternatives"]
    n_voters = df.loc[0, "num_voters"]

    # Maximum possible Kemeny distance (used for normalization)
    max_kemeny_dist = max_kemeny_distance(n_alternatives=n_alternatives, n_voters=n_voters)

    if not "kemeny_dist_norm" in df.columns:
        df.insert(4, "kemeny_dist_norm", df["kemeny_dist"] / max_kemeny_dist)
    else:
        df["kemeny_dist_norm"] = df["kemeny_dist"] / max_kemeny_dist

    df.to_csv(csv_filename, index=False)

    print(f"Finished --> {name}")


def update_norm_dist(metrics_folder: str, comb_csv_file_name: str):
    """
    Parameters
    ----------
    metrics_folder : str
        The path of the folder where the metrics are stored.
    """
    pattern = "*.csv"

    Parallel(n_jobs=-1)(
        delayed(update_ind_norm_dist)(path, name)
        for path, subdirs, files in os.walk(metrics_folder)
        for name in files
        if (fnmatch(name, pattern) and name != comb_csv_file_name)
    )

    # for path, subdirs, files in os.walk(metrics_folder):
    #     for name in files:
    #         if fnmatch(name, pattern) and name != comb_csv_file_name:
    #             update_ind_norm_dist(path, name)


if __name__ == "__main__":
    import time

    PATH_FOLDER = f"{get_disk_path()}/profiles/mallow/"
    METRICS_FOLDER = f"{PATH_FOLDER}metrics/"
    COMB_CSV_FILE_NAME = "metrics_profile_mallow.csv"

    start_time = time.time()
    # add_kemeny_dist_to_index_files(PATH_FOLDER, METRICS_FOLDER)
    update_norm_dist(METRICS_FOLDER, COMB_CSV_FILE_NAME)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

    print("\nLoading combined metrics csv...")
    start_time = time.time()
    df = load_df_metrics(METRICS_FOLDER, COMB_CSV_FILE_NAME)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
