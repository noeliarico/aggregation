import os
import pandas as pd
from fnmatch import fnmatch

from ranking_aggregation.disk_operations.disk_operations import get_disk_path

from utils import get_info_from_name


def load_df_metrics(dirpath: str) -> pd.DataFrame:
    """
    Load all the .csv files in the directory dirpath and return a dataframe.

    Parameters
    ----------
    dirpath : str
        The directory where the .csv files are located.

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
            if fnmatch(name, "*.csv"):
                new_df = pd.read_csv(path + name)

                info = get_info_from_name(name, metrics=True)

                new_df.insert(3, "mallow_disp", [info["mallow_disp"] for i in range(len(new_df))])

                df = pd.concat([df, new_df])

    return df


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
        lambda row: "CR" if row["condorcet_winner"] else "CW" if row["condorcet_weak_winner"] else "NC", axis=1
    )

    return df


if __name__ == "__main__":
    import plotly.io as pio
    import plotly.express as px

    pio.renderers.default = "notebook"

    path_folder = f"{get_disk_path()}/profiles/mallow/metrics/"

    df = load_df_metrics(path_folder)

    df = add_profile_type(df)

    df_grouped = df.groupby(["num_alternatives", "num_voters", "mallow_disp", "profile_type"]).count()

    fig = px.bar(
        df_grouped,
        x=df_grouped.index.get_level_values(2),
        y="culture",
        color=df_grouped.index.get_level_values(3),
        facet_col=df_grouped.index.get_level_values(0),
        facet_row=df_grouped.index.get_level_values(1),
    )

    fig.update_yaxes(matches=None)
    fig.show()
