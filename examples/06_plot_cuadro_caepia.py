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

                df = pd.concat([df, new_df]).reset_index(drop=True)

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
        lambda row: "CR" if row["condorcet_ranking"] else "CW" if row["condorcet_winner"] else "NC", axis=1
    )

    return df


def generate_plot(df):
    df_grouped = (
        df.groupby(["num_alternatives", "num_voters", "mallow_disp", "profile_type"]).size().reset_index(name="count")
    )

    fig = px.bar(
        df_grouped,
        x="mallow_disp",
        y="count",
        color="profile_type",
        facet_col="num_voters",
        facet_row="num_alternatives",
        # text="count",
        text=df_grouped["count"].apply(lambda x: x if x >= 10 else None),
        category_orders={"profile_type": ["NC", "CW", "CR"]},
        color_discrete_map={"CR": "#f9f3dd", "CW": "#c7d4b8", "NC": "#8fc0a9"},
        labels={
            "mallow_disp": "Mallow's dispersion",
            "count": "Number of rankings",
            "num_alternatives": "Alternatives",
            "num_voters": "Voters",
            "profile_type": "Profile type",
        },
    )

    y_margin = (df_grouped["count"].max() - df_grouped["count"].min()) * 0.05

    fig.update_yaxes(
        showticklabels=False,
        title_text="",
        showline=True,
        linewidth=1,
        linecolor="#323232",
        mirror=True,
        range=[df_grouped["count"].min() - y_margin, df_grouped["count"].max() + y_margin],
    )

    fig.update_xaxes(title_text="", showline=True, linewidth=1, linecolor="#323232", mirror=True)

    # Update text in facet titles
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("=", ": ")))

    fig.update_layout(
        font=dict(family="Times New Roman", size=14),
        plot_bgcolor="white",
        legend=dict(orientation="h", y=-0.15, x=0.4, xanchor="center", yanchor="bottom"),
        # xaxis_title="Mallow's dispersion",
        # yaxis_title="Number of rankings",
        xaxis_title_standoff=0.5,
        yaxis_title_standoff=10,
        autosize=False,
        height=600,
        width=1000,
        uniformtext_minsize=14,
    )

    fig.update_xaxes(title_text="Mallow's dispersion", row=1, col=3)
    fig.update_yaxes(title_text="Number of rankings", row=2, col=1)

    fig.update_traces(
        textposition="inside",
        textangle=90,
        marker_line_width=0.6,
        marker_line_color="black",
        textfont_family="Times New Roman",
        textfont_size=14,
    )

    fig.show()

    return fig


if __name__ == "__main__":
    import plotly.io as pio
    import plotly.express as px

    pio.renderers.default = "notebook"

    path_folder = f"{get_disk_path()}/profiles/mallow/metrics/"

    df = load_df_metrics(path_folder)

    df = add_profile_type(df)

    fig = generate_plot(df)
