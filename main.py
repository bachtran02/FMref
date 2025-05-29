import streamlit as st

from player_df import PlayerDF

from pages.player_compare import player_compare_page
from pages.player_stats import player_statistics_page
from pages.upload_players import player_upload_page

from df_processing import *

if __name__ == '__main__':

    # initialize player dataframe if not exists
    if 'player_df' not in st.session_state:
        st.session_state['player_df'] = PlayerDF()

    pages = {
        '': [
            st.Page(player_upload_page, title='Player Dataframe', icon='⚽'),
            st.Page(player_statistics_page, title='Player Statistics', icon='⚽'),
            st.Page(player_compare_page, title='Player Comparison', icon='⚽')
        ], 
    }
    pg = st.navigation(pages)
    pg.run()