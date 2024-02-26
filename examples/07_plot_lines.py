import pandas as pd

from ranking_aggregation.disk_operations.disk_operations import get_disk_path

from utils import add_profile_type, check_create_file


def generate_plot(df: pd.DataFrame, mallow_disps: list[str] = None, voters: list[float] = None, img_path: str = None):
    """
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe with the data to plot.
    mallow_disps : list[str]
        The Mallow's dispersions to plot. Optional, if None all the Mallow's dispersions are plotted.
    voters : list[float]
        The number of voters to plot. Optional, if None all the number of voters are plotted.
    img_path : str
        The path to save the image. Optional, if None the image is not saved.

    Returns
    -------
    fig : plotly.graph_objs.Figure
        The plot figure
    """
    if mallow_disps is not None:
        df.loc[:, "mallow_disp"] = df["mallow_disp"].astype(float)
        df = df[df["mallow_disp"].isin(mallow_disps)]

    if voters is not None:
        df.loc[:, "num_voters"] = df["num_voters"].astype(float)
        df = df[df["num_voters"].isin(voters)]

    df.loc[:, "mallow_disp"] = df["mallow_disp"].astype(str)

    df_grouped = (
        df.groupby(["num_alternatives", "num_voters", "mallow_disp", "profile_type"])
        .size()
        .unstack(fill_value=0)
        .stack()
        .reset_index(name="count")
    )

    fig = px.line(
        df_grouped,
        x="num_voters",
        y="count",
        color="profile_type",
        facet_col="num_alternatives",
        facet_row="mallow_disp",
        # text="count",
        # text=df_grouped["count"].apply(lambda x: x if x >= 10 else None),
        category_orders={"profile_type": ["NC", "CW", "CR"]},
        color_discrete_map={"CR": "#7F27FF", "CW": "#009d9a", "NC": "#012749"},
        labels={
            "mallow_disp": "Mallow's disp",
            "count": "Number of rankings",
            "num_alternatives": "Alternatives",
            "num_voters": "Voters",
            "profile_type": "Profile type",
        },
    )

    fig.update_yaxes(
        # showticklabels=False,
        title_text="",
        showline=True,
        linewidth=1,
        linecolor="#323232",
        mirror=True,
        range=[0, 110],
        gridcolor="#929292",
        gridwidth=0.5,
        dtick=25,
    )

    fig.update_xaxes(
        title_text="", showline=True, linewidth=1, linecolor="#323232", mirror=True, gridcolor="#929292", gridwidth=0.5
    )

    fig.update_xaxes(showticklabels=True, row=1, col=1)
    fig.update_xaxes(showticklabels=True, row=1, col=2)
    fig.update_xaxes(showticklabels=True, row=1, col=3)
    fig.update_xaxes(showticklabels=True, row=1, col=4)

    # Update text in facet titles
    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("=", ": ")))

    fig.update_layout(
        font=dict(family="Times New Roman", size=14),
        plot_bgcolor="white",
        legend=dict(orientation="h", y=-0.4, x=0.5, xanchor="center", yanchor="bottom"),
        # xaxis_title_standoff=0.5,
        # yaxis_title_standoff=10,
        autosize=False,
        height=1800,
        width=1000,
        # uniformtext_minsize=11,
        # uniformtext_mode="hide",
    )

    fig.update_xaxes(title_text="Voters", row=1, col=2)
    # fig.update_xaxes(title_text="Alternatives", row=1, col=2)
    fig.update_yaxes(title_text="Number of rankings", row=2, col=1)

    if img_path is not None:
        check_create_file(img_path)
        # fig.write_image(img_path, format="png", scale=6)
        fig.write_image(img_path, format=img_path.split(".")[-1], scale=6)
    else:
        fig.show()

    return fig


if __name__ == "__main__":
    import plotly.io as pio
    import plotly.express as px

    pio.renderers.default = "notebook"

    PATH_FOLDER = f"{get_disk_path()}/profiles/mallow/metrics/"
    IMG_PATH_FOLDER = f"{get_disk_path()}/img/"
    COMB_CSV_FILE_NAME = "metrics_profile_mallow.csv"

    # MALLOW_DISPS_TO_PLOT = [0.5, 0.6, 0.7, 0.75, 0.80, 0.85, 0.90, 0.95, 1.0]
    # MALLOW_DISPS_TO_PLOT = [0.1, 0.4, 0.7, 1.0]

    VOTERS_TO_PLOT = [10, 20, 30, 40, 50, 100, 150, 200, 300, 400]

    df = pd.read_csv(PATH_FOLDER + COMB_CSV_FILE_NAME)

    df = add_profile_type(df)

    fig = generate_plot(
        df, voters=VOTERS_TO_PLOT
    )  # ,  MALLOW_DISPS_TO_PLOT, img_path=IMG_PATH_FOLDER + "plot_cuadro_caepia_tfg_miguel.png")
