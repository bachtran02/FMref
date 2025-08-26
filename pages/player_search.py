import streamlit as st

from player_df import PlayerDF
from fm_mapping import MINS, PLAYER_CLUB, PLAYER_NAME, PLAYER_NAT
from config import (
    PER90_PERCENTILE_DEFENDING_STATS, PER90_PERCENTILE_MISC_STATS,
    PER90_PERCENTILE_PASSING_STATS, PER90_PERCENTILE_POSSESSION_STATS,
    PER90_PERCENTILE_SHOOTING_STATS
)
from html_templates import search_results_table_thead

def player_search_by_percentile_page():
    assert 'player_df' in st.session_state
    player_df: PlayerDF = st.session_state['player_df']

    st.write('## Search Player by Percentile')
    if player_df.is_empty():
        st.warning('Please upload player file first.')
        return
    
    df = player_df.get_dataframe()
    percentile_dfs = player_df.get_percentile_dataframes()
    assert percentile_dfs is not None
    available_groups = list(percentile_dfs.keys())

    # segment control
    selected_position = st.segmented_control(
        label='Search for Player in Postion',
        options=available_groups,
        selection_mode='single',
        default=available_groups[0],
    ) or available_groups[0]

    stats_groups = (
        PER90_PERCENTILE_SHOOTING_STATS,
        PER90_PERCENTILE_PASSING_STATS,
        PER90_PERCENTILE_DEFENDING_STATS,
        PER90_PERCENTILE_POSSESSION_STATS,
        PER90_PERCENTILE_MISC_STATS,
    )

    slider_added = set()    # easy way to ensure no duplicate
    percentile_df = percentile_dfs[selected_position]

    cols = st.columns(5)
    for i, col in enumerate(cols):
        stats_group = stats_groups[i]
        for stat in stats_group:
            if stat in slider_added:
                continue
            slider_added.add(stat)
            perc = col.slider(stat, 1, 99, 1)
            percentile_df = percentile_df[percentile_df[stat] >= perc]

    found_player_ids = percentile_df.index.tolist()
    if len(found_player_ids) > 20:
        st.warning('More than 20 search result, truncating to 20 results...')

    st.write('##### Search Results')
    if found_player_ids:
        table_html = generate_search_results_table_html(found_player_ids, df)
        st.html(table_html)
    else:
        st.info("No players found with the selected criteria.")

def generate_search_results_table_html(found_players, player_df):
    table = '<table class="search-results-table">'
    table += '''
        <colgroup>
            <col style="width: 40px;">
            <col style="width: 150px;">
            <col style="width: 100px;">
            <col style="width: 180px;">
            <col style="width: 80px;">
        </colgroup>
    '''
    table += search_results_table_thead()
    table += '<tbody>'
    for i, player_id in enumerate(found_players):
        if i >= 20:
            break
        player_dict = player_df.loc[player_id].to_dict()
        table += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
            i + 1,
            player_dict[PLAYER_NAME],
            player_dict[PLAYER_NAT],
            player_dict[PLAYER_CLUB],
            player_dict[MINS])
    table += '</tbody></table>'
    return table
