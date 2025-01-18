import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from mplsoccer import PyPizza, FontManager
from highlight_text import fig_text

from df_processing import *
from utils import FONT_NORMAL_FILE, FONT_ITALIC_FILE, FONT_BOLD_FILE

DEFAULT_SELECTED_METRICS = [
    'np_xg_90', 'shot_90', 'shot_r', 'xa_90', 'ch_c_90', 'op_kp_90',
    'op_cr_r', 'op_crs_a_90', 'drb_90', 'pas_r', 'ps_a_90', 'pr_passes_90',
    'pr_passes_r', 'net_poss_90', 'padj_def_act_90', 'padj_pres_a_90',
    'hdr_r', 'aer_a_90'
]

PER90_METRICS = {
    'gls_90':           {'type': 'att', 'display': 'Goals'},
    'xg_90':            {'type': 'att', 'display': 'xG'},
    'np_xg_90':         {'type': 'att', 'display': 'Non-penalty\nxG'},
    'shot_90':          {'type': 'att', 'display': 'Shots'},
    'shot_r':           {'type': 'att', 'display': 'Shot\nOn Target %'},
    'conv_r':           {'type': 'att', 'display': 'Conversion %'},
    'asts_90':          {'type': 'att', 'display': 'Assists\n%'},
    'xa_90':            {'type': 'att', 'display': 'Expected\nAssists'},
    'ps_a_90':          {'type': 'pos', 'display': 'Passes\nAttempted'},
    'pas_r':            {'type': 'pos', 'display': 'Pass\nCompletion %'},
    'ps_c_90':          {'type': 'pos', 'display': 'Passes\nCompleted'},
    'pr_passes_90':     {'type': 'pos', 'display': 'Progressive\nPasses'},
    'op_kp_90':         {'type': 'att', 'display': 'Open-play\nKey Passes'},
    'op_crs_a_90':      {'type': 'att', 'display': 'Open-play\nCrosses\nAttempted'},
    'op_cr_r':          {'type': 'att', 'display': 'Open-play\nCross %'},
    'op_crs_c':         {'type': 'att', 'display': 'Open-play\nCrosses\nCompleted'},
    'ch_c_90':          {'type': 'att', 'display': 'Chances\nCreated'},
    'drb_90':           {'type': 'pos', 'display': 'Dribbles\nCompleted'},
    'poss_won_90':      {'type': 'pos', 'display': 'Possession\nWon'},
    'poss_lost_90':     {'type': 'pos', 'display': 'Possession\nLost'},
    'tck_90':           {'type': 'def', 'display': 'Tackles Won'},
    'tck_r':            {'type': 'def', 'display': 'Tackle Won %'},
    'k_tck_90':         {'type': 'def', 'display': 'Key Tackles'},
    'blk_90':           {'type': 'def', 'display': 'Blocks'},
    'int_90':           {'type': 'def', 'display': 'Interceptions'},
    'clr_90':           {'type': 'def', 'display': 'Clearances'},
    'aer_a_90':         {'type': 'def', 'display': 'Aerial Duels\nAttempted'},
    'hdr_r':            {'type': 'def', 'display': 'Headers\nWon %'},
    'hdrs_w_90':        {'type': 'def', 'display': 'Headers\nWon'},
    'hdrs_l_90':        {'type': 'def', 'display': 'Headers\nLost'},
    'k_hdrs_90':        {'type': 'def', 'display': 'Key Headers'},
    'pres_a_90':        {'type': 'def', 'display': 'Pressures\nAttempted'},
    'pres_c_90':        {'type': 'def', 'display': 'Pressures\nCompleted'},
    'sprints_90':       {'type': 'def', 'display': 'High-intensity\nSprints'},
    'dist_90':          {'type': 'def', 'display': 'Distance\nCovered'},
    'fls_90':           {'type': 'def', 'display': 'Fouls Made'},
    'fa_90':            {'type': 'def', 'display': 'Fouls Against'},
    'tck_a_90':         {'type': 'def', 'display': 'Tackles\nAttempted'},
    'xg_op_90':         {'type': 'att', 'display': 'xG\nOverperformance'},
    'net_poss_90':      {'type': 'pos', 'display': 'Net\nPossession\nGained'},
    'def_act_90':       {'type': 'def', 'display': 'Defensive\nActions'},
    'pres_r':           {'type': 'def', 'display': 'Pressures\n Completed %'},
    'pr_passes_r':      {'type': 'pos', 'display': 'Progressive\nPasses %'},
    'padj_def_act_90':  {'type': 'def', 'display': 'PAdj\nDef. Actions'},
    'padj_poss_won_90': {'type': 'pos', 'display': 'PAdj\nPossession Won'},
    'padj_pres_a_90':   {'type': 'def', 'display': 'PAdj\nPressures\nAttempted'},
    'padj_blk_90':      {'type': 'def', 'display': 'PAdj\nBlocks'},
    'padj_int_90':      {'type': 'def', 'display': 'PAdj\nInterceptions'},
    'padj_k_tck_90':    {'type': 'def', 'display': 'PAdj\nKey Tackles'},
    'padj_tck_90':      {'type': 'def', 'display': 'PAdj\nTackles Won'}
}

def find_percentiles(df, metrics, player_name):

    # Get the player data
    player_stats = df[df['name'] == player_name]
    assert player_stats.empty is False
    # Get the player's stats for the selected metrics
    player_stats = player_stats[metrics].iloc[0]
    
    # Return percentiles for each stat in the metrics
    return np.rint(np.array([
        min(99, 100 - stats.percentileofscore(df[param], player_stats[param])) 
        if param == 'poss_lost_90'  # poss lost percentile is inversed (more poss lost ~ lower percentile)
        else max(1, min(99, int(stats.percentileofscore(df[param], player_stats[param]))))
        for param in metrics
    ])).astype(int)

def pizza_stats_page():
    
    st.write('## Player Statistics')

    if 'players_df' not in st.session_state:
        st.warning("Please upload players file first!")
        return

    players_df = st.session_state['players_df']

    player_names = players_df['name'].sort_values()
    player_name = st.selectbox(
        label='Select Player',
        options=player_names,
    )

    selected_metrics = st.multiselect(
        label='Select metrics to display',
        options=PER90_METRICS.keys(),
        default=DEFAULT_SELECTED_METRICS
    )
    plot_player_pizza_chart(player_name, players_df, selected_metrics)


def pizza_comparison_page():
    st.write('## Player Comparison')

    if 'players_df' not in st.session_state:
        st.warning("Please upload players file first!")
        return

    players_df = st.session_state['players_df']
    
    player_names = players_df['name'].sort_values()
    player1_name = st.selectbox(
        label='Select Player',
        key='player_1',
        options=player_names,
    )
    player2_name = st.selectbox(
        label='Select Player',
        key='player_2',
        options=player_names,
    )
    selected_metrics = st.multiselect(
        label='Select metrics to display',
        options=PER90_METRICS.keys(),
        default=DEFAULT_SELECTED_METRICS
    )
    plot_compare_pizza_chart(player1_name, player2_name, players_df, selected_metrics)

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
            df[df['name'] == player_name]['mins'].values[0]
        ),
        fontsize=14,
        fontproperties=font_normal.prop,
        color="#000000",
        ha="center",
    )
    
    st.pyplot(fig)

def plot_compare_pizza_chart(player_1_name, player_2_name, df: pd.DataFrame, selected_metrics: list[str]):

    if len(selected_metrics) < 5:
        st.warning('Select minimum 5 metrics for visualization!')
        return

    # style formatting
    font_normal = FontManager(FONT_NORMAL_FILE)
    font_italic = FontManager(FONT_ITALIC_FILE)
    font_bold = FontManager(FONT_BOLD_FILE)

    group_order = {'att': 0, 'pos': 1, 'def': 2}

    sorted_metrics = sorted(
        selected_metrics,
        key=lambda x: (
            group_order[PER90_METRICS[x]['type']],
            selected_metrics.index(x)))

    metrics_display = [PER90_METRICS[metric]['display'] for metric in sorted_metrics]

    player1_percentiles = find_percentiles(df, sorted_metrics, player_1_name)
    player2_percentiles = find_percentiles(df, sorted_metrics, player_2_name)

    # instantiate PyPizza class
    baker = PyPizza(
        params=metrics_display,         # list of parameters
        background_color="#EBEBE9",     # background color
        straight_line_color="#222222",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=1,               # linewidth of last circle
        last_circle_color="#222222",    # color of last circle
        other_circle_ls="-.",           # linestyle for other circles
        other_circle_lw=1               # linewidth for other circles
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        values=player1_percentiles,                     # list of values
        compare_values=player2_percentiles,             # comparison values
        figsize=(10, 10.5),             # adjust figsize according to your need
        kwargs_slices=dict(
            facecolor="#1A78CF", edgecolor="#222222",
            zorder=2, linewidth=1
        ),                          # values to be used when plotting slices
        kwargs_compare=dict(
            facecolor="#FF9300", edgecolor="#222222",
            zorder=2, linewidth=1,
        ),
        kwargs_params=dict(
            color="#000000", fontsize=12,
            fontproperties=font_normal.prop, va="center"
        ),                          # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=12,
            fontproperties=font_normal.prop, zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        ),                          # values to be used when adding parameter-values labels
        kwargs_compare_values=dict(
            color="#000000", fontsize=12, fontproperties=font_normal.prop, zorder=3,
            bbox=dict(edgecolor="#000000", facecolor="#FF9300", boxstyle="round,pad=0.2", lw=1)
        ),                          # values to be used when adding parameter-values labels
    )

    # add title
    fig_text(
        0.515, 0.99,
        "<{}> vs <{}>".format(player_1_name, player_2_name), size=20, fig=fig,
        highlight_textprops=[{"color": '#1A78CF'}, {"color": '#EE8900'}],
        ha="center", fontproperties=font_bold.prop, color="#000000"
    )

    fig.text(
        0.515, 0.942,
        'All stats are percentile ranks & per 90',
        fontsize=14,
        fontproperties=font_normal.prop,
        color="#000000",
        ha="center",
    )

    st.pyplot(fig)