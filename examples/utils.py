# Function to get info about the filename
import os

import numpy as np
import pandas as pd


def get_info_from_name(text: str, metrics: bool = False):
    """
    Get the information of the profile from the filename.

    Filenames formats:
        - Profile objects filenames: profile_<culture>_<num_alternatives>_<num_voters>_<mallow_disp>.obj
        - Metrics csv filenames: metrics_profile_<culture>_<num_alternatives>_<num_voters>_<mallow_disp>.obj

    Parameters
    ----------
    text : str
        The filename.
    metrics : bool
        True if the filename is one of a metrics file, False otherwise.
    """
    text = text.replace(".obj", "")

    # Remove the extension
    text_without_ext = ".".join(text.split(".")[:-1])

    # Split the text by the underscores (which are the info dividers)
    result = text_without_ext.split("_")

    # If the filename is a metrics file, the first rwo elements are "metrics" and "profile".
    # If not, the first element is "profile".
    init_index = 2 if metrics else 1

    dictionary = {
        "culture": result[init_index],
        "num_alternatives": result[init_index + 1],
        "num_voters": result[init_index + 2],
    }

    if dictionary["culture"] == "mallow":
        dictionary.update({"mallow_disp": result[init_index + 3]})

    return dictionary


def check_create_file(filename: str):
    """
    Check if the file exists. If not, create it.

    Parameters
    ----------
    filename : str
        The path to the file.
    """
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w"):
            pass


def add_profile_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a new column to the dataframe df with the type of profile.

    The new column is named `profile_type`.

    The type can be:
        - "CR" if the profile has a Condorcet winner.
        - "CW" if the profile has a Condorcet weak winner.
        - "NC" if the profile has neither a Condorcet winner nor a Condorcet weak winner.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to modify.

    Returns
    -------
    df : pandas.DataFrame
        The modified dataframe.
    """
    df["profile_type"] = df.apply(
        lambda row: "CR" if row["condorcet_ranking"] else "CW" if row["condorcet_winner"] else "NC", axis=1
    )

    return df


def add_borda_win_rate_pctl(df: pd.DataFrame, ranges: list[float]) -> pd.DataFrame:
    """
    Add a new column to the dataframe with the Borda winner rate percentiles.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to modify.
    ranges : list[float]
        The ranges of the percentiles. It should not contain 0 and 1 (as they are automatically added).

    Returns
    -------
    df : pandas.DataFrame
        The modified dataframe.
    """
    # Extract win rates to a float list
    win_rates = df["borda_score_normalized"].apply(lambda x: np.array(list(map(float, x.strip("[]").split()))))

    ranges = np.append(ranges, [0, 1.1])
    ranges.sort()

    for i in range(len(ranges) - 1):
        df[f"borda_win_rate_pctl_{i}"] = win_rates.apply(lambda x: np.sum((x >= ranges[i]) & (x < ranges[i + 1])))

    return df


def add_borda_winner_pctl(df: pd.DataFrame, ranges: list[float]) -> pd.DataFrame:
    """
    Add a new column to the dataframe with the percentage of the max Borda win rate achieved
    by the Borda count winning alternative. The percentage is grouped in the corresponding range.

    The new column is named `borda_winner_pctl`.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to modify.
    ranges : list[float]
        The ranges of the percentiles. It should not contain 0 and 1 (as they are automatically added).

    Returns
    -------
    df : pandas.DataFrame
        The modified dataframe.
    """

    def get_range_idx(x: float, ranges: list[float]):
        for i in range(len(ranges) - 1):
            # Check if x is in the range
            if ranges[i] <= x < ranges[i + 1]:
                return f"{ranges[i]:.0%}-{ranges[i+1]:.0%}"
            # Check if x is equal to the top limit
            elif ranges[i + 1] == x == 1:
                return f"{ranges[i]:.0%}-{ranges[i+1]:.0%}"

    ranges = np.append(ranges, [0, 1])  # Add bottom and top limits
    ranges = np.unique(ranges)  # Sort and get unique range limits

    df["borda_winner_pctl"] = df["borda_score_normalized"].apply(
        lambda x: get_range_idx(max(list(map(float, x.strip("[]").split()))), ranges)
    )

    return df
