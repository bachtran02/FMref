import streamlit as st

from pages.upload_players import upload_players_page
from pages.input_poss import input_poss_page
from pages.player_pizza import player_pizza_page

from df_processing import *

if __name__ == '__main__':

    pg = st.navigation([
        st.Page(upload_players_page, title='Upload players file'),
        st.Page(input_poss_page, title='Input possession'),
        st.Page(player_pizza_page, title='Pizza chart Visualization')
    ])
    pg.run()