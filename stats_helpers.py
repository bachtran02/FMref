import numpy as np
import pandas as pd

from fm_mapping import *

def find_similar_player_ids(player_data, percentile_dfs, position_group, top_n=10):
    target_id = player_data[PLAYER_UID]
    percentile_df = percentile_dfs[position_group]
    player_vector = percentile_df.loc[target_id]

    distances = percentile_df.drop(target_id).apply(
        lambda row: np.abs(row - player_vector).sum(), axis=1).sort_values()
    
    return distances.head(top_n).index.tolist()

def player_stats_to_tuple_data(player_data: dict, stats_to_include: dict, percentile_df: pd.DataFrame):
    """
    Convert player stats to a tuple of tuples for FBref-like HTML table rendering.
    """

    percentiles = percentile_df.loc[player_data[PLAYER_UID]].to_dict()

    res = []
    for key in stats_to_include:
        percentile = 0
        stat = player_data.get(key, 0)
        percentile = percentiles[key]

        field_tuple = (PER90_METRICS_READABLE_NAME_MAPPING[key][0], round(stat, 2), percentile)
        res.append(field_tuple)
    return res
