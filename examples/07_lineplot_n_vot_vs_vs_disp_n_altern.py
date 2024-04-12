import pandas as pd
from ipywidgets import widgets
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go
import sys

from ranking_aggregation.disk_operations.disk_operations import get_disk_path

from utils import check_create_file, widget_to_png


def generate_plot(
    df: pd.DataFrame,
    stat_to_plot: str,
    col_x: str = "n_v",
    col_facet_cols: str = "n_a",
    col_colour: str = "m_d",
    mallow_disps: list[str] = None,
    voters: list[float] = None,
    img_path: str = None,
    summary_plot: bool = False,
    show_plot: bool = True,
):
    """
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe with the data to plot.
    stat_to_plot : str
        The statistic to plot. One of "mean" or "std".
    col_x : str
        The column to plot in the x-axis. One of "n_v", "n_a" or "m_d".
    col_facet_cols : str
        The column to divide the plot in facet columns. One of "n_v", "n_a" or "m_d".
    col_colour : str
        The column to use as the colour categories in the plot. One of "n_v", "n_a" or "m_d".
    mallow_disps : list[str]
        The Mallow's dispersions to plot. Optional, if None all the Mallow's dispersions are plotted.
    voters : list[float]
        The number of voters to plot. Optional, if None all the number of voters are plotted.
    img_path : str
        The path to save the image. Optional, if None the image is not saved.
    summary_plot : bool
        If True, the plot is generated with a wider range of Mallows dispersions. If False, the plot is generated with a
        range of Mallows dispersions closer to the IC.
    show_plot : bool
        If True, the plot is displayed. If False, the plot is not displayed.

    Returns
    -------
    fig : plotly.graph_objs.Figure
        The plot figure
    """
    if stat_to_plot not in ["mean", "std", "median"]:
        raise ValueError("stat_to_plot must be one of 'mean' or 'std'.")

    if col_x not in ["n_v", "n_a", "m_d"]:
        raise ValueError("col_x must be one of 'n_v', 'n_a' or 'm_d'.")

    if col_facet_cols not in ["n_v", "n_a", "m_d"]:
        raise ValueError("col_facet_cols must be one of 'n_v', 'n_a' or 'm_d'.")

    if col_colour not in ["n_v", "n_a", "m_d"]:
        raise ValueError("col_colour must be one of 'n_v', 'n_a' or 'm_d'.")

    # Filter out the Mallows dispersions and the number of voters
    if mallow_disps is not None:
        df.loc[:, "mallow_disp"] = df["mallow_disp"].astype(float)
        df = df[df["mallow_disp"].isin(mallow_disps)]

    if voters is not None:
        df.loc[:, "num_voters"] = df["num_voters"].astype(float)
        df = df[df["num_voters"].isin(voters)]

    # Convert the Mallows dispersions to string again to plot them as cathegorical variables
    df.loc[:, "mallow_disp"] = df["mallow_disp"].astype(str)

    df_grouped = df.groupby(["num_alternatives", "num_voters", "mallow_disp"]).agg(
        {"kemeny_dist_norm": ["mean", "std", "median"]}
    )

    df_grouped.columns = ["_".join(col).strip() for col in df_grouped.columns.values]
    df_grouped = df_grouped.reset_index()

    cat_orders = {
        "mallow_disp": sorted(df_grouped["mallow_disp"].unique()),
        "num_voters": sorted(df_grouped["num_voters"].unique()),
        "num_alternatives": sorted(df_grouped["num_alternatives"].unique()),
    }

    color_scale = pc.make_colorscale(
        ["#FFBB5C", "#FF9B50", "#E25E3E", "#C63D2F"]
        if stat_to_plot == "mean"
        else (
            ["#81B214", "#A2D5AB", "#335D2D"] if stat_to_plot == "std" else ["#A9DFDC", "#7FC7D9", "#365486", "#0F1035"]
        )
    )

    color_palette = dict(
        zip(
            cat_orders["mallow_disp"],
            pc.sample_colorscale(
                color_scale,
                [(1 / (len(cat_orders["mallow_disp"]) - 1)) * i for i in range(len(cat_orders["mallow_disp"]))],
            ),
        )
    )

    color_palette.update(
        dict(
            zip(
                cat_orders["num_voters"],
                pc.sample_colorscale(
                    color_scale,
                    [(1 / (len(cat_orders["num_voters"]) - 1)) * i for i in range(len(cat_orders["num_voters"]))],
                ),
            )
        )
    )

    color_palette.update(
        dict(
            zip(
                cat_orders["num_alternatives"],
                pc.sample_colorscale(
                    color_scale,
                    [
                        (1 / (len(cat_orders["num_alternatives"]) - 1)) * i
                        for i in range(len(cat_orders["num_alternatives"]))
                    ],
                ),
            )
        )
    )

    fig = px.line(
        df_grouped,
        x="num_voters" if col_x == "n_v" else "num_alternatives" if col_x == "n_a" else "mallow_disp",
        y=(
            "kemeny_dist_norm_mean"
            if stat_to_plot == "mean"
            else "kemeny_dist_norm_std" if stat_to_plot == "std" else "kemeny_dist_norm_median"
        ),
        color="num_voters" if col_colour == "n_v" else "num_alternatives" if col_colour == "n_a" else "mallow_disp",
        facet_col=(
            "num_voters"
            if col_facet_cols == "n_v"
            else "num_alternatives" if col_facet_cols == "n_a" else "mallow_disp"
        ),
        category_orders=cat_orders,
        color_discrete_map=color_palette,
        labels={
            "mallow_disp": "Mallows model dispersion",
            "num_alternatives": "Alternatives",
            "num_voters": "Voters",
            "kemeny_dist_norm_mean": "Mean normalized Kemeny distance",
            "kemeny_dist_norm_std": "STD of normalized Kemeny distance",
            "kemeny_dist_norm_median": "Median of normalized Kemeny distance",
        },
    )

    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="#323232",
        mirror=True,
        gridcolor="white",
        gridwidth=0.5,
    )

    fig.update_xaxes(
        title_text="", showline=True, linewidth=1, linecolor="#323232", mirror=True, gridcolor="white", gridwidth=0.5
    )

    fig.update_xaxes(
        title_text=(
            "Number of alternatives"
            if col_x == "n_a"
            else "Number of voters" if col_x == "n_v" else "Mallows model dispersion"
        ),
        row=1,
        col=3,
    )

    # Update text in facet titles
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("=", ": ")))

    fig.update_layout(
        font=dict(family="Times New Roman", size=14),
        plot_bgcolor="#F2F2F2",
        legend=dict(orientation="h", y=-0.4, x=0.5, xanchor="center", yanchor="bottom"),
        autosize=False,
        # height=1800,
        # width=1000,
    )

    if img_path is not None:
        filename = img_path.split(".")[0]
        extension = img_path.split(".")[-1]

        m_d = "broad_disp" if summary_plot else "ic_close_disp"

        if "m_d" == col_x:
            col_x = m_d
        if "m_d" == col_facet_cols:
            col_facet_cols = m_d
        if "m_d" == col_colour:
            col_colour = m_d

        img_path = f"{filename}_{stat_to_plot}_{col_facet_cols}_vs_{col_x}_vs_{col_colour}.{extension}"

        check_create_file(img_path)
        fig.write_image(img_path, format=img_path.split(".")[-1], scale=6)

    if show_plot:
        fig.show()

    return fig


def generate_plot_all_metrics(
    df: pd.DataFrame,
    col_x: str = "n_v",
    col_facet_cols: str = "n_a",
    col_colour: str = "m_d",
    mallow_disps: list[str] = None,
    voters: list[float] = None,
    img_path: str = None,
    summary_plot: bool = False,
    show_plot: bool = True,
):
    """
    Generate a widget with all the plots for the metrics. The plots are aligned in a vertical box.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe with the data to plot.
    col_x : str
        The column to plot in the x-axis. One of "n_v", "n_a" or "m_d".
    col_facet_cols : str
        The column to divide the plot in facet columns. One of "n_v", "n_a" or "m_d".
    col_colour : str
        The column to use as the colour categories in the plot. One of "n_v", "n_a" or "m_d".
    mallow_disps : list[str]
        The Mallow's dispersions to plot. Optional, if None all the Mallow's dispersions are plotted.
    voters : list[float]
        The number of voters to plot. Optional, if None all the number of voters are plotted.
    img_path : str
        The path to save the image. Optional, if None the image is not saved.
    summary_plot : bool
        If True, the plot is generated with a wider range of Mallows dispersions. If False, the plot is generated with a
        range of Mallows dispersions closer to the IC.
    show_plot : bool
        If True, the plot is displayed. If False, the plot is not displayed.

    Returns
    -------
    widget : ipywidgets.widgets.widget_box.VBox
        The widget including all the plots.
    """
    metrics_list = ["mean", "std", "median"]

    fig_list = []

    for metric in metrics_list:
        fig = generate_plot(
            df,
            stat_to_plot=metric,
            col_x=col_x,
            col_facet_cols=col_facet_cols,
            col_colour=col_colour,
            mallow_disps=mallow_disps,
            voters=voters,
            img_path=None,
            summary_plot=summary_plot,
            show_plot=False,
        )

        fig_list.append(go.FigureWidget(fig))

    box = widgets.VBox(fig_list)

    if img_path is not None:
        filename = img_path.split(".")[0]
        extension = img_path.split(".")[-1]

        m_d = "broad_disp" if summary_plot else "ic_close_disp"

        if "m_d" == col_x:
            col_x = m_d
        if "m_d" == col_facet_cols:
            col_facet_cols = m_d
        if "m_d" == col_colour:
            col_colour = m_d

        img_path = f"{filename}_{col_facet_cols}_vs_{col_x}_vs_{col_colour}.{extension}"

        widget_to_png(box, img_path)

    # Display the widget if the code is run in a interactive environment
    if hasattr(sys, "ps1") and show_plot:
        display(box)

    return box


if __name__ == "__main__":
    import plotly.io as pio

    pio.renderers.default = "notebook"

    PATH_FOLDER = f"{get_disk_path()}/profiles/mallow/metrics/"
    IMG_PATH_FOLDER = f"{get_disk_path()}/img/"
    COMB_CSV_FILE_NAME = "metrics_profile_mallow.csv"

    SAVE_TO_DISK = True  # Save the figure to disk or not
    IMG_NAME = "norm_kemeny_dist"

    SUMMARY_PLOT = False  # Generate plot with wider range of Mallows dispersions or range closer to IC
    ALL_METRICS = True
    STAT_TO_PLOT = "median"  # Ignored if ALL_METRICS is True

    VOTERS_TO_PLOT = [10, 50, 100, 200, 500, 1000]  # Range of voters to plot

    if SUMMARY_PLOT:
        MALLOW_DISPS_TO_PLOT = [0.1, 0.4, 0.7, 1.0]  # Range of Mallows dispersions to plot
    else:
        # MALLOW_DISPS_TO_PLOT = [0.5, 0.6, 0.7, 0.80, 0.90, 1.0]
        MALLOW_DISPS_TO_PLOT = [0.7, 0.75, 0.80, 0.85, 0.90, 0.95, 1.0]  # Range of Mallows dispersions to plot

    df = pd.read_csv(PATH_FOLDER + COMB_CSV_FILE_NAME)

    if ALL_METRICS:
        box = generate_plot_all_metrics(
            df,
            # img_path=f"{IMG_PATH_FOLDER}{IMG_NAME}.png" if SAVE_TO_DISK else None,
            img_path=(
                f"C:/Users/villarmario/OneDrive - Universidad de Oviedo/compartida_noelia_mario/inv/congresos/2024_ecai/graficos_distancia_kemeny/{IMG_NAME}.png"
                if SAVE_TO_DISK
                else None
            ),
            col_x="n_a",
            col_facet_cols="n_v",
            col_colour="m_d",
            mallow_disps=MALLOW_DISPS_TO_PLOT,
            voters=VOTERS_TO_PLOT,
            summary_plot=SUMMARY_PLOT,
            show_plot=False,
        )
    else:
        fig = generate_plot(
            df,
            stat_to_plot=STAT_TO_PLOT,
            col_x="n_a",
            col_facet_cols="n_v",
            col_colour="m_d",
            mallow_disps=MALLOW_DISPS_TO_PLOT,
            voters=VOTERS_TO_PLOT,
            img_path=f"{IMG_PATH_FOLDER}{IMG_NAME}.svg" if SAVE_TO_DISK else None,
            summary_plot=SUMMARY_PLOT,
        )
