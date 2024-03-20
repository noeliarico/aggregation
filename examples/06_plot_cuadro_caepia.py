import os
import pandas as pd
from fnmatch import fnmatch

import plotly.io as pio
import plotly.express as px
import plotly.colors as pc

from ranking_aggregation.disk_operations.disk_operations import get_disk_path

from utils import get_info_from_name, check_create_file, add_profile_type, add_borda_winner_pctl


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
            if fnmatch(name, "*.csv") and name != "metrics_profile_mallow.csv":
                new_df = pd.read_csv(path + name)

                info = get_info_from_name(name, metrics=True)

                new_df.insert(3, "mallow_disp", [info["mallow_disp"] for i in range(len(new_df))])

                df = pd.concat([df, new_df]).reset_index(drop=True)

    df.to_csv(dirpath + comb_csv_file_name, mode="w+")  # mode overwrite

    return df


def generate_plot(
    df: pd.DataFrame, col_to_plot: str, mallow_disps: list[str] = None, voters: list[float] = None, img_path: str = None
):
    """
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe with the data to plot.
    col_to_plot : str
        The column of the df to plot.
    mallow_disps : list[str]
        The Mallows dispersions to plot. Optional, if None all the Mallows dispersions are plotted.
    voters : list[float]
        The number of voters to plot. Optional, if None all the number of voters are plotted.
    img_path : str
        The path to save the image. Optional, if None the image is not saved.

    Returns
    -------
    fig : plotly.graph_objs.Figure
        The plot figure
    """
    if col_to_plot not in df.columns:
        raise ValueError(f"The column {col_to_plot} does not exist in the dataframe.")

    # Filter out the Mallows dispersions and the number of voters
    if mallow_disps is not None:
        df.loc[:, "mallow_disp"] = df["mallow_disp"].astype(float)
        df = df[df["mallow_disp"].isin(mallow_disps)]

    if voters is not None:
        df.loc[:, "num_voters"] = df["num_voters"].astype(float)
        df = df[df["num_voters"].isin(voters)]

    # Convert the Mallows dispersions to string again to plot them as cathegorical variables
    df.loc[:, "mallow_disp"] = df["mallow_disp"].astype(str)

    # Group the data by the number of alternatives, the number of voters, the Mallows dispersion and the profile type
    df_grouped = (
        df.groupby(["num_alternatives", "num_voters", "mallow_disp", col_to_plot]).size().reset_index(name="count")
    )

    cat_orders = {"profile_type": ["NC", "CW", "CR"]}
    color_palette = {"CR": "#f9f3dd", "CW": "#c7d4b8", "NC": "#8fc0a9"}

    if "borda_winner_pctl" in df.columns:
        borda_values = df["borda_winner_pctl"].unique()
        n_b_v = len(borda_values)

        cat_orders["borda_winner_pctl"] = sorted(
            borda_values,
            key=lambda x: (float(x.split("-")[0].strip("%")), float(x.split("-")[1].strip("%"))),
            reverse=True,
        )

        color_palette.update(
            dict(
                zip(
                    cat_orders["borda_winner_pctl"],
                    pc.sample_colorscale(
                        pc.make_colorscale(["#f9f3dd", "#8fc0a9", "#567365"]),
                        [(1 / (n_b_v - 1)) * i for i in range(n_b_v)],
                    ),
                )
            )
        )

    # Plot the data
    fig = px.bar(
        df_grouped,
        x="mallow_disp",
        y="count",
        color=col_to_plot,
        facet_col="num_voters",
        facet_row="num_alternatives",
        # text="count",
        text=df_grouped["count"].apply(lambda x: x if x >= 11 else None),
        category_orders=cat_orders,
        color_discrete_map=color_palette,
        labels={
            "mallow_disp": "Mallows model dispersion",
            "count": "Number of profiles",
            "num_alternatives": "Alternatives",
            "num_voters": "Voters",
            "profile_type": "Profile type",
            "borda_winner_pctl": "Maximum Borda Score percentage",
        },
    )

    y_margin = (df_grouped["count"].max() - df_grouped["count"].min()) * 0.05

    fig.update_yaxes(
        showticklabels=False,  # Do not show tick labels
        title_text="",  # Hide the title in all y axes (afterwards one will be added)
        showline=True,  # Show y axis line
        linewidth=1,
        linecolor="#323232",
        mirror=True,
        range=[df_grouped["count"].min() - y_margin, df_grouped["count"].max() + y_margin],
    )

    fig.update_xaxes(
        title_text="",  # Hide the title in all y axes (afterwards one will be added)
        showline=True,  # Show x axis line
        linewidth=1,
        linecolor="#323232",
        mirror=True,
        # tickmode="linear",
        # dtick=0.05,
        # tick0=0.7,
        # tickmode="array",
        # tickvals=[0.7 + 0.05 * i for i in range(len(df["mallow_disp"].unique()))],
        # ticktext=[f"{0.7 + 0.05 * i:.1f}" if i % 2 == 0 else "" for i in range(len(df["mallow_disp"].unique()))],
        # tickangle=0,
    )

    # Uncomment to show grid of ticks in last row of x axes
    # for i in range(len(df["num_voters"].unique())):
    #     fig.update_xaxes(showgrid=True, ticks="outside", tickson="labels", ticklen=5, row=1, col=1 + i)

    # Add titles to each axis
    fig.update_xaxes(title_text="Mallows model dispersion", row=1, col=3)
    fig.update_yaxes(title_text="Number of profiles", row=2, col=1)

    # Update text in facet titles
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("=", ": ")))

    # Update the labels of each bar
    fig.update_traces(
        textposition="inside",
        textangle=0,
        marker_line_width=1.5,
        marker_line_color="black",
        textfont_family="Times New Roman",
        textfont_size=13.33,
    )

    # Update the layout
    fig.update_layout(
        font=dict(family="Times New Roman", size=13.33),
        plot_bgcolor="white",
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", yanchor="bottom", traceorder="reversed"),
        xaxis_title_standoff=0.5,
        yaxis_title_standoff=10,
        autosize=False,
        height=800,
        width=1100,
        # uniformtext_minsize=13.33,
        # uniformtext_mode="hide",
    )

    if img_path is not None:
        check_create_file(img_path)
        # fig.write_image(img_path, format="png", scale=6)
        fig.write_image(img_path, format=img_path.split(".")[-1], scale=6)

    fig.show()

    return fig


if __name__ == "__main__":
    pio.renderers.default = "notebook"

    PATH_FOLDER = f"{get_disk_path()}/profiles/mallow/metrics/"
    IMG_PATH_FOLDER = f"{get_disk_path()}/img/"
    COMB_CSV_FILE_NAME = "metrics_profile_mallow.csv"

    SAVE_TO_DISK = False  # Save the figure to disk or not

    SUMMARY_PLOT = False  # Generate plot with wider range of Mallows dispersions or range closer to IC

    COL_TO_PLOT = "borda_winner_pctl"  # "profile_type"  # Column to plot

    BORDA_RANGES = [0.1 * i for i in range(1, 10)]  # Rango of percentiles of Borda max winner rate

    if SUMMARY_PLOT:
        IMG_NAME = f"n_altn_vs_n_voters_vs_broad_disp_{COL_TO_PLOT}"
        MALLOW_DISPS_TO_PLOT = [0.1, 0.4, 0.7, 1.0]  # Range of Mallows dispersions to plot
    else:
        IMG_NAME = f"n_altn_vs_n_voters_vs_ic_close_disp_{COL_TO_PLOT}"
        # MALLOW_DISPS_TO_PLOT = [0.5, 0.6, 0.7, 0.80, 0.90, 1.0]
        MALLOW_DISPS_TO_PLOT = [0.7, 0.75, 0.80, 0.85, 0.90, 0.95, 1.0]  # Range of Mallows dispersions to plot

    VOTERS_TO_PLOT = [10, 50, 100, 200, 500, 1000]  # Range of voters to plot

    # df = load_df_metrics(PATH_FOLDER, COMB_CSV_FILE_NAME)

    df = pd.read_csv(PATH_FOLDER + COMB_CSV_FILE_NAME)

    df = add_profile_type(df)  # Add profile type column (CR, CW, NC)

    df = add_borda_winner_pctl(df, BORDA_RANGES)  # Add Borda max winner rate percentiles

    fig = generate_plot(
        df,
        COL_TO_PLOT,
        mallow_disps=MALLOW_DISPS_TO_PLOT,
        voters=VOTERS_TO_PLOT,
        img_path=f"{IMG_PATH_FOLDER}{IMG_NAME}.svg" if SAVE_TO_DISK else None,
    )
