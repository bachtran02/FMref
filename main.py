import streamlit as st

from pages.upload_players import upload_players_page
from pages.input_poss import input_poss_page
from pages.player_pizza import pizza_stats_page, pizza_comparison_page

from df_processing import *

if __name__ == '__main__':

    pages = {
        '': [
            st.Page(upload_players_page, title='Upload players file'),
            st.Page(input_poss_page, title='Input possession'),
        ], 
        'Pizza Chart Visualizations': [
            st.Page(pizza_stats_page, title='Player Stats'),
            st.Page(pizza_comparison_page, title='Player Comparison')
        ]
    }

    pg = st.navigation(pages)
    pg.run()