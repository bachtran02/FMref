import streamlit as st

from models.player_dataset import PlayerDataset

from load_pages import pages
from utils import load_css

if __name__ == '__main__':

    # initialize player dataframe if not exists
    # if 'player_dataset' not in st.session_state:
    #     st.session_state['player_dataset'] = PlayerDataset()

    # render CSS
    st.html(load_css('./assets/style.css'))

    pg = st.navigation(pages)
    pg.run()