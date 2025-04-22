import pandas as pd
import numpy as np

from fm_mapping import *
from utils import *

def verify_dataframe_columns():
    pass

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:

    df = df.drop(columns=['Rec', 'Inf'], errors='ignore')                             # not useful for analysis
    df = df.dropna(subset=[PLAYER_UID])                              # drop rows with no player UID
    df = df.drop(columns=[DIST_90])                                  # not exported correctly by FM24 (all zeros)

    # weird bug when "Tck W" is sometimes saved as "Tck C"
    if 'Tck C' in df.columns:
        df.rename(columns={'Tck C': 'Tck W'}, inplace=True)         

    # TODO: improve this
    # sanity check to ensure all the necessary fields are included
    # required_fields = list(nonnumeric_fields_to_cc.keys()) + list(numeric_fields_to_cc.keys())
    # missing_fields = [f for f in required_fields if f not in df.columns]

    # if missing_fields:
    #     print(f"Missing fields: {missing_fields}")
    # else:
    #     print("DataFrame contains all required fields.")

    # use UID as index
    df[PLAYER_UID] = df[PLAYER_UID].astype(str).str.replace(',', '')
    df = df.set_index(PLAYER_UID)
    
    # TODO: improve this
    # Replace missing stats with 0s
    # Note: in Football Manager - ~ 0
    df = df.replace('-', 0)

    # assert correct metric units (kg, cm, £, mi)
    _first_entry = df.iloc[0]
    assert _first_entry[PLAYER_WEIGHT].split()[1] == 'kg'
    assert _first_entry[PLAYER_HEIGHT].split()[1] == 'cm'
    assert _first_entry[PLAYER_SALARY][0] == '£'
    # assert _first_entry[DIST][-2:] == 'mi'

    # transform weight, height columns
    df[PLAYER_WEIGHT] = df[PLAYER_WEIGHT].str.split().str[0]  # only keep numeric value, should be in cm
    df[PLAYER_HEIGHT] = df[PLAYER_HEIGHT].str.split().str[0]  # only keep numeric value, should be in kg
    # transform salary column
    df[PLAYER_SALARY] = df[PLAYER_SALARY].str.extract(r'£([\d,]+)\s*p/w')[0]
    df[PLAYER_SALARY] = df[PLAYER_SALARY].str.replace(',', '').astype(float)
    # transform transfer value column
    df[PLAYER_MAX_TRANSFER_VALUE] = df[PLAYER_TRANSFER_VALUE].astype(str).apply(find_max_transfer_value_regex_func)

    # extract distance covered
    df[DIST] = df[DIST].str.extract(r'([\d.]+)').astype(float)
    df[DIST_90] = round(df[DIST] / df[MINS].astype(int) * 90, 2)

    # Convert % string to float
    df[PERCENT_FIELDS] = df[PERCENT_FIELDS].apply(
        lambda x: (pd.to_numeric(x.str.rstrip('%'), errors='coerce') / 100)).fillna(0)

    df[NUMERIC_FIELDS] = df[NUMERIC_FIELDS].apply(pd.to_numeric, errors='coerce')
    return df

# def merge_possession_to_df(players_df: pd.DataFrame, teams_df: pd.DataFrame) -> pd.DataFrame:
    
#     # drop existing 'team_poss' column if exists
#     players_df = players_df.drop(columns='team_poss', errors='ignore')

#     # add team possession column to players dataframe
#     teams_df = teams_df.drop(columns='division')
#     players_df = pd.merge(players_df, teams_df, on='club', how='left')
#     # check if there is any player row without poss
#     print('All players have team possession:', players_df['poss'].notna().all())
#     players_df = players_df.rename(columns={'poss': 'team_poss'})
#     players_df['team_poss'] = players_df['team_poss'] / 100

#     return players_df

def normalize_metrics(df: pd.DataFrame) -> pd.DataFrame:

    normalize_90_fn = lambda metric: round(df[metric] / df[MINS] * 90, 2)
    
    # normalize some metrics to per 90
    df[FLS_90] = normalize_90_fn(FLS)
    df[FA_90] = normalize_90_fn(FA)
    df[TCK_A_90] = normalize_90_fn(TCK_A)
    df[XG_OP_90] = normalize_90_fn(XG_OP)
    df[GL_MST_90] = normalize_90_fn(GL_MST)

    # TODO: normalize more metrics if needed
    return df

def add_custom_metrics(df: pd.DataFrame) -> pd.DataFrame:

    df[POSS_NET_90] = df[POSS_WON_90] - df[POSS_LOST_90]
    df[DEF_ACT_90] = df[TCK_A_90] + df[INT_90] + df[FLS_90]
    df[PRES_R] = round(df[PRES_C_90] / df[PRES_A_90], 2)
    df[PR_PASSES_R] = round(df[PR_PASSES_90] / df[PS_C_90] * 100, 2)

    # TODO: normalize more custom metrics if needed
    return df

# def add_poss_adjusted_metrics(df: pd.DataFrame) -> pd.DataFrame:
#     if 'team_poss' not in df.columns:
#         # Return the original DataFrame if 'team_poss' column is missing
#         return df

#     metrics_to_adjust = [
#         'def_act_90',
#         'poss_won_90',
#         'pres_a_90',
#         'blk_90',
#         'int_90',
#         'k_tck_90',
#         'tck_90',
#     ]
    
#     # Filter metrics that exist in the DataFrame
#     metrics_to_adjust = [m for m in metrics_to_adjust if m in df.columns]

#     if not metrics_to_adjust:
#         # No metrics to adjust, return the DataFrame as is
#         return df

#     # Precompute the adjustment factor to avoid recomputation
#     team_poss = df['team_poss']
#     adjustment_factor = 2 / (1 + np.exp(-0.1 * (team_poss * 100 - 50)))

#     # Add adjusted metrics
#     for metric in metrics_to_adjust:
#         adj_col = f'padj_{metric}'
#         df[adj_col] = round(df[metric] * adjustment_factor, 2)

#     return df
