import streamlit as st

from fm_mapping import *
from player_df import PlayerDF

def player_search_by_percentile_page():
    assert 'player_df' in st.session_state
    player_df: PlayerDF = st.session_state['player_df']

    st.write('## Search Player by Percentile')
    if player_df.is_empty():
        st.warning('Please upload player file first.')
        return
    
    df = player_df.get_dataframe()
    percentile_dfs = player_df.get_percentile_dataframes()

    # segment control
    selected_position = st.segmented_control(
        label='Search for Player in Postion',
        options=POSITION_GROUPS,
        selection_mode='single',
        default=POSITION_GROUPS[0],
    ) or POSITION_GROUPS[0]

    stats_groups = (
        PER90_PERCENTILE_SHOOTING_STATS,
        PER90_PERCENTILE_PASSING_STATS,
        PER90_PERCENTILE_DEFENDING_STATS,
        PER90_PERCENTILE_POSSESSION_STATS,
        PER90_PERCENTILE_MISC_STATS,
    )

    percentile_df = percentile_dfs[selected_position]

    cols = st.columns(5)
    for i, col in enumerate(cols):
        stats_group = stats_groups[i]
        for stat in stats_group:
            perc = col.slider(stat, 1, 99, 1)
            percentile_df = percentile_df[percentile_df[stat] >= perc]

    found_player_ids = percentile_df.index.tolist()
    if len(found_player_ids) > 20:
        st.warning('More than 20 search result, truncating to 20 results...')

    found_player_table = ''
    found_player_table += ('|   Rk   | Player | Nation | Squad  | Minutes|\n')
    found_player_table += ('|:------:|:------:|:------:|:------:|:------:|\n')
    for i, found_player_id in enumerate(found_player_ids):
        if i >= 20:
            break

        found_player_dict = df.loc[found_player_id].to_dict()
        found_player_table += '|{}|{}|{}|{}|{}|\n'.format(
            i + 1,
            found_player_dict[PLAYER_NAME],
            found_player_dict[PLAYER_NAT],
            found_player_dict[PLAYER_CLUB],
            found_player_dict[MINS])
        
    st.write('##### Search Results')
    st.write(found_player_table)
