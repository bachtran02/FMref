import copy
import pandas as pd
from fm_mapping import *
from df_processing import *

class PlayerDF:

    MIN_MINUTES = 450

    def __init__(self):
        self._raw_df = None
        self._df = None
        self._percentile_dfs = None
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
        self._df = parse_player_position(self._df)
        self._df = add_custom_metrics(self._df)
        self._df = normalize_metrics(self._df)

        # calculate & store percentiles for each position group
        self._percentile_dfs = get_percentile_df_by_groups(self._df.copy())

    def get_dataframe(self):
        return self._df.copy()
    
    def get_percentile_dataframes(self):
        return copy.deepcopy(self._percentile_dfs)

    def get_shape(self):
        return self._df.shape
    
    def get_player_row_by_id(self, player_uid: int) -> dict:
        if player_uid not in self._df.index:
            return None
        row_dict = self._df.loc[player_uid].to_dict()
        row_dict['uid'] = player_uid
        return row_dict
