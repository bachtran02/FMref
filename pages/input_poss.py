import streamlit as st
import pandas as pd
import numpy as np

from df_processing import *

# maybe break leagues into seperate tables for ease of input

def input_poss_table() -> pd.DataFrame:
    
    assert 'players_df' in st.session_state
    players_df : pd.DataFrame = st.session_state['players_df']
    teams_df = (
        players_df[['club', 'division']]
        .drop_duplicates()
        .sort_values(['division', 'club'])
        .reset_index(drop=True)
    )    
    teams_df['poss'] = 50

    
    st.write('##### Input possession table')

    edited_teams_df = st.data_editor(
        teams_df,
        column_config={
            'club': 'Club',
            'division': 'League',
            'poss': st.column_config.NumberColumn(
                'Team Possession',
                help='Enter team average possession from 0-100',
                min_value=0,
                max_value=100,
                step=1
            )
        },
        disabled=['division', 'club'],
        hide_index=True,
    )

    return edited_teams_df

def upload_poss_file() -> pd.DataFrame:

    assert 'players_df' in st.session_state
    players_df : pd.DataFrame = st.session_state['players_df']
    existing_club_set = set(players_df['club'])

    st.write('##### Upload file')

    uploaded_file = st.file_uploader(
        label='Upload saved possession `.csv` file',
        type='csv',
    )

    # wait for file to be uploaded
    if not uploaded_file:
        return

    assert uploaded_file.name.endswith('.csv') # check file extension

    df = pd.read_csv(uploaded_file)
    uploaded_club_set = set(df['club'])

    # check if all columns exist
    columns_exist = all(col in df.columns for col in ('club', 'division', 'poss'))
    # check if all possession values are within  [0, 100]
    poss_within_range = 'poss' in df.columns and df['poss'].between(0, 100).all()
    # check if all clubs in players dataframe exist in uploaded dataframe
    all_exist = existing_club_set.issubset(uploaded_club_set)

    if not (columns_exist and poss_within_range and all_exist):
        print('All columns exist:', columns_exist)
        print('All clubs exist:', all_exist)
        print('Possession value within range:', poss_within_range)

    return df

def input_poss_page():

    st.write('## Input Possesssion')

    if 'players_df' not in st.session_state:
        st.warning("Please upload players file first!")
        return
    
    st.write('Update `Team Possession` column of table or upload prefilled possession `.csv`')
    
    uploaded_teams_df = upload_poss_file()
    filled_teams_df = input_poss_table()

    if isinstance(uploaded_teams_df, pd.DataFrame):
        final_teams_df = uploaded_teams_df
    else:
        final_teams_df = filled_teams_df

    st.write('##### Final possession table')
    st.write(final_teams_df)

    # merge team possession to players dataframe
    players_df = st.session_state['players_df']
    players_df = merge_possession_to_df(players_df, final_teams_df)
    players_df = add_poss_adjusted_metrics(players_df)

    st.write(players_df)

    # update players df
    st.session_state['players_df'] = players_df
    