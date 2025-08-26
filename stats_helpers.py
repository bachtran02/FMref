import numpy as np
import pandas as pd

from fm_mapping import *

def find_similar_players(player_data, percentile_dfs, top_n=10):
    target_id = player_data[PLAYER_UID]
    player_positions = [group for group in POSITION_GROUPS if player_data[group]]

    all_distances_dfs = []

    for position in player_positions:
        percentile_df = percentile_dfs[position]
        player_vector = percentile_df.loc[target_id]

        distances = percentile_df.apply(
            lambda row: np.abs(row - player_vector).sum(), axis=1
        )
        distances = distances.drop(target_id)

        if not distances.empty:
            distances_df = distances.to_frame(name='distance')
            distances_df['position'] = position
            all_distances_dfs.append(distances_df)

    if not all_distances_dfs:
        return pd.DataFrame()

    all_distances = pd.concat(all_distances_dfs)

    # For each player, find the position group with the minimum distance
    all_distances = all_distances.sort_values('distance')
    similar_players = all_distances[~all_distances.index.duplicated(keep='first')]
    similar_players = similar_players.head(top_n)

    return similar_players

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
