import streamlit as st

from df_processing import *
from player_df import PlayerDF
from stats_helpers import find_similar_players

STATS_SUMMARY_TABLE = """
| MP     | Min    | Gls    | Ast    | xG     | npxG   |  xA    |
|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| {}     | {}     | {}     | {}     | {}     | {}     | {}     |     
"""

PERCENTILE_TABLE_THEAD = """
    <thead>
        <tr><th colspan="3">{category_name}</th></tr>
        <tr>
            <th>Statistic</th>
            <th>Per 90</th>
            <th>Percentile</th>
        </tr>
    </thead>
"""

SIMILAR_PLAYERS_TABLE_THEAD = """
    <thead>
        <tr>
            <th>Rk</th>
            <th>Player</th>
            <th>Nat</th>
            <th>Squad</th>
        </tr>
    </thead>
"""

def player_statistics_page():
    assert 'player_df' in st.session_state
    player_df: PlayerDF = st.session_state['player_df']

    st.write('## Player Statistics')
    if player_df.is_empty():
        st.warning('Please upload player file first.')
        return

    df = player_df.get_dataframe()
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
    print_player_basic_info(player_data)
    print_player_summary(player_data)
    col1, col2 = st.columns([1, 1])
    print_percentile_table(col1, player_data, perc_df)
    print_similar_players(col2, player_data, data_df, perc_df)

def print_player_basic_info(player_data: dict):
    """
    Print basic player information.
    """
    st.write(f'#### {player_data.get(PLAYER_NAME)}')
    st.write(f'**Position:** {player_data.get(PLAYER_POSITION)} ▪  **Footed**: {player_data.get(PLAYER_PREFERRED_FOOT)}')
    st.write(f'{player_data.get(PLAYER_HEIGHT)}cm, {player_data.get(PLAYER_WEIGHT)}kg')
    st.write(f'**Age**: {player_data.get(PLAYER_AGE)}')
    st.write(f'**Nationality**: {player_data.get(PLAYER_NAT)}')
    st.write(f'**Club**: {player_data.get(PLAYER_CLUB)}')
    st.write(f'**Wages**: £{round(player_data.get(PLAYER_SALARY)):,} Weekly')
    st.write('---')

def print_player_summary(player_data: dict):
    """
    Print player statistics summary.
    """
    st.write('##### Statistics Summary')
    st.write(STATS_SUMMARY_TABLE.format(
        player_data.get(APPS), player_data.get(MINS), player_data.get(GLS), player_data.get(AST),
        player_data.get(XG), player_data.get(NP_XG), player_data.get(XA)))
    st.text("")
    
def print_percentile_table(col, player_data, percentile_dfs):
    """
    Print player percentile table.
    """
    col.write('##### Percentile Statistics')

    playable_position = [group for group in POSITION_GROUPS if player_data.get(group) == 1]

    selected_group = col.segmented_control(
        label='Position Group to compare against',
        options=playable_position,
        selection_mode='single',
        default=playable_position[0],
    )

    if not selected_group:
        selected_group = playable_position[0]
    
    # ensure that selected option is valid position group
    assert selected_group in POSITION_GROUPS
    percentile_df = percentile_dfs[selected_group]

    stats_dict = {
        'Standard': PER90_PERCENTILE_STANDARD_STATS,
        'Shooting': PER90_PERCENTILE_SHOOTING_STATS,
        'Passing': PER90_PERCENTILE_PASSING_STATS,
        'Defending': PER90_PERCENTILE_DEFENDING_STATS,
        'Possession': PER90_PERCENTILE_POSSESSION_STATS,
        'Miscellaneous': PER90_PERCENTILE_MISC_STATS,
    }

    table = '<table>'
    for stat_category in stats_dict:
        stat_tuple = player_stats_to_tuple_data(player_data, stats_dict[stat_category], percentile_df)
        table += PERCENTILE_TABLE_THEAD.format(category_name=stat_category)
        table += '<tbody>'
        for stat, per90, perc in stat_tuple:
            table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
                stat, per90, render_percentile_box(int(perc))
            )
        table += '</tbody>'
    table += '</table>'
    col.html(table)

def print_similar_players(col, player_data, player_df, percentile_dfs):
    # find top 5 most similar players
    similar_players = find_similar_players(player_data, percentile_dfs, 10)
    similar_player_ids = similar_players.index.tolist()

    col.write('##### Similar Players')
    table = '<table>'
    table += SIMILAR_PLAYERS_TABLE_THEAD
    table += '<tbody>'
    for i, similar_player_id in enumerate(similar_player_ids):
        sim_player_dict = player_df.loc[similar_player_id].to_dict()
        table += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
            i + 1,
            sim_player_dict[PLAYER_NAME],
            sim_player_dict[PLAYER_CLUB],
            sim_player_dict[PLAYER_POSITION])
        table += '</tbody>'
    table += '</table>'
    col.html(table)