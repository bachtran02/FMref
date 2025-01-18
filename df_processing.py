import pandas as pd
import numpy as np

from fm_mapping import *
from utils import *

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:

    # drop rows with no player UID
    df = df.dropna(subset=['UID'])

    # sanity check to ensure all the necessary fields are included
    required_fields = list(nonnumeric_fields_to_cc.keys()) + list(numeric_fields_to_cc.keys())
    missing_fields = [f for f in required_fields if f not in df.columns]

    if missing_fields:
        print(f"Missing fields: {missing_fields}")
    else:
        print("DataFrame contains all required fields.")

    # renaming FM fields to camel case
    df = df.rename(columns=nonnumeric_fields_to_cc)
    df = df.rename(columns=numeric_fields_to_cc)

    # use UID as index
    df['uid'] = df['uid'].astype(str).str.replace(',', '')
    df = df.set_index('uid')
    
    # 'Rec' and 'Info' are not useful
    # 'Dist/90' are not exported correctly by FM24 (all zeros)
    df = df.drop(columns=['rec', 'inf', 'dist_90'])

    # Replace missing stats with 0s
    # Note: in Football Manager - ~ 0
    df = df.replace('-', 0)

    # transform weight, height columns
    df['weight'] = df['weight'].str.split().str[0]  # only keep numeric value, should be in cm
    df['height'] = df['height'].str.split().str[0]  # only keep numeric value, should be in kg

    # transform salary column (expected to be in £ per week)
    df['salary'] = df['salary'].str.extract(r'£([\d,]+)\s*p/w')[0]
    df['salary'] = df['salary'].str.replace(',', '').astype(float)

    # transform transfer value column (expected to be in £)
    df['max_transfer_value'] = df['transfer_value'].astype(str).apply(find_max_transfer_value_regex_func)

    # extract distance covered
    df['dist'] = df['dist'].str.extract(r'([\d.]+)').astype(float)
    df['dist_90'] = round(df['dist'] / df['mins'].astype(int) * 90, 2)

    # Convert % string to float
    percent_columns = ['shot_r', 'conv_r', 'pas_r', 'op_cr_r', 'tck_r', 'hdr_r']
    df[percent_columns] = df[percent_columns].apply(
        lambda x: (pd.to_numeric(x.str.rstrip('%'), errors='coerce') / 100)).fillna(0)

    numeric_columns = list(numeric_cc_to_fields.keys())
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    return df

def merge_possession_to_df(players_df: pd.DataFrame, teams_df: pd.DataFrame) -> pd.DataFrame:
    
    # drop existing 'team_poss' column if exists
    players_df = players_df.drop(columns='team_poss', errors='ignore')

    # add team possession column to players dataframe
    teams_df = teams_df.drop(columns='division')
    players_df = pd.merge(players_df, teams_df, on='club', how='left')
    # check if there is any player row without poss
    print('All players have team possession:', players_df['poss'].notna().all())
    players_df = players_df.rename(columns={'poss': 'team_poss'})
    players_df['team_poss'] = players_df['team_poss'] / 100

    return players_df

def normalize_metrics(df: pd.DataFrame) -> pd.DataFrame:

    normalize_90_fn = lambda metric: round(df[metric] / df['mins'] * 90, 2)
    
    # normalize some metrics to per 90
    df['fls_90'] = normalize_90_fn('fls')
    df['fa_90'] = normalize_90_fn('fa')
    df['tck_a_90'] = normalize_90_fn('tck_a')
    df['xg_op_90'] = normalize_90_fn('xg_op')
    df['gl_mst_90'] = normalize_90_fn('gl_mst')

    # TODO: normalize more metrics if needed

    return df

def add_custom_metrics(df: pd.DataFrame) -> pd.DataFrame:

    df['net_poss_90'] = df['poss_won_90'] - df['poss_lost_90']              # net possession gain per 90
    df['def_act_90'] = df['tck_a_90'] + df['int_90'] + df['fls_90']         # defensive actions per 90
    df['pres_r'] = round(df['pres_c_90'] / df['pres_a_90'], 2)              # pressure success %
    df['pr_passes_r'] = round(df['pr_passes_90'] / df['ps_c_90'] * 100, 2)  # ratio of progressive passes to passes completed 

    return df

def add_poss_adjusted_metrics(df: pd.DataFrame) -> pd.DataFrame:
    if 'team_poss' not in df.columns:
        # Return the original DataFrame if 'team_poss' column is missing
        return df

    metrics_to_adjust = [
        'def_act_90',
        'poss_won_90',
        'pres_a_90',
        'blk_90',
        'int_90',
        'k_tck_90',
        'tck_90',
    ]
    
    # Filter metrics that exist in the DataFrame
    metrics_to_adjust = [m for m in metrics_to_adjust if m in df.columns]

    if not metrics_to_adjust:
        # No metrics to adjust, return the DataFrame as is
        return df

    # Precompute the adjustment factor to avoid recomputation
    team_poss = df['team_poss']
    adjustment_factor = 2 / (1 + np.exp(-0.1 * (team_poss * 100 - 50)))

    # Add adjusted metrics
    for metric in metrics_to_adjust:
        adj_col = f'padj_{metric}'
        df[adj_col] = round(df[metric] * adjustment_factor, 2)

    return df
