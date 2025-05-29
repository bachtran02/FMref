import streamlit as st
from fm_mapping import *
from utils import *

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
    
def print_percentile_table(player_stats, percentile_dfs):
    """
    Print player percentile table.
    """
    st.write('##### Percentile Statistics')

    position_groups = (
        'Centerback',
        'Fullback',
        'Midfielder',
        'Att-Mid/Winger',
        'Forward',
    )

    playable_position = [group for group in position_groups if player_stats.get(group) == 1]

    selected_group = st.segmented_control(
        label='Position Group to compare against',
        options=playable_position,
        selection_mode='single',
        default=playable_position[0],
    )

    if not selected_group:
        # TODO: warning
        return
    
    # ensure that selected option is valid position group
    assert selected_group in position_groups
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

        stat_tuple = player_stats_to_tuple_data(player_stats, stats_dict[stat_category], percentile_df)
        table += PERCENTILE_TABLE_THEAD.format(category_name=stat_category)
        table += '<tbody>'
        for stat, per90, perc in stat_tuple:
            table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
                stat, per90, render_percentile_box(int(perc))
            )
        table += '</tbody>'
    table += '</table>'
    st.html(stats_table_css)
    st.html(table)

    

    # standard_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_STANDARD_STATS, df)
    # shooting_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_SHOOTING_STATS, df)
    # passing_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_PASSING_STATS, df)
    # defending_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_DEFENDING_STATS, df)
    # possession_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_POSSESSION_STATS, df)
    # misc_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_MISC_STATS, df)

    # table = ''
    # table += '<table>'
    # table += PERCENTILE_TABLE_THEAD.format(category_name='Standard Stats')
    # table += '<tbody>'
    # for stat, per90, perc in standard_stats_tuple:
    #     table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
    #         stat, per90, render_percentile_box(int(perc))
    #     )
    # table += '</tbody>'
    # table += PERCENTILE_TABLE_THEAD.format(category_name='Shooting Stats')
    # table += '<tbody>'
    # for stat, per90, perc in shooting_stats_tuple:
    #     table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
    #         stat, per90, render_percentile_box(int(perc))
    #     )
    # table += '</tbody>'
    # table += PERCENTILE_TABLE_THEAD.format(category_name='Passing Stats')
    # table += '<tbody>'
    # for stat, per90, perc in passing_stats_tuple:
    #     table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
    #         stat, per90, render_percentile_box(int(perc))
    #     )
    # table += '</tbody>'
    # table += PERCENTILE_TABLE_THEAD.format(category_name='Defending Stats')
    # table += '<tbody>'
    # for stat, per90, perc in defending_stats_tuple:
    #     table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
    #         stat, per90, render_percentile_box(int(perc))
    # )
    # table += '</tbody>'
    # table += PERCENTILE_TABLE_THEAD.format(category_name='Possession Stats')
    # table += '<tbody>'
    # for stat, per90, perc in possession_stats_tuple:
    #     table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
    #         stat, per90, render_percentile_box(int(perc))
    # )
    # table += '</tbody>'
    # table += PERCENTILE_TABLE_THEAD.format(category_name='Miscellaneous Stats')
    # table += '<tbody>'
    # for stat, per90, perc in misc_stats_tuple:
    #     table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
    #         stat, per90, render_percentile_box(int(perc))
    # )
    # table += '</tbody>'
    # table += '</table>'
    # st.html(stats_table_css)
    # st.html(table)
