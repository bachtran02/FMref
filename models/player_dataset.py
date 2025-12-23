import copy
import pandas as pd
import typing as t
from fm_mapping import *
from df_processing import *

class PlayerDataset:

    def __init__(self):
        self._raw_df = None
        self._df = None
        self._percentile_dfs = None
        self._is_empty = True

    def is_empty(self):
        return self._is_empty

    def init_dataset(self, uploaded_file, min_minutes=None) -> None:

        assert uploaded_file.name.endswith('.html'), "Only HTML files are supported for player datasets."

        dfs = pd.read_html(uploaded_file, encoding='utf8')
        assert len(dfs) > 0, "No tables found in the uploaded HTML file."

        df = dfs[0]
        self._raw = df
        self._df = df.copy()
        self._is_empty = False
        
        # preprocess dataframe
        self._df = preprocess_df(self._df)

        if min_minutes is not None:
            self._df = self._df[self._df[MINS].astype(int) >= min_minutes]
        
        self._df = parse_player_position(self._df)

        # TODO: handle goalkeepers, for now filter out
        self._df = self._df[~(self._df[GOALKEEPER] == 1)]

        self._df = add_custom_metrics(self._df)
        self._df = normalize_metrics(self._df)

        # calculate & store percentiles for each position group
        self._percentile_dfs = get_percentile_df_by_groups(self._df.copy())

    def get_dataframe(self) -> t.Optional[pd.DataFrame]:
        if not self.is_empty() and self._df is not None:
            return self._df.copy()
        return None

    def get_percentile_dataframes(self) -> t.Optional[dict[str, pd.DataFrame]]:
        if not self.is_empty() and self._percentile_dfs is not None:
            return copy.deepcopy(self._percentile_dfs)
        return None

    def get_raw_dataframe(self) -> t.Optional[pd.DataFrame]:
        if not self.is_empty() and self._raw is not None:
            return self._raw.copy()
        return None

    def get_shape(self) -> tuple[int, int]:
        if not self.is_empty() and self._df is not None:
            return self._df.shape
        return 0, 0

    def get_player_row_by_id(self, player_uid: int) -> t.Optional[dict]:
        if not self.is_empty() and self._df is not None:
            if player_uid not in self._df.index:
                return None
            row_dict = self._df.loc[player_uid].to_dict()
            # assign back player uid to dict
            row_dict[PLAYER_UID] = player_uid
            return row_dict
        return None
