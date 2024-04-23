import pickle
import os
from fnmatch import fnmatch
from ipywidgets import widgets
from ipywidgets.embed import embed_minimal_html
from selenium import webdriver
import numpy as np
import pandas as pd
import time


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


def add_borda_winner_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a new column to the dataframe with the index of the Borda winner alternative.

    The new column is named `borda_winner_idx`.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to modify.

    Returns
    -------
    df : pandas.DataFrame
        The modified dataframe.
    """
    df["borda_winner_idx"] = df["borda_score_normalized"].apply(
        lambda x: np.argmax(np.array(list(map(float, x.strip("[]").split()))))
    )

    return df


def add_borda_index(df: pd.DataFrame, index: int) -> pd.DataFrame:
    """
    Add a new column to the dataframe with the index of the Borda winner alternative.

    The new column is named `borda_winner_idx`.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to modify.
    index : int
        The index of the Borda alternative. Starting in zero.

    Returns
    -------
    df : pandas.DataFrame
        The modified dataframe.
    """
    index += 1
    df[f"borda_{index}_idx"] = df["borda_score_normalized"].apply(
        lambda x: np.argsort(np.array(list(map(float, x.strip("[]").split()))))[::-1][:index][index - 1]
    )

    return df


def add_borda_diff(df: pd.DataFrame, index1: int, index2: int) -> pd.DataFrame:
    """
    Add a new column to the dataframe with the difference between the Borda scores of the alternatives
    with indexes index1 and index2 (index1 - index2).

    The new column is named `borda_diff_{index1}_{index2}`.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to modify.
    index1 : int
        The index of the first alternative. Starting in zero.
    index2 : int
        The index of the second alternative. Starting in zero.

    Returns
    -------
    df : pandas.DataFrame
        The modified dataframe.
    """
    index1 += 1
    index2 += 1

    def get_borda_diff(borda_list: list) -> float:
        borda_list = np.array(list(map(float, borda_list.strip("[]").split())))
        borda_argsort = np.argsort(borda_list)[::-1]
        borda1 = float(borda_list[borda_argsort[:index1][index1 - 1]])
        borda2 = float(borda_list[borda_argsort[:index2][index2 - 1]])
        return borda1 - borda2

    df[f"borda_diff_{index1-1}_{index2-1}"] = df["borda_score_normalized"].apply(get_borda_diff)

    return df


def load_df_metrics(dirpath: str, comb_csv_file_name: str) -> pd.DataFrame:
    """
    Load all the .csv files in the directory dirpath and return a dataframe.

    Parameters
    ----------
    dirpath : str
        The directory where the .csv files are located.
    comb_csv_file_name : str
        The name to the .csv file where the combination of all .csv files is going to be stored.

    Returns
    -------
    df : pandas.DataFrame
        A dataframe with all the data from the .csv files in the directory.
    """
    # Crear un dataframe vacío
    df = pd.DataFrame()

    # Leer todos los archivos .csv del directorio dirpath
    for path, subdirs, files in os.walk(dirpath):
        for name in files:
            if fnmatch(name, "*.csv") and name != comb_csv_file_name:
                new_df = pd.read_csv(path + name)

                info = get_info_from_name(name, metrics=True)

                new_df.insert(3, "mallow_disp", [info["mallow_disp"] for i in range(len(new_df))])

                df = pd.concat([df, new_df]).reset_index(drop=True)

    df.to_csv(dirpath + comb_csv_file_name, mode="w+", index=False)  # mode overwrite

    return df


def load_list_of_profiles(file_name: str):
    """
    Load a list of profiles from a file.

    Parameters
    ----------
    file_name : str
        The name of the file where the profiles are stored.

    Returns
    -------
    profiles : list
        The list of profiles.
    """
    with open(file_name, "rb") as file_handler:
        profiles = pickle.load(file_handler)
    return profiles


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


def widget_to_png(widget: widgets.Widget, filename: str):
    """
    Save a widget from ipywidgets as an PNG file.

    Parameters
    ----------
    widget : ipywidgets.Widget
        The widget to save as an PNG file.
    filename : str
        The path to save the PNG file.
    """
    temp_html = "export.html"

    # Save the widget as an HTML file
    embed_minimal_html(temp_html, views=[widget], title="Widgets export")

    # Configure the browser to take a screenshot of the widget
    driver = webdriver.Chrome()
    driver.get("file:///" + os.path.abspath(temp_html))

    time.sleep(5)

    driver.set_window_size(720, 1250)

    # Take a screenshot of the widget and save it as an SVG file
    # svg_content = driver.execute_script('return document.getElementsByTagName("body")[0].innerHTML')
    # with open(filename, "w") as f:
    #     f.write(svg_content)

    driver.save_screenshot(filename)

    driver.quit()
    os.remove(temp_html)
