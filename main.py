import streamlit as st

from player_df import PlayerDF

from pages.upload_players import *
# from pages.input_poss import input_poss_page
from pages.player_stats import *

from df_processing import *

if __name__ == '__main__':

    # initialize player dataframe if not exists
    if 'player_df' not in st.session_state:
        st.session_state['player_df'] = PlayerDF()

    pages = {
        '': [
            st.Page(player_dataframe_page, title='Player Dataframe', icon='⚽'),
            st.Page(player_statistics_page, title='Player Statistics', icon='⚽'),
        ], 
    }
    pg = st.navigation(pages)
    pg.run()