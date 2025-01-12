import streamlit as st
import pandas as pd
import numpy as np

from df_processing import *

def upload_file() -> pd.DataFrame:

    uploaded_file = st.file_uploader(
        label='Upload players `.html` file',
        type='html',
        help='Export file in Football Manager > Scouting > Players > Players in Range'
    )

    # wait for file to be uploaded
    if not uploaded_file:
        return

    assert uploaded_file.name.endswith('.html') # check file extension

    # TODO: better error handling here
    dfs = pd.read_html(uploaded_file, encoding='utf8')
    assert len(dfs) > 0
    df = dfs[0]

    # output dataframe's dimension & first few rows
    st.write('Number of players:', df.shape[0])
    st.write('Number of fields:', df.shape[1])
    st.write('First few rows from raw dataframe')
    st.write(df)

    return df

def upload_players_page():

    st.write('## Upload players file')
    
    raw_df = upload_file()
    
    if raw_df is None:
        return

    df = raw_df.copy()
    df = preprocess_df(df)

    st.write('Dataframe after preprocessing:')
    st.write(df)

    # Store the processed data in session_state
    st.session_state["players_df"] = df
    st.success("File uploaded and processed successfully!")