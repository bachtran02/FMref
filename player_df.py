import pandas as pd
import streamlit as st
from fm_mapping import *

from df_processing import preprocess_df, normalize_metrics, add_custom_metrics

class PlayerDF:

    MIN_MINUTES = 450

    def __init__(self):
        self._raw_df = None
        self._df = None
        self._is_empty = True

    def is_empty(self):
        return self._is_empty

    def init_df(self, uploaded_file) -> None:
        try:
            assert uploaded_file.name.endswith('.html')

            dfs = pd.read_html(uploaded_file, encoding='utf8')
            df = dfs[0]

            print('Number of players:', df.shape[0])
            print('Number of columns:', df.shape[1])

        except:
            # TODO: handle error here
            raise NotImplementedError
        
        self._raw = df
        self._df = df.copy()
        self._is_empty = False
        
        # preprocess dataframe
        self._df = preprocess_df(self._df)
        self._df = self._df[self._df[MINS] >= self.MIN_MINUTES]   # filter out players who play fewer than MIN_MINUTES
        self._df = add_custom_metrics(self._df)
        self._df = normalize_metrics(self._df)

    def add_team_poss(self, poss_df: pd.DataFrame):
        pass

    def get_dataframe(self):
        return self._df.copy()

    def get_shape(self):
        return self._df.shape
    
    def get_player_by_name(self, player_name: str):
        matched_rows = self._df[self._df[PLAYER_NAME] == player_name]
        return matched_rows.iloc[0].to_dict() if not matched_rows.empty else {}