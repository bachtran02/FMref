import streamlit as st
import pandas as pd
import numpy as np

from player_df import PlayerDF

def player_upload_page():
    
    assert 'player_df' in st.session_state
    player_df: PlayerDF = st.session_state['player_df']

    st.write('## Player Upload')
    st.write("#### Upload player file")

    _player_file = st.file_uploader(
        label='Upload players `.html` file', type='html',
        help='Export file in Football Manager > Scouting > Players > Players in Range'
    )

    # if there is no file uploaded yet
    if _player_file is None and 'player_file' not in st.session_state:
        return

    if _player_file:
        player_df.init_df(_player_file)
        st.session_state['player_file'] = _player_file

    df_shape = player_df.get_shape()
    
    st.write("#### Player Dataframes")
    st.write('Number of players:', df_shape[0])
    st.write('Number of columns:', df_shape[1])
    st.write('##### Raw Dataframe')
    st.write(player_df.get_raw_dataframe())
    st.write('##### Processed Dataframe')
    st.write(player_df.get_dataframe())