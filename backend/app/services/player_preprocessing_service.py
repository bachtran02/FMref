import re
import numpy as np
import pandas as pd
import logging
from typing import Tuple

from ..constants import *
from ..errors.errors import InvalidColumnValueError
from .utils import series_ratio_with_fallback, log_dropped_rows

logger = logging.getLogger(__name__)

# Pre-compile regex patterns for performance
HEIGHT_CM_REGEX = re.compile(r'(\d+)\s*cm')
HEIGHT_FT_REGEX = re.compile(r'(\d+)\'(\d+)"')
WEIGHT_KG_REGEX = re.compile(r'(\d+)\s*kg')
WEIGHT_LB_REGEX = re.compile(r'(\d+)\s*lb')
TRANSFER_VALUE_REGEX = re.compile(r'£(\d+\.?\d*[MK]*)')

# Constants
NOT_FOR_SALE_VALUE = 999_999_999
MISSING_VALUE_INDICATORS = {'Unknown', '-', 'nan', ''}


def find_max_transfer_value(value_string: str) -> float:
    """
    Extract the maximum transfer value from a transfer value string.
    
    Args:
        value_string: Transfer value string (e.g., "£5M-£10M")
        
    Returns:
        float: Maximum transfer value in pounds
        
    Raises:
        InvalidColumnValueError: If value format is unexpected
    """
    # Handle edge cases
    if pd.isna(value_string) or str(value_string).strip() in MISSING_VALUE_INDICATORS:
        return 0.0
    
    value_string = str(value_string).strip()
    if value_string == 'Not for Sale':
        return float(NOT_FOR_SALE_VALUE)

    # Extract all values and take the maximum
    matches = TRANSFER_VALUE_REGEX.findall(value_string)
    if not matches:
        raise InvalidColumnValueError(
            PLAYER_TRANSFER_VALUE,
            f'Unexpected value: "{value_string}". Expected format: £XX.XM or £XX.XK'
        )
    
    max_value_str = matches[-1]  # Last value is typically the max
    
    # Parse value with unit
    if max_value_str[-1] not in ('M', 'K'):
        return float(max_value_str)
    
    value, unit = float(max_value_str[:-1]), max_value_str[-1]
    multiplier = 1_000_000 if unit == 'M' else 1_000
    return value * multiplier


def transform_height(height_str: str) -> int:
    """
    Convert height from various formats to centimeters.
    
    Args:
        height_str: Height string (e.g., "180 cm")
        
    Returns:
        int: Height in centimeters
        
    Raises:
        InvalidColumnValueError: If format is unexpected
    """
    height_str = str(height_str).strip()
    
    # Try centimeters first
    if match := HEIGHT_CM_REGEX.match(height_str):
        return int(match.group(1))
    
    # Try feet/inches
    if match := HEIGHT_FT_REGEX.match(height_str):
        feet, inches = match.groups()
        return round(int(feet) * 30.48 + int(inches) * 2.54)
    
    raise InvalidColumnValueError(
        PLAYER_HEIGHT,
        f'Unexpected value: "{height_str}". Expected format: "XXX cm""'
    )


def transform_weight(weight_str: str) -> int:
    """
    Convert weight from various formats to kilograms.
    
    Args:
        weight_str: Weight string (e.g., "75 kg")
        
    Returns:
        int: Weight in kilograms
        
    Raises:
        InvalidColumnValueError: If format is unexpected
    """
    weight_str = str(weight_str).strip()
    
    # Try kilograms first
    if match := WEIGHT_KG_REGEX.match(weight_str):
        return int(match.group(1))
    
    # Try pounds
    if match := WEIGHT_LB_REGEX.match(weight_str):
        pounds = int(match.group(1))
        return round(pounds * 0.453592)
    
    raise InvalidColumnValueError(
        PLAYER_WEIGHT,
        f'Unexpected value: "{weight_str}". Expected format: "XX kg"'
    )


def transform_distance(distance_str: str) -> float:
    """
    Convert distance to miles.
    
    Args:
        distance_str: Distance string (e.g., "6.5 mi")
        
    Returns:
        float: Distance in miles
        
    Raises:
        InvalidColumnValueError: If format is unexpected
    """
    distance_str = str(distance_str).strip()
    
    if distance_str in MISSING_VALUE_INDICATORS:
        return 0.0
    
    if distance_str.endswith('mi'):
        return float(distance_str[:-2].strip())
    
    if distance_str.endswith('km'):
        km_value = float(distance_str[:-2].strip())
        return round(km_value * 0.621371, 1)
    
    raise InvalidColumnValueError(
        DIST,
        f'Unexpected value: "{distance_str}". Expected format: "XX.X mi"'
    )


def parse_position_str(position_str: str) -> Tuple[int, ...]:
    """
    Parse player position string into one-hot encoded tuple.
    
    Format: "D/WB (R), M (C)" -> positions for each role
    
    Args:
        position_str: Position string from FM
        
    Returns:
        Tuple of 6 integers (GK, CB, FB, MID, AM/W, FW)
    """
    positions = [0, 0, 0, 0, 0, 0]
    pos_groups = str(position_str).split(',')
    
    for group in pos_groups:
        parts = group.strip().split()
        if not parts:
            continue
        
        position_code = parts[0]
        
        # Handle special cases first
        if position_code == 'GK':
            positions[0] = 1
            continue
        if position_code == 'DM':
            positions[3] = 1
            continue
        
        # Parse position and side
        pos_roles = position_code.split('/')
        side = parts[1].strip('()') if len(parts) > 1 else 'C'
        
        # Map to position categories
        if 'D' in pos_roles and 'C' in side:
            positions[1] = 1  # Center back
        
        if any(role in pos_roles for role in ['D', 'WB']) and any(s in side for s in ['R', 'L']):
            positions[2] = 1  # Fullback
        
        if any(role in pos_roles for role in ['DM', 'M']) and 'C' in side:
            positions[3] = 1  # Midfielder
        
        if (any(role in pos_roles for role in ['M', 'AM']) and any(s in side for s in ['R', 'L'])) or \
           ('AM' in pos_roles and 'C' in side):
            positions[4] = 1  # Attacking mid/winger
        
        if 'ST' in pos_roles:
            positions[5] = 1  # Forward
    
    return tuple(positions)


def clean_player_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate player dataframe.
    
    Steps:
    - Remove rows with missing player UID
    - Remove players with no minutes played
    - Drop unnecessary columns
    - Set index to player UID
    
    Args:
        df: Raw player DataFrame
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    initial_count = len(df)
    
    # Drop rows with no player UID
    df = df.dropna(subset=[PLAYER_UID])
    log_dropped_rows(initial_count, len(df), "missing player UID")
    
    # Drop unnecessary columns
    df = df.drop(columns=['Rec', 'Inf'], errors='ignore')
    df = df.drop(columns=[DIST_90], errors='ignore')  # FM24 export bug
    
    # Drop players with no minutes
    initial_count = len(df)
    df = df[df[MINS] != '-']
    log_dropped_rows(initial_count, len(df), "no minutes played")
    
    # Clean and set player UID as index
    df[PLAYER_UID] = df[PLAYER_UID].astype(str).str.replace(',', '').str.strip()
    df = df.set_index(PLAYER_UID).sort_index()
    
    logger.info(f"Cleaned dataframe: {len(df)} players remaining")
    return df


def transform_units(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform physical measurements to standard units.
    
    - Height -> cm
    - Weight -> kg
    - Distance -> miles
    - Transfer value -> £
    
    Args:
        df: DataFrame with raw units
        
    Returns:
        pd.DataFrame: DataFrame with standardized units
    """
    df = df.copy()
    
    df[PLAYER_HEIGHT] = df[PLAYER_HEIGHT].apply(transform_height).astype(int)
    df[PLAYER_WEIGHT] = df[PLAYER_WEIGHT].apply(transform_weight).astype(int)
    df[PLAYER_MAX_TRANSFER_VALUE] = (
        df[PLAYER_TRANSFER_VALUE]
        .astype(str)
        .apply(find_max_transfer_value)
        .astype(float)
    )
    df[DIST] = df[DIST].apply(transform_distance).astype(float)
    
    logger.info("Transformed physical measurements to standard units")
    return df


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert columns to appropriate data types.
    
    - Numeric columns: int/float
    - Percentage columns: decimal (0-1)
    
    Args:
        df: DataFrame with string values
        
    Returns:
        pd.DataFrame: DataFrame with correct types
    """
    df = df.copy()
    
    # Convert numeric fields
    df[list(PRESET_NUMERIC_FIELDS)] = (
        df[list(PRESET_NUMERIC_FIELDS)]
        .replace('-', 0)
        .fillna(0)
        .apply(pd.to_numeric, errors='coerce')
        .fillna(0)
    )
    
    # Convert percentage fields
    df[list(PRESET_PERCENT_FIELDS)] = (
        df[list(PRESET_PERCENT_FIELDS)]
        .replace('-', '0%')
        .apply(lambda x: pd.to_numeric(x.str.rstrip('%'), errors='coerce') / 100)
        .fillna(0)
    )
    
    logger.info("Converted data types for numeric and percentage fields")
    return df


def preprocess_player_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main preprocessing pipeline for player data.
    
    Steps:
    1. Clean and validate data
    2. Transform units to standards
    3. Convert to appropriate data types
    
    Args:
        df: Raw player DataFrame with required columns
        
    Returns:
        pd.DataFrame: Preprocessed DataFrame ready for feature engineering
        
    Raises:
        InvalidColumnValueError: If any column value has unexpected format
    """
    logger.info(f"Starting preprocessing for {len(df)} players")
    
    df = clean_player_dataframe(df)
    df = transform_units(df)
    df = convert_data_types(df)
    
    logger.info("Preprocessing complete")
    return df


def add_player_position_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add one-hot encoded position columns.
    
    Creates 6 binary columns for: GK, CB, FB, MID, AM/W, FW
    
    Args:
        df: Preprocessed player DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with position columns added
    """
    pos_array = df[PLAYER_POSITION].apply(parse_position_str)
    pos_df = pd.DataFrame(
        pos_array.tolist(),
        index=df.index,
        columns=[GOALKEEPER, CENTERBACK, FULLBACK, MIDFIELDER, ATT_MID_WINGER, FORWARD]
    )
    
    logger.info("Added position encoding columns")
    return df.join(pos_df)


def add_custom_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate custom derived metrics.
    
    Includes:
    - Goal contributions (G+A, npG, npxG+xA)
    - Efficiency ratios
    - Defensive actions
    - Possession metrics
    
    Args:
        df: Preprocessed player DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with custom metrics added
    """
    custom_metrics = {
        # Attacking metrics
        GLS_AST: df[GLS] + df[AST],
        NP_G: df[GLS] - df[PEN_SC],
        NP_XG_XA: df[NP_XG] + df[XA],
        NP_XG_OP: (df[GLS] - df[PEN_SC]) - df[NP_XG],
        
        # Shooting efficiency
        CONV_OT_R: series_ratio_with_fallback(df[GLS], df[SHOT_OT]),
        NP_XG_SHOT: series_ratio_with_fallback(df[NP_XG], df[SHOTS]),
        
        # Defensive metrics
        TCK_INT: df[TCK_C] + df[INT],
        DEF_ACT_C: df[HDRS_W] + df[TCK_C] + df[INT] + df[BLK] + df[CLR],
        DEF_ACT_F: (df[AER_A] - df[HDRS_W]) + (df[TCK_A] - df[TCK_C]) + 
                   (df[PRES_A] - df[PRES_C]) + df[FLS],
        
        # Possession metrics
        POSS_NET_90: df[POSS_WON_90] - df[POSS_LOST_90],
        PRES_R: series_ratio_with_fallback(df[PRES_C_90], df[PRES_A_90]),
        PR_PASSES_R: series_ratio_with_fallback(df[PR_PASSES_90], df[PS_C_90]),
        
        # Corrected FM percentage columns
        OP_CR_R: series_ratio_with_fallback(df[OP_CRS_C_90], df[OP_CRS_A_90])
    }
    
    df = df.assign(**custom_metrics)
    
    # Defensive actions total and ratio
    df[DEF_ACT_A] = df[DEF_ACT_C] + df[DEF_ACT_F]
    df[DEF_ACT_R] = series_ratio_with_fallback(df[DEF_ACT_C], df[DEF_ACT_A])
    
    logger.info(f"Added {len(custom_metrics) + 2} custom metrics")
    return df


def normalize_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize metrics to per-90 minutes.
    
    Converts totals to per-90 rates for fair comparison across players
    with different playing time.
    
    Args:
        df: DataFrame with custom metrics
        
    Returns:
        pd.DataFrame: DataFrame with normalized metrics
    """
    def normalize_to_90(metric: str) -> pd.Series:
        return series_ratio_with_fallback(df[metric] * 90, df[MINS])
    
    normalized_cols = {
        CCC_90: normalize_to_90(CCC),
        DEF_ACT_A_90: normalize_to_90(DEF_ACT_A),
        DEF_ACT_C_90: normalize_to_90(DEF_ACT_C),
        FLS_AGST_90: normalize_to_90(FLS_AGST),
        FLS_90: normalize_to_90(FLS),
        GLS_AST_90: normalize_to_90(GLS_AST),
        GLS_OUT_BOX_90: normalize_to_90(GLS_OUT_BOX),
        MST_GL_90: normalize_to_90(MST_GL),
        NP_G_90: normalize_to_90(NP_G),
        NP_XG_XA_90: normalize_to_90(NP_XG_XA),
        NP_XG_OP_90: normalize_to_90(NP_XG_OP),
        OFF_90: normalize_to_90(OFF),
        PEN_ATT_90: normalize_to_90(PEN_ATT),
        PEN_SC_90: normalize_to_90(PEN_SC),
        RED_90: normalize_to_90(RED),
        TCK_A_90: normalize_to_90(TCK_A),
        TCK_INT_90: normalize_to_90(TCK_INT),
        XG_OP_90: normalize_to_90(XG_OP),
        YEL_90: normalize_to_90(YEL),
    }
    
    logger.info(f"Normalized {len(normalized_cols)} metrics to per-90 values")
    return df.assign(**normalized_cols)