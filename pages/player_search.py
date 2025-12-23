import streamlit as st

from models.player_dataset import PlayerDF
from fm_mapping import (
    MINS, PLAYER_AGE, PLAYER_CLUB, PLAYER_NAME, PLAYER_NAT, PLAYER_POSITION
)
from config import PER90_PERCENTILE_STATS_GROUPS

def player_search_by_percentile_page():
    assert 'player_df' in st.session_state
    player_df: PlayerDF = st.session_state['player_df']

    st.write('## Search Player by Percentile')
    if player_df.is_empty():
        st.warning('Please upload player file first.')
        return
    
    df = player_df.get_dataframe()
    percentile_dfs = player_df.get_percentile_dataframes()
    assert (df is not None) and (percentile_dfs is not None)
    available_groups = list(percentile_dfs.keys())

    # segment control
    selected_position = st.segmented_control(
        label='Search for Player in Postion',
        options=available_groups,
        selection_mode='single',
        default=available_groups[0],
    ) or available_groups[0]

    slider_added = set()    # easy way to ensure no duplicate
    filtered_percentile_df = percentile_dfs[selected_position]

    cols = st.columns(len(PER90_PERCENTILE_STATS_GROUPS))
    for i, col in enumerate(cols):
        stats_group = PER90_PERCENTILE_STATS_GROUPS[i]
        for stat in stats_group:
            if stat in slider_added:
                continue
            slider_added.add(stat)
            perc = col.slider(stat, 1, 99, 1)
            filtered_percentile_df = filtered_percentile_df[filtered_percentile_df[stat] >= perc]

    found_player_ids = filtered_percentile_df.index.tolist()
    if len(found_player_ids) > 50:
        st.warning('More than 50 search result, truncating to 50 results...')

    st.write('##### Search Results')
    if found_player_ids:
        found_player_display_df = df.loc[found_player_ids, [
            PLAYER_NAME, PLAYER_AGE, PLAYER_NAT, PLAYER_CLUB, PLAYER_POSITION, MINS]]
        found_player_display_df = found_player_display_df.sort_values(by=MINS, ascending=False)
        found_player_display_df = found_player_display_df.reset_index(drop=True)
        st.write(f'Number of players found: `{len(found_player_ids)}`')
        st.write(found_player_display_df.head(50))  # display top 50 results
    else:
        st.info("No players found with the selected criteria.")

