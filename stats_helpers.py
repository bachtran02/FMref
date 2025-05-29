import numpy as np
import pandas as pd

from fm_mapping import *

def find_similar_players(player_data, percentile_dfs, top_n = 5):

    target_id = player_data[PLAYER_UID]
    player_positions = [group for group in POSITION_GROUPS if player_data[group]]

    all_distances = pd.Series(dtype=float)

    for position in player_positions:
        percentile_df = percentile_dfs[position]
        player_vector = percentile_df.loc[target_id]

        distances = percentile_df.apply(lambda row: np.abs(row - player_vector).sum(), axis=1)
        distances = distances.drop(target_id)

        if not distances.empty:
            all_distances = pd.concat([all_distances, distances])

    all_distances = all_distances.groupby(all_distances.index).min()
    similar_players_id = all_distances.nsmallest(top_n)

    return similar_players_id
