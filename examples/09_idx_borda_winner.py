import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ranking_aggregation.disk_operations.disk_operations import get_disk_path

from utils import load_df_metrics, check_create_file, add_borda_winner_index, add_borda_index, add_borda_diff


def generate_line_plot(
    df: pd.DataFrame,
    col_to_plot: str,
    mallow_disps: list[str] = None,
    voters: list[float] = None,
    img_path: str = None,
    plot_with_px=True,
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
    plot_with_px : bool
        If True, the plot is generated with plotly express; if False, with plotly graph objects.

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
    df = df[["num_alternatives", "num_voters", "mallow_disp", col_to_plot]]

    # df_grouped = df.groupby(["num_alternatives", "num_voters", "mallow_disp"]).mean().reset_index()

    df_grouped = df.groupby(["num_alternatives", "num_voters", "mallow_disp"]).agg({col_to_plot: ["mean", "std"]})

    df_grouped.columns = ["_".join(col).strip() for col in df_grouped.columns.values]
    df_grouped = df_grouped.reset_index()

    if plot_with_px:
        fig = px.line(
            df_grouped,
            x="mallow_disp",
            y=f"{col_to_plot}_mean",
            facet_col="num_voters",
            facet_row="num_alternatives",
            labels={
                "mallow_disp": "Mallows model dispersion",
                "num_alternatives": "Alternatives",
                "num_voters": "Voters",
                "borda_winner_idx": "Mean Borda winner alternative index",
            },
        )

        fig.update_xaxes(title_text="Mallows model dispersion", row=1, col=3)

        if col_to_plot == "borda_winner_idx":
            fig.update_yaxes(title_text="Mean index of the Borda winner alternative", row=2, col=1)
        elif col_to_plot == "borda_2_idx":
            fig.update_yaxes(title_text="Mean index of the second Borda alternative", row=2, col=1)
        elif col_to_plot == "borda_diff_0_1":
            fig.update_yaxes(title_text="Mean difference between the first and second Borda alternative", row=2, col=1)

        # Update text in facet titles
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("=", ": ")))

        fig.update_xaxes(title_text="")
        fig.update_yaxes(title_text="")
    else:
        # Get number of different alternatives and voters
        num_rows = len(df_grouped["num_alternatives"].unique())
        num_cols = len(df_grouped["num_voters"].unique())

        y_axis_title = None
        if col_to_plot == "borda_winner_idx":
            y_axis_title = "Mean index of the Borda winner alternative"
        elif col_to_plot == "borda_2_idx":
            y_axis_title = "Mean index of the second Borda alternative"
        elif col_to_plot == "borda_diff_0_1":
            y_axis_title = "Mean difference between the first and second Borda alternative"

        # Create subplots, one for each combination of alternatives and voters
        fig = make_subplots(
            rows=num_rows,
            cols=num_cols,
            shared_xaxes="all",
            shared_yaxes="all",
            vertical_spacing=0.05,
            x_title="Mallows model dispersion",
            y_title=y_axis_title,
        )

        for i, num_alternatives in enumerate(df_grouped["num_alternatives"].unique()):
            for j, num_voters in enumerate(df_grouped["num_voters"].unique()):

                filtered_df = df_grouped[
                    (df_grouped["num_voters"] == num_voters) & (df_grouped["num_alternatives"] == num_alternatives)
                ]

                filtered_df.loc[:, f"{col_to_plot}_upper"] = (
                    filtered_df[f"{col_to_plot}_mean"] + filtered_df[f"{col_to_plot}_std"]
                )
                filtered_df.loc[:, f"{col_to_plot}_lower"] = (
                    filtered_df[f"{col_to_plot}_mean"] - filtered_df[f"{col_to_plot}_std"]
                )

                fig.add_trace(
                    go.Scatter(
                        x=pd.concat([filtered_df["mallow_disp"], filtered_df["mallow_disp"][::-1]]),
                        y=pd.concat([filtered_df[f"{col_to_plot}_upper"], filtered_df[f"{col_to_plot}_lower"][::-1]]),
                        fill="toself",
                        fillcolor="rgba(0,100,80,0.2)",
                        line_color="rgba(0,100,80,1)",
                        mode="markers",
                        marker_symbol="star-diamond",
                        marker_size=3,
                        showlegend=False,
                    ),
                    row=i + 1,
                    col=j + 1,
                )

                fig.add_trace(
                    go.Scatter(
                        x=filtered_df["mallow_disp"],
                        y=filtered_df[f"{col_to_plot}_mean"],
                        mode="lines",
                        line_color="rgba(0,100,80,1)",
                        line_width=2,
                    ),
                    row=i + 1,
                    col=j + 1,
                )

        fig.update_layout(title_x=0.5, showlegend=False)  # title="Line Plot",

        # for i in range(num_rows):
        #     for j in range(num_cols):
        #         fig.update_xaxes(showticklabels=False, row=i + 1, col=j + 1)
        #         fig.update_yaxes(showticklabels=False, row=i + 1, col=j + 1)

        # for i, num_alternatives in enumerate(df_grouped["num_alternatives"].unique()):
        #     fig.update_yaxes(title_text=f"Alternatives: {num_alternatives}", side="right", row=i + 1, col=num_cols)

        # for j, num_voters in enumerate(df_grouped["num_voters"].unique()):
        #     fig.update_xaxes(title_text=f"Voters: {num_voters}", side="top", row=1, col=j + 1, title_standoff=0)

        # fig.update_xaxes(matches="x")
        # fig.update_yaxes(matches="y")

    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="#323232",
        mirror=True,
        gridcolor="white",
        gridwidth=0.5,
        # range=[-1, 11],
    )

    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="#323232",
        mirror=True,
        gridcolor="white",
        gridwidth=0.5,
        tickangle=90,
    )

    fig.update_layout(
        font=dict(family="Times New Roman", size=13.33),
        plot_bgcolor="#f2f2f2",
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", yanchor="bottom", traceorder="reversed"),
        # xaxis_title_standoff=0.5,
        # yaxis_title_standoff=10,
        autosize=False,
        height=800,
        width=1100,
    )

    if img_path is not None:
        check_create_file(img_path)
        fig.write_image(img_path, format=img_path.split(".")[-1], scale=6)

    fig.show()

    return fig


if __name__ == "__main__":
    import plotly.io as pio

    pio.renderers.default = "notebook"

    PATH_FOLDER = f"{get_disk_path()}/profiles/mallow/metrics/"
    IMG_PATH_FOLDER = f"{get_disk_path()}/img/"
    COMB_CSV_FILE_NAME = "metrics_profile_mallow.csv"

    SAVE_TO_DISK = False  # Save the figure to disk or not

    SUMMARY_PLOT = False  # Generate plot with wider range of Mallows dispersions or range closer to IC

    # Column to plot
    METRICS = {0: "borda_winner_idx", 1: "borda_2_idx", 2: "borda_diff_0_1"}
    COL_TO_PLOT = METRICS[0]

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

    df = add_borda_winner_index(df)  # Add index of the Borda winner alternative

    df = add_borda_index(df, 1)

    df = add_borda_diff(df, 0, 1)

    fig = generate_line_plot(
        df,
        COL_TO_PLOT,
        mallow_disps=MALLOW_DISPS_TO_PLOT,
        voters=VOTERS_TO_PLOT,
        img_path=f"{IMG_PATH_FOLDER}{IMG_NAME}.svg" if SAVE_TO_DISK else None,
        plot_with_px=False,
    )
