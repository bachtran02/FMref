from highlight_text import fig_text
from mplsoccer import PyPizza, FontManager
import streamlit as st

from fm_mapping import *
from player_df import PlayerDF
from utils import FONT_NORMAL_FILE, FONT_ITALIC_FILE, FONT_BOLD_FILE

font_normal = FontManager(FONT_NORMAL_FILE)
font_italic = FontManager(FONT_ITALIC_FILE)
font_bold = FontManager(FONT_BOLD_FILE)

DEFAULT_SELECTED_METRICS = [
    NP_XG_90, SHOT_90, SHOT_R, XA_90, CH_C_90, OP_KP_90,
    OP_CR_R, OP_CRS_A_90, DRB_90, PAS_R, PS_A_90, PR_PASSES_90,
    PR_PASSES_R, POSS_WON_90, POSS_LOST_90, DEF_ACT_90, PRES_R, PRES_A_90,
    HDR_R, AER_A_90
]

def player_compare_page():
    assert 'player_df' in st.session_state
    player_df: PlayerDF = st.session_state['player_df']

    st.write('## Player Statistics')
    if player_df.is_empty():
        st.warning('Please upload player file first.')
        return

    df = player_df.get_dataframe()
    player_id_name_map = df[PLAYER_NAME].to_dict()
    
    selected_player_1_id = st.selectbox(
        label='Select Player 1',
        options = player_id_name_map.keys(),
        key='compare_player_1',
        format_func=lambda x: player_id_name_map[x],
        help='Select a player to compare'
    )

    selected_player_2_id = st.selectbox(
        label='Select Player 2',
        options = player_id_name_map.keys(),
        key='compare_player_2',
        format_func=lambda x: player_id_name_map[x],
        help='Select a player to compare'
    )

    player_1_data = player_df.get_player_row_by_id(selected_player_1_id)
    player_2_data = player_df.get_player_row_by_id(selected_player_2_id)

    # find common position groups
    common_groups = []
    for position in POSITION_GROUPS:
        if player_1_data.get(position) and player_2_data.get(position):
            common_groups.append(position)

    if not common_groups:
        st.warning('Players have no common position.\nPlease select players who play in similar positions.')
        return
    
    # select which position group to compare
    selected_group = st.segmented_control(
        label='Position Group to compare against',
        options=common_groups,
        selection_mode='single',
        default=common_groups[0],
    )

    if not selected_group:
        selected_group = common_groups[0]
    
    percentile_dfs = player_df.get_percentile_dataframes()
    percentile_df = percentile_dfs[selected_group]

    percentile_metrics = list(set().union(
        PER90_PERCENTILE_STANDARD_STATS,
        PER90_PERCENTILE_SHOOTING_STATS,
        PER90_PERCENTILE_PASSING_STATS,
        PER90_PERCENTILE_DEFENDING_STATS,
        PER90_PERCENTILE_POSSESSION_STATS,
        PER90_PERCENTILE_MISC_STATS,
        PER90_OTHER_STATS,
    ))

    percentile_metrics = sorted(percentile_metrics)  # sorted metrics for easier lookup

    selected_metrics = st.multiselect(
            label='Select metrics to display',
            options=percentile_metrics,
            default=DEFAULT_SELECTED_METRICS
        )
    
    plot_comparison_pizza_chart(player_1_data, player_2_data, percentile_df, selected_metrics)


def plot_comparison_pizza_chart(player_1_data, player_2_data, percentile_df, selected_metrics):
    player_1_percentiles = percentile_df.loc[player_1_data['uid'], selected_metrics].to_numpy()
    player_2_percentiles = percentile_df.loc[player_2_data['uid'], selected_metrics].to_numpy()

    # construct readable selected metrics
    display_selected_metrics = []
    for metric in selected_metrics:
        display_selected_metrics.append(PER90_METRICS_READABLE_NAME_MAPPING[metric][1])

    # instantiate PyPizza class
    baker = PyPizza(
        params=display_selected_metrics,                    # list of parameters
        background_color="#f8f8f8",                         # background color
        straight_line_color="#222222",                      # color for straight lines
        straight_line_lw=1,                                 # linewidth for straight lines
        last_circle_lw=1,                                   # linewidth of last circle
        last_circle_color="#222222",                        # color of last circle
        other_circle_ls="-.",                               # linestyle for other circles
        other_circle_lw=1                                   # linewidth for other circles
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        values=player_1_percentiles,                        # list of values
        compare_values=player_2_percentiles,                # comparison values
        figsize=(8, 8.3),                                   # adjust figsize according to your need
        kwargs_slices=dict(
            facecolor="#1f77b4", edgecolor="#0f4c81",
            zorder=2, linewidth=1
        ),                          # values to be used when plotting slices
        kwargs_compare=dict(
            facecolor="#ff7f0e", edgecolor="#cc6600",
            zorder=2, linewidth=1,
        ),
        kwargs_params=dict(
            color="#000000", fontsize=11,
            fontproperties=font_normal.prop, va="center"
        ),                          # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=11,
            fontproperties=font_normal.prop, zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        ),                          # values to be used when adding parameter-values labels
        kwargs_compare_values=dict(
            color="#000000", fontsize=11, fontproperties=font_normal.prop, zorder=3,
            bbox=dict(edgecolor="#000000", facecolor="#FF9300", boxstyle="round,pad=0.2", lw=1)
        ),                          # values to be used when adding parameter-values labels
    )

    # add title
    fig_text(
        0.505,
        1,
        "<{}> vs <{}>".format(player_1_data.get(PLAYER_NAME), player_2_data.get(PLAYER_NAME)), size=20, fig=fig,
        highlight_textprops=[{"color": '#1f77b4'}, {"color": '#ff7f0e'}],
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