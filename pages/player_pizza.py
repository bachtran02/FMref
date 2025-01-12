import streamlit as st
import pandas as pd
import numpy as np

from df_processing import *

def player_pizza_page():
    
    st.write('## Player Pizza chart')

    if 'players_df' not in st.session_state:
        st.warning("Please upload players file first!")
        return
    
    players_df = st.session_state['players_df']
    teams_df = st.session_state['teams_df']

    players_df = merge_possession_to_df(players_df, teams_df)
    players_df = normalize_metrics(players_df)
    players_df = add_custom_metrics(players_df)

    # only include players with more than 900 minutes played ~ 10 matches
    filtered_df = players_df[players_df['mins'] >= 900]
    st.write(filtered_df)
