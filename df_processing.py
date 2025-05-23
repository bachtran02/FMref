import pandas as pd
import numpy as np

from errors import *
from fm_mapping import *
from utils import *

def verify_dataframe_columns():
    pass

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:

    df = df.drop(columns=['Rec', 'Inf'], errors='ignore')           # not useful for analysis
    df = df.dropna(subset=[PLAYER_UID])                             # drop rows with no player UID
    df = df.drop(columns=[DIST_90])                                 # not exported correctly by FM24 (all zeros)

    # TODO: ensure that dataframe has all the columns we need

    # Drop all players that haven't played a single minute (Mins = '-')
    df = df[df[MINS] != '-']

    # weird bug when "Tck W" is sometimes saved as "Tck C"
    if 'Tck C' in df.columns:
        df.rename(columns={'Tck C': 'Tck W'}, inplace=True)

    # use UID as index
    df[PLAYER_UID] = df[PLAYER_UID].astype(str).str.replace(',', '')
    df = df.set_index(PLAYER_UID)
    
    # transform weight columns
    df[PLAYER_HEIGHT] = df[PLAYER_HEIGHT].apply(transform_height).astype(int)
    df[PLAYER_WEIGHT] = df[PLAYER_WEIGHT].apply(transform_weight).astype(int)

    # TODO: handle salary/transfer value in different units
    try:
        # transform salary column
        df[PLAYER_SALARY] = df[PLAYER_SALARY].str.extract(r'£([\d,]+)\s*p/w')[0]
        df[PLAYER_SALARY] = df[PLAYER_SALARY].str.replace(',', '').astype(float)
    except Exception as e:
        raise SalaryParsingError(f"Error processing salary: {e}") from e
    try:
        # transform transfer value column
        df[PLAYER_MAX_TRANSFER_VALUE] = df[PLAYER_TRANSFER_VALUE].astype(str).apply(find_max_transfer_value_regex_func)
    except Exception as e:
        raise TransferValueParsingError(f"Error processing transfer value: {e}") from e

    # transform distance covered
    df[DIST] = df[DIST].apply(transform_distance).astype(float)
    df[DIST_90] = round(df[DIST] / df[MINS].astype(int) * 90, 2)

    # Replace missing stats with 0s
    # Note: in Football Manager - ~ 0
    df = df.replace('-', 0)

    # Convert % string to float
    df[PERCENT_FIELDS] = df[PERCENT_FIELDS].apply(
        lambda x: (pd.to_numeric(x.str.rstrip('%'), errors='coerce') / 100)).fillna(0)

    df[NUMERIC_FIELDS] = df[NUMERIC_FIELDS].apply(pd.to_numeric, errors='coerce')
    return df

def normalize_metrics(df: pd.DataFrame) -> pd.DataFrame:
    normalize_90_fn = lambda metric: round(df[metric] / df[MINS] * 90, 2)
    normalized_cols = {
        FLS_90: normalize_90_fn(FLS),
        FA_90: normalize_90_fn(FA),
        TCK_A_90: normalize_90_fn(TCK_A),
        XG_OP_90: normalize_90_fn(XG_OP),
        GL_MST_90: normalize_90_fn(GL_MST),
    }
    return df.assign(**normalized_cols)

def add_custom_metrics(df: pd.DataFrame) -> pd.DataFrame:

    df[POSS_NET_90] = df[POSS_WON_90] - df[POSS_LOST_90]
    df[DEF_ACT_90] = df[TCK_A_90] + df[INT_90] + df[FLS_90]
    df[PRES_R] = round(df[PRES_C_90] / df[PRES_A_90], 2)
    df[PR_PASSES_R] = round(df[PR_PASSES_90] / df[PS_C_90] * 100, 2)

    # TODO: normalize more custom metrics if needed
    return df