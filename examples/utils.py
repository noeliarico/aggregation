# Function to get info about the filename
import os

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
