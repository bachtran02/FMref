import streamlit as st
import pandas as pd
import numpy as np

from player_df import PlayerDF

def player_dataframe_page():
    
    assert 'player_df' in st.session_state
    player_df: PlayerDF = st.session_state['player_df']
    team_df: PlayerDF = st.session_state['team_df']

    st.write('## Player Dataframe')

    if 'player_file' not in st.session_state or player_df.is_empty():

        st.write("#### Upload player file")

        player_file = st.file_uploader(
            label='Upload players `.html` file', type='html',
            help='Export file in Football Manager > Scouting > Players > Players in Range'
        )
        if player_file is None:
            return

        st.session_state['player_file'] = player_file
        player_df.init_df(player_file)

        st.success("File uploaded and processed successfully!")

    if 'team_file' not in st.session_state or team_df.is_empty():

        st.write("#### Upload team file")

        team_file = st.file_uploader(
            label='Upload team `.html` file', type='html',
            help='Export file in Football Manager > Squad'
        )
        if team_file is None:
            return

        st.session_state['team_file'] = team_file
        team_df.init_df(team_file)

        st.success("File uploaded and processed successfully!")
        
    df_shape = player_df.get_shape()
    
    st.write("#### Player Dataframe")
    st.write('Number of players:', df_shape[0])
    st.write('Number of columns:', df_shape[1])
    st.write(player_df.get_dataframe())