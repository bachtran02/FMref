import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from mplsoccer import PyPizza, FontManager
from highlight_text import fig_text

from df_processing import *
from player_df import PlayerDF
from utils import FONT_NORMAL_FILE, FONT_ITALIC_FILE, FONT_BOLD_FILE

DEFAULT_SELECTED_METRICS = [
    NP_XG_90, SHOT_90, SHOT_R, XA_90, CH_C_90, OP_KP_90,
    OP_CR_R, OP_CRS_A_90, DRB_90, PAS_R, PS_A_90, PR_PASSES_90,
    PR_PASSES_R, POSS_WON_90, POSS_LOST_90, DEF_ACT_90, PRES_R, PRES_A_90,
    HDR_R, AER_A_90
]

PER90_METRICS = {
    GLS_90:           {'type': 'att', 'display': 'Goals'},
    XG_90:            {'type': 'att', 'display': 'xG'},
    NP_XG_90:         {'type': 'att', 'display': 'Non-penalty\nxG'},
    SHOT_90:          {'type': 'att', 'display': 'Shots'},
    SHOT_R:           {'type': 'att', 'display': 'Shot\nOn Target %'},
    CONV_R:           {'type': 'att', 'display': 'Conversion %'},
    XG_OP_90:         {'type': 'att', 'display': 'xG\nOverperformance'},

    ASTS_90:          {'type': 'att', 'display': 'Assists'},
    XA_90:            {'type': 'att', 'display': 'Expected\nAssists'},
    PS_A_90:          {'type': 'pos', 'display': 'Passes\nAttempted'},
    PAS_R:            {'type': 'pos', 'display': 'Pass\nCompletion %'},
    PS_C_90:          {'type': 'pos', 'display': 'Passes\nCompleted'},
    PR_PASSES_90:     {'type': 'pos', 'display': 'Progressive\nPasses'},
    PR_PASSES_R:      {'type': 'pos', 'display': 'Progressive\nPasses %'},
    OP_KP_90:         {'type': 'att', 'display': 'Open-play\nKey Passes'},
    OP_CRS_A_90:      {'type': 'att', 'display': 'Open-play\nCrosses\nAttempted'},
    OP_CR_R:          {'type': 'att', 'display': 'Open-play\nCross %'},
    OP_CRS_C_90:      {'type': 'att', 'display': 'Open-play\nCrosses\nCompleted'},
    CH_C_90:          {'type': 'att', 'display': 'Chances\nCreated'},
    DRB_90:           {'type': 'pos', 'display': 'Dribbles\nCompleted'},
    POSS_WON_90:      {'type': 'pos', 'display': 'Possession\nWon'},
    POSS_LOST_90:     {'type': 'pos', 'display': 'Possession\nLost'},
    POSS_NET_90:      {'type': 'pos', 'display': 'Possession\nNet'},
    FA_90:            {'type': 'pos', 'display': 'Fouls Against'},

    TCK_90:           {'type': 'def', 'display': 'Tackles Won'},
    TCK_R:            {'type': 'def', 'display': 'Tackle Won %'},
    K_TCK_90:         {'type': 'def', 'display': 'Key Tackles'},
    TCK_A_90:         {'type': 'def', 'display': 'Tackles\nAttempted'},
    BLK_90:           {'type': 'def', 'display': 'Blocks'},
    INT_90:           {'type': 'def', 'display': 'Interceptions'},
    CLR_90:           {'type': 'def', 'display': 'Clearances'},
    DEF_ACT_90:       {'type': 'def', 'display': 'Defensive\nActions'},
    AER_A_90:         {'type': 'def', 'display': 'Aerial Duels\nAttempted'},
    HDR_R:            {'type': 'def', 'display': 'Headers\nWon %'},
    HDRS_W_90:        {'type': 'def', 'display': 'Headers\nWon'},
    HDRS_L_90:        {'type': 'def', 'display': 'Headers\nLost'},
    K_HDRS_90:        {'type': 'def', 'display': 'Key Headers'},
    PRES_A_90:        {'type': 'def', 'display': 'Pressures\nAttempted'},
    PRES_C_90:        {'type': 'def', 'display': 'Pressures\nCompleted'},
    PRES_R:           {'type': 'def', 'display': 'Pressures\n Completed %'},
    SPRINTS_90:       {'type': 'def', 'display': 'High-intensity\nSprints'},
    DIST_90:          {'type': 'def', 'display': 'Distance\nCovered'},
    FLS_90:           {'type': 'def', 'display': 'Fouls Made'},
}

def find_percentiles(df, metrics, player_name):
    # Get the player data
    player_stats = df[df[PLAYER_NAME] == player_name]
    assert not player_stats.empty, f"No data found for player: {player_name}"
    
    # Get the player's stats for the selected metrics
    player_stats = player_stats[metrics].iloc[0]
    
    # Calculate percentiles, handling NaN values
    percentiles = [
        min(99, 100 - stats.percentileofscore(df[param].dropna(), player_stats[param]))
        if param.startswith('Poss Lost')  # inverse for 'Poss Lost'
        else max(1, min(99, int(np.nan_to_num(stats.percentileofscore(df[param].dropna(), player_stats[param]), nan=1))))
        for param in metrics
    ]
    
    # Convert to integers after ensuring no NaN values
    return np.rint(np.array(percentiles)).astype(int)

def player_statistics_page():
    assert 'player_df' in st.session_state
    player_df: PlayerDF = st.session_state['player_df']

    st.write('## Player Statistics')
    if player_df.is_empty():
        st.warning('Please upload player file first.')
        return        

    df = player_df.get_dataframe()

    # TODO: handle duplicate player names
    player_names = df[PLAYER_NAME].sort_values()
    player_name = st.selectbox(label='Select Player', options=player_names)

    display_player_statistics(player_name)
    # selected_metrics = st.multiselect(
    #     label='Select metrics to display',
    #     options=PER90_METRICS.keys(),
    #     default=DEFAULT_SELECTED_METRICS
    # )
    # plot_player_pizza_chart(player_name, df, selected_metrics)

def display_player_statistics(player_name: str):
    assert 'player_df' in st.session_state
    player_df: PlayerDF = st.session_state['player_df']

    player = player_df.get_player_by_name(player_name)

    # Display basic information
    st.write(f'#### {player_name}')
    st.write(f'**Position:** {player[PLAYER_POSITION]} ▪  **Footed**: {player[PLAYER_PREFERRED_FOOT]}')
    st.write(f'{player[PLAYER_HEIGHT]}cm, {player[PLAYER_WEIGHT]}kg')
    st.write(f'**Age**: {player[PLAYER_AGE]}')
    st.write(f'**Nationality**: {player[PLAYER_NAT]}')
    st.write(f'**Club**: {player[PLAYER_CLUB]}')
    st.write(f'**Wages**: £{round(player[PLAYER_SALARY]):,} Weekly')

# def pizza_comparison_page():
#     st.write('## Player Comparison')

#     if 'players_df' not in st.session_state:
#         st.warning("Please upload players file first!")
#         return

#     players_df = st.session_state['players_df']
    
#     player_names = players_df['name'].sort_values()
#     player1_name = st.selectbox(
#         label='Select Player',
#         key='player_1',
#         options=player_names,
#     )
#     player2_name = st.selectbox(
#         label='Select Player',
#         key='player_2',
#         options=player_names,
#     )
#     selected_metrics = st.multiselect(
#         label='Select metrics to display',
#         options=PER90_METRICS.keys(),
#         default=DEFAULT_SELECTED_METRICS
#     )
#     plot_compare_pizza_chart(player1_name, player2_name, players_df, selected_metrics)

def plot_player_pizza_chart(player_name, df: pd.DataFrame, selected_metrics: list[str]):

    if len(selected_metrics) < 5:
        st.warning('Select minimum 5 metrics for visualization!')
        return

    # style formatting
    font_normal = FontManager(FONT_NORMAL_FILE)
    # font_italic = FontManager(FONT_ITALIC_FILE)
    font_bold = FontManager(FONT_BOLD_FILE)

    group_order = {'att': 0, 'pos': 1, 'def': 2}
    sorted_metrics = sorted(
        selected_metrics,
        key=lambda x: (
            group_order[PER90_METRICS[x]['type']],
            selected_metrics.index(x)))

    metrics_display = []
    type_count = {}
    for metric in sorted_metrics:
        # count number of metrics in each category
        t = PER90_METRICS[metric]['type']
        type_count[t] = type_count.get(t, 0) + 1
        # display name for metric
        metrics_display.append(PER90_METRICS[metric]['display'])

    blue, yellow, red = type_count.get('att', 0), type_count.get('pos', 0), type_count.get('def', 0)
    slice_colors = ["#1A78CF"] * blue + ["#FF9300"] * yellow + ["#D70232"] * red
    text_colors = ["#000000"] * (blue + yellow) + ["#F2F2F2"] * red

    player_percentiles = find_percentiles(df, sorted_metrics, player_name)

    baker = PyPizza(
        params=metrics_display,             # list of parameters
        # background_color="#030338",       # background color
        straight_line_color="#222222",      # color for straight lines
        straight_line_lw=1,                 # linewidth for straight lines
        last_circle_lw=1,                   # linewidth of last circle
        last_circle_color="#222222",        # color of last circle
        other_circle_ls="-.",               # linestyle for other circles
        other_circle_lw=1                   # linewidth for other circles
    )
    
    # plot pizza
    fig, ax = baker.make_pizza(
        player_percentiles,
        figsize=(8, 8.3),                # adjust figsize according to your need
        color_blank_space="same",        # use same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#F2F2F2", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            color="#000000", fontsize=11,
            fontproperties=font_normal.prop, va="center"
        ),                               # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=11,
            fontproperties=font_normal.prop, zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                                # values to be used when adding parameter-values
    )

    # Add title and auto adjust title to be in the center of the plot
    fig.text(
        0.505,
        1,
        player_name,
        fontsize=20,
        fontproperties=font_bold.prop,
        color="#000000",
        ha="center",
    )

    # Add a subtitle and auto adjust subtitle to be in the center of the plot
    fig.suptitle(
        "{} minutes played | All stats are percentile ranks & per 90".format(
            df[df[PLAYER_NAME] == player_name][MINS].values[0]
        ),
        fontsize=14,
        fontproperties=font_normal.prop,
        color="#000000",
        ha="center",
    )
    
    st.pyplot(fig)

# def plot_compare_pizza_chart(player_1_name, player_2_name, df: pd.DataFrame, selected_metrics: list[str]):

#     if len(selected_metrics) < 5:
#         st.warning('Select minimum 5 metrics for visualization!')
#         return

#     # style formatting
#     font_normal = FontManager(FONT_NORMAL_FILE)
#     font_italic = FontManager(FONT_ITALIC_FILE)
#     font_bold = FontManager(FONT_BOLD_FILE)

#     group_order = {'att': 0, 'pos': 1, 'def': 2}

#     sorted_metrics = sorted(
#         selected_metrics,
#         key=lambda x: (
#             group_order[PER90_METRICS[x]['type']],
#             selected_metrics.index(x)))

#     metrics_display = [PER90_METRICS[metric]['display'] for metric in sorted_metrics]

#     player1_percentiles = find_percentiles(df, sorted_metrics, player_1_name)
#     player2_percentiles = find_percentiles(df, sorted_metrics, player_2_name)

#     # instantiate PyPizza class
#     baker = PyPizza(
#         params=metrics_display,         # list of parameters
#         background_color="#EBEBE9",     # background color
#         straight_line_color="#222222",  # color for straight lines
#         straight_line_lw=1,             # linewidth for straight lines
#         last_circle_lw=1,               # linewidth of last circle
#         last_circle_color="#222222",    # color of last circle
#         other_circle_ls="-.",           # linestyle for other circles
#         other_circle_lw=1               # linewidth for other circles
#     )

#     # plot pizza
#     fig, ax = baker.make_pizza(
#         values=player1_percentiles,                     # list of values
#         compare_values=player2_percentiles,             # comparison values
#         figsize=(10, 10.5),             # adjust figsize according to your need
#         kwargs_slices=dict(
#             facecolor="#1A78CF", edgecolor="#222222",
#             zorder=2, linewidth=1
#         ),                          # values to be used when plotting slices
#         kwargs_compare=dict(
#             facecolor="#FF9300", edgecolor="#222222",
#             zorder=2, linewidth=1,
#         ),
#         kwargs_params=dict(
#             color="#000000", fontsize=12,
#             fontproperties=font_normal.prop, va="center"
#         ),                          # values to be used when adding parameter
#         kwargs_values=dict(
#             color="#000000", fontsize=12,
#             fontproperties=font_normal.prop, zorder=3,
#             bbox=dict(
#                 edgecolor="#000000", facecolor="cornflowerblue",
#                 boxstyle="round,pad=0.2", lw=1
#             )
#         ),                          # values to be used when adding parameter-values labels
#         kwargs_compare_values=dict(
#             color="#000000", fontsize=12, fontproperties=font_normal.prop, zorder=3,
#             bbox=dict(edgecolor="#000000", facecolor="#FF9300", boxstyle="round,pad=0.2", lw=1)
#         ),                          # values to be used when adding parameter-values labels
#     )

#     # add title
#     fig_text(
#         0.515, 0.99,
#         "<{}> vs <{}>".format(player_1_name, player_2_name), size=20, fig=fig,
#         highlight_textprops=[{"color": '#1A78CF'}, {"color": '#EE8900'}],
#         ha="center", fontproperties=font_bold.prop, color="#000000"
#     )

#     fig.text(
#         0.515, 0.942,
#         'All stats are percentile ranks & per 90',
#         fontsize=14,
#         fontproperties=font_normal.prop,
#         color="#000000",
#         ha="center",
#     )

#     st.pyplot(fig)