import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
from mplsoccer import PyPizza, FontManager
import matplotlib.pyplot as plt

from df_processing import *

def find_percentiles(df, metrics, player_name):
    
    # assert all(x in df.columns for x in ['name'] + metrics)
 
    # Get the player data
    player_stats = df[df['name'] == player_name]
    
    # # Return an empty list if no player found
    # if player_stats.empty:
    #     return []
    
    # Get the player's stats for the selected metrics
    player_stats = player_stats[metrics].iloc[0]
    
    # Return percentiles for each stat in the metrics
    return np.rint(np.array([
        min(99, 100 - stats.percentileofscore(df[param], player_stats[param])) 
        if param == 'poss_lost_90'
        else max(1, min(99, int(stats.percentileofscore(df[param], player_stats[param]))))
        for param in metrics
    ])).astype(int)

def player_pizza_page():
    
    st.write('## Pizza chart Visualization')

    if 'players_df' not in st.session_state:
        st.warning("Please upload players file first!")
        return

    players_df = st.session_state['players_df']
    # only include players with more than 900 minutes played ~ 10 matches
    filtered_df = players_df[players_df['mins'] >= 900]

    player_names = filtered_df['name'].sort_values()
    player_name = st.selectbox(
        'Player Name',
        player_names,
    )

    metrics_dict = {
        'np_xg_90': 'Non-penalty\nxG',
        'shot_90': 'Shot',
        'shot_r': 'Shot\nOn Target %',
        'xa_90': 'Expected\nAssists',
        'ch_c_90': 'Chances\nCreated',
        'op_kp_90': 'Open-play\nKey Passes',
        'op_cr_r': 'Open-play\nCross %',
        'op_crs_a_90': 'Open-play\nCross Attempts',
        'drb_90': 'Dribbles\nCompleted',
        'pas_r': 'Pass\nCompleted %',
        'ps_a_90': 'Pass\nAttempts',
        'pr_passes_90': 'Progressive\nPasses',
        'pr_passes_r': 'Progressive\nPasses %',
        'net_poss_90': 'Net\nPossession Gain',
        'padj_def_act_90': 'PAdj\nDef. Actions',
        'padj_pres_a_90': 'PAdj\nPress. Attempts',
        'hdr_r': 'Aerial Duels\nWon %',
        'aer_a_90': 'Aerial Duels\nAttempts'
    }

    # style formatting
    font_normal = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Regular.ttf')
    font_italic = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Italic.ttf')
    font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/RobotoSlab[wght].ttf')

    # color for the slices and text
    slice_colors = ["#1A78CF"] * 8 + ["#FF9300"] * 6 + ["#D70232"] * 4
    text_colors = ["#000000"] * 14 + ["#F2F2F2"] * 4

    player_percentiles = find_percentiles(players_df, metrics_dict.keys(), player_name)

    if not len(player_percentiles):
        print('Player not found')
        return

    baker = PyPizza(
        params=metrics_dict.values(),       # list of parameters
        # background_color="#030338",         # background color
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
        figsize=(9, 9.5),                # adjust figsize according to your need
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
            players_df[players_df['name'] == player_name]['mins'].values[0]
        ),
        fontsize=14,
        fontproperties=font_normal.prop,
        color="#000000",
        ha="center",
    )
    
    st.pyplot(fig)
