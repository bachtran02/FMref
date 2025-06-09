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
    df = df.sort_index()                                            # sort by player UID
    
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

    preset_percent_fields  = list(PRESET_PERCENT_FIELDS)
    preset_numeric_fields = list(PRESET_NUMERIC_FIELDS)

    # Replace missing stats with 0s (Note: in Football Manager - ~ 0)
    df[preset_numeric_fields] = df[preset_numeric_fields].replace('-', 0).fillna(0)
    # Convert % string to float
    df[preset_percent_fields] = df[preset_percent_fields].apply(
        lambda x: (pd.to_numeric(x.str.rstrip('%'), errors='coerce') / 100)).fillna(0)
    
    df[preset_numeric_fields] = df[preset_numeric_fields].apply(pd.to_numeric, errors='coerce')
    return df

def parse_player_position(df: pd.DataFrame) -> pd.DataFrame:
    pos_array = df[PLAYER_POSITION].apply(parse_position)
    pos_df = pd.DataFrame(pos_array.tolist(), index=df.index)
    pos_df.columns = ['Goalkeeper', 'Centerback', 'Fullback', 'Midfielder', 'Att-Mid/Winger', 'Forward']
    return df.join(pos_df)

def normalize_metrics(df: pd.DataFrame) -> pd.DataFrame:
    normalize_90_fn = lambda metric: series_ratio_with_fallback(df[metric] * 90, df[MINS])
    normalized_cols = {
        CCC_90: normalize_90_fn(CCC),
        DEF_ACT_A_90: normalize_90_fn(DEF_ACT_A),
        DEF_ACT_C_90: normalize_90_fn(DEF_ACT_C),
        FA_90: normalize_90_fn(FA),
        FLS_90: normalize_90_fn(FLS),
        GLS_AST_90: normalize_90_fn(GLS_AST),
        GL_MST_90: normalize_90_fn(GL_MST),
        GLS_OUT_BOX_90: normalize_90_fn(GLS_OUT_BOX),
        NP_G_90: normalize_90_fn(NP_G),
        NP_XG_XA_90: normalize_90_fn(NP_XG_XA),
        NP_XG_OP_90: normalize_90_fn(NP_XG_OP),
        OFF_90: normalize_90_fn(OFF),
        PEN_S_90: normalize_90_fn(PEN_S),
        PENS_90: normalize_90_fn(PENS),
        RED_90: normalize_90_fn(RED),
        TCK_A_90: normalize_90_fn(TCK_A),
        TCK_INT_90: normalize_90_fn(TCK_INT),
        XG_OP_90: normalize_90_fn(XG_OP),
        YEL_90: normalize_90_fn(YEL),
    }
    return df.assign(**normalized_cols)

def add_custom_metrics(df: pd.DataFrame) -> pd.DataFrame:

    custom_metrics = {
        # FBref metrics
        # BLK_PAS_90:     np.round(df[BLK_90] - df[BLK_SHT_90], 2),
        GLS_AST:        df[GLS] + df[AST],
        NP_G:           df[GLS] - df[PEN_S],
        NP_XG_XA:       df[NP_XG] + df[XA],
        CONV_OT_R:      series_ratio_with_fallback(df[GLS_90], df[SHT_90]), 
        NP_XG_OP:       (df[GLS] - df[PEN_S]) - df[NP_XG],
        NP_XG_SHOT:     series_ratio_with_fallback(df[NP_XG_90], df[SHOT_90]),
        TCK_INT :       df[TCK_W] + df[INT],

        DEF_ACT_C:      df[HDRS_W] + df[TCK_W] + df[INT] + df[BLK] + df[CLR],
        DEF_ACT_F:      (df[AER_A] - df[HDRS_W]) + (df[TCK_A] - df[TCK_W]) + (df[PRES_A] - df[PRES_C]) + df[FLS],

        POSS_NET_90:    df[POSS_WON_90] - df[POSS_LOST_90],
        PRES_R:         series_ratio_with_fallback(df[PRES_C_90], df[PRES_A_90]),
        PR_PASSES_R:    series_ratio_with_fallback(df[PR_PASSES_90], df[PS_C_90]),

        # % columns not correctly computed by FM
        OP_CR_R:        series_ratio_with_fallback(df[OP_CRS_C_90], df[OP_CRS_A_90])
    }
    df = df.assign(**custom_metrics)
    df[DEF_ACT_A] = df[DEF_ACT_C] + df[DEF_ACT_F]
    df[DEF_ACT_R] = series_ratio_with_fallback(df[DEF_ACT_C], df[DEF_ACT_A])
    return df

def get_percentile_df_by_groups(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Create a DataFrame with percentiles for each position group in the original DataFrame.
    """

    percentile_dfs = {}

    # list of columns to keep for percentile dataframe
    percentile_metrics = list(set().union(
        PER90_PERCENTILE_STANDARD_STATS,
        PER90_PERCENTILE_SHOOTING_STATS,
        PER90_PERCENTILE_PASSING_STATS,
        PER90_PERCENTILE_DEFENDING_STATS,
        PER90_PERCENTILE_POSSESSION_STATS,
        PER90_PERCENTILE_MISC_STATS,
    ))
    
    for group in POSITION_GROUPS:
        # filter the players for the current position group
        filtered_df = df[df[group] == 1]        
        # if dataframe is empty or has fewer than 100 rows then skip
        if filtered_df.empty or filtered_df.shape[0] < 100:
            continue

        # only keep numeric columns for percentile calculation
        percentiles = {}
        for metric in percentile_metrics:
            if metric not in filtered_df.columns or not pd.api.types.is_numeric_dtype(filtered_df[metric]):
                continue

            invert = metric in INVERTED_PERCENTILE_FIELDS
            series = filtered_df[metric].rank(pct=True).apply(lambda x: to_percentile(x, invert))
            percentiles[metric] = series

        group_df = pd.DataFrame(percentiles, index=filtered_df.index)
        percentile_dfs[group] = group_df

    # st.write(percentile_dfs)
    return percentile_dfs