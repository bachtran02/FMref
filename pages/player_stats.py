import streamlit as st

from df_processing import *
from player_df import PlayerDF
from stats_helpers import find_similar_players, player_stats_to_tuple_data
from html_templates import (
    render_summary_table, render_percentile_bar, percentile_table_thead,
    similar_table_thead
)

def player_statistics_page():

    assert 'player_df' in st.session_state
    player_df: PlayerDF = st.session_state['player_df']

    st.write('## Player Statistics')
    if player_df.is_empty():
        st.warning('Please upload player file first.')
        return

    df = player_df.get_dataframe()
    if df is None:
        st.warning('Player dataframe is empty or not loaded correctly.')
        return
    
    player_id_name_map = df[PLAYER_NAME].to_dict()
    
    selected_player_id = st.selectbox(
        label='Select Player',
        options = player_id_name_map.keys(),
        format_func=lambda x: player_id_name_map[x],
        help='Select a player to view their statistics'
    )

    data_df = player_df.get_dataframe()
    perc_df = player_df.get_percentile_dataframes()

    player_data = player_df.get_player_row_by_id(selected_player_id)
    if player_data is None:
        st.warning('Error retrieving player data. Please try again.')
        return
    
    print_player_basic_info(player_data)
    print_player_summary(player_data)
    
    # percentile and similar table on same row
    col1, col2 = st.columns([3, 2])
    print_percentile_table(col1, player_data, perc_df)
    print_similar_players(col2, player_data, data_df, perc_df)

def print_player_basic_info(player_data: dict):
    """
    Print basic player information.
    """
    st.write(f'#### {player_data.get(PLAYER_NAME)}')
    st.write(f'**Position:** {player_data.get(PLAYER_POSITION)} ▪  **Footed**: {player_data.get(PLAYER_PREFERRED_FOOT)}')
    st.write(f'**Age**: {player_data.get(PLAYER_AGE)} ▪ **Height:** {player_data.get(PLAYER_HEIGHT)}cm ▪ **Weight:** {player_data.get(PLAYER_WEIGHT)}kg')
    st.write(f'**Club**: {player_data.get(PLAYER_CLUB)} ▪ **Nationality**: {player_data.get(PLAYER_NAT)}')
    st.write(f'**Wages**: £{round(player_data[PLAYER_SALARY]):,} Weekly')
    st.write('---')

def print_player_summary(player_data: dict):
    """
    Print player statistics summary.
    """
    st.write('##### Statistics Summary')
    summary_table_html = '<table class="summary-table">'
    summary_table_html += render_summary_table(
        mp=player_data.get(APPS),
        min=player_data.get(MINS),
        gls=player_data.get(GLS),
        ast=player_data.get(AST),
        xg=player_data.get(XG),
        npxg=player_data.get(NP_XG),
        xa=player_data.get(XA)
    )
    summary_table_html += '</table>'
    st.html(summary_table_html)
    
def generate_percentile_table_html(player_data, percentile_df):

    table = '''
        <table class="percentile-table">
        <colgroup>
            <col style="width: 150px;">
            <col style="width: 40px;">
            <col style="width: 200px;">
        </colgroup>
    '''

    stats_dict = {
        'Standard': PER90_PERCENTILE_STANDARD_STATS,
        'Shooting': PER90_PERCENTILE_SHOOTING_STATS,
        'Passing': PER90_PERCENTILE_PASSING_STATS,
        'Defending': PER90_PERCENTILE_DEFENDING_STATS,
        'Possession': PER90_PERCENTILE_POSSESSION_STATS,
        'Miscellaneous': PER90_PERCENTILE_MISC_STATS,
    }

    for stat_category in stats_dict:
        stat_tuple = player_stats_to_tuple_data(player_data, stats_dict[stat_category], percentile_df)
        table += percentile_table_thead(stat_category)
        table += '<tbody>'
        for stat, per90, perc in stat_tuple:
            table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
                stat, per90, render_percentile_bar(int(perc)))
        table += '</tbody>'
    table += '</table>'
    return table

def generate_similar_players_table_html(similar_players, player_df):
    table = '<table class="similar-table">'
    table += '''
        <colgroup>
            <col style="width: 20px;">
            <col style="width: 130px;">
            <col style="width: 100px;">
            <col style="width: 100px;">
        </colgroup>
    '''
    table += similar_table_thead()
    table += '<tbody>'
    for i, (similar_player_id, row) in enumerate(similar_players.iterrows()):
        sim_player_dict = player_df.loc[similar_player_id].to_dict()
        position_group = row['position']
        table += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
            i + 1,
            sim_player_dict[PLAYER_NAME],
            sim_player_dict[PLAYER_CLUB],
            position_group)
        table += '</tbody>'
    table += '</table>'
    return table

def print_percentile_table(col, player_data, percentile_dfs):
    """
    Print player percentile table.
    """
    col.write('##### Percentile Statistics')

    # get player's playable positions
    playable_position = [group for group in POSITION_GROUPS if player_data.get(group) == 1]

    selected_group = col.segmented_control(
        label='Position Group to compare against',
        options=playable_position,
        selection_mode='single',
        default=playable_position[0],
    )

    # select the first one by default
    if not selected_group:
        selected_group = playable_position[0]
    
    # ensure that selected option is valid position group
    assert selected_group in POSITION_GROUPS
    percentile_df = percentile_dfs[selected_group]

    table_html = generate_percentile_table_html(player_data, percentile_df)
    col.html(table_html)

def print_similar_players(col, player_data, player_df, percentile_dfs):
    # find top 5 most similar players
    similar_players = find_similar_players(player_data, percentile_dfs, 10)

    col.write('##### Similar Players')
    table_html = generate_similar_players_table_html(similar_players, player_df)
    col.html(table_html)