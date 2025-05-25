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

def print_player_basic_info(player_name: str, player_stats: dict):
    """
    Print basic player information.
    """
    st.write(f'#### {player_name}')
    st.write(f'**Position:** {player_stats[PLAYER_POSITION]} ▪  **Footed**: {player_stats[PLAYER_PREFERRED_FOOT]}')
    st.write(f'{player_stats[PLAYER_HEIGHT]}cm, {player_stats[PLAYER_WEIGHT]}kg')
    st.write(f'**Age**: {player_stats[PLAYER_AGE]}')
    st.write(f'**Nationality**: {player_stats[PLAYER_NAT]}')
    st.write(f'**Club**: {player_stats[PLAYER_CLUB]}')
    st.write(f'**Wages**: £{round(player_stats[PLAYER_SALARY]):,} Weekly')
    st.write('---')

def print_player_summary(player_stats: dict):
    """
    Print player statistics summary.
    """
    st.write('##### Statistics Summary')
    st.write(STATS_SUMMARY_TABLE.format(
        20, player_stats[MINS], player_stats[GLS], player_stats[AST],
        player_stats[XG], player_stats[NP_XG], player_stats[XA]))
    
def print_percentile_table(player_stats, df):
    """
    Print player percentile table.
    """
    st.write('##### Percentile Statistics')

    standard_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_STANDARD_STATS, df)
    shooting_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_SHOOTING_STATS, df)
    passing_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_PASSING_STATS, df)
    defending_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_DEFENDING_STATS, df)
    possession_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_POSSESSION_STATS, df)
    misc_stats_tuple = player_stats_to_tuple_data(player_stats, PER90_PERCENTILE_MISC_STATS, df)

    table = ''
    table += '<table>'
    table += PERCENTILE_TABLE_THEAD.format(category_name='Standard Stats')
    table += '<tbody>'
    for stat, per90, perc in standard_stats_tuple:
        table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
            stat, per90, render_percentile_box(int(perc))
        )
    table += '</tbody>'
    table += PERCENTILE_TABLE_THEAD.format(category_name='Shooting Stats')
    table += '<tbody>'
    for stat, per90, perc in shooting_stats_tuple:
        table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
            stat, per90, render_percentile_box(int(perc))
        )
    table += '</tbody>'
    table += PERCENTILE_TABLE_THEAD.format(category_name='Passing Stats')
    table += '<tbody>'
    for stat, per90, perc in passing_stats_tuple:
        table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
            stat, per90, render_percentile_box(int(perc))
        )
    table += '</tbody>'
    table += PERCENTILE_TABLE_THEAD.format(category_name='Defending Stats')
    table += '<tbody>'
    for stat, per90, perc in defending_stats_tuple:
        table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
            stat, per90, render_percentile_box(int(perc))
    )
    table += '</tbody>'
    table += PERCENTILE_TABLE_THEAD.format(category_name='Possession Stats')
    table += '<tbody>'
    for stat, per90, perc in possession_stats_tuple:
        table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
            stat, per90, render_percentile_box(int(perc))
    )
    table += '</tbody>'
    table += PERCENTILE_TABLE_THEAD.format(category_name='Miscellaneous Stats')
    table += '<tbody>'
    for stat, per90, perc in misc_stats_tuple:
        table += '<tr><td>{}</td><td>{:.2f}</td><td>{}</td></tr>'.format(
            stat, per90, render_percentile_box(int(perc))
    )
    table += '</tbody>'
    table += '</table>'
    st.html(stats_table_css)
    st.html(table)
