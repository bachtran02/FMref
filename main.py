import streamlit as st

from player_df import PlayerDF

from pages.upload_players import player_dataframe_page
from pages.input_poss import input_poss_page
from pages.player_pizza import pizza_stats_page, pizza_comparison_page

from df_processing import *

if __name__ == '__main__':

    # initialize player dataframe if not exists
    if 'player_df' not in st.session_state:
        st.session_state['player_df'] = PlayerDF()

    pages = {
        '': [
            st.Page(player_dataframe_page, title='Player Dataframe'),
            st.Page(input_poss_page, title='Input possession'),
        ], 
        # 'Pizza Chart Visualizations': [
        #     st.Page(pizza_stats_page, title='Player Stats'),
        #     st.Page(pizza_comparison_page, title='Player Comparison')
        # ]
    }
    pg = st.navigation(pages)
    pg.run()