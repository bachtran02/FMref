import re
import numpy as np
import pandas as pd

from ..constants import *
from ..errors.errors import MissingColumnsError, InvalidColumnValueError

REGEX_HEIGHT_CM_PATTERN = r'(\d+)\scm'
REGEX_HEIGHT_FT_PATTERN = r'(\d+)\'(\d+)"'
REGEX_WEIGHT_KG_PATTERN = r'(\d+)\skg'
REGEX_WEIGHT_LB_PATTERN = r'(\d+)\slb'

def find_max_transfer_value(value_string):
    """
    Find the maximum transfer value from transfer value string.

    Args:
        value_string: Transfer value string (e.g., "£5M-£10M", "Not for Sale")
        
    Returns:
        float: Maximum transfer value in pounds (£)

    Raises:
        InvalidColumnValueError: If the format of the value_string is unexpected
            or unit not in pounds.
    """

    NOT_FOR_SALE_VALUE = 999_999_999

    # handle edge cases
    if pd.isna(value_string) or value_string in ('Unknown', '-', 'nan'):
        return 0
    if value_string == 'Not for Sale':
        return NOT_FOR_SALE_VALUE

    if (found := re.findall(r'£(\d+\.*\d*[MK]*)', value_string)):
        s = found[-1]       # get the last value (max)

        # If no M or K suffix then return as is
        if s[-1] not in ('M', 'K'):
            return float(s)
        
        val, unit = float(s[:-1]), s[-1]
        if unit == 'M':
            val *= 1_000_000
        elif unit == 'K':
            val *= 1000
        return val
    else:
        raise InvalidColumnValueError(
            PLAYER_TRANSFER_VALUE,
            f"Unexpected value: \"{value_string}\". Currency Unit should be \"£\"")
    
def transform_height(height_str):
    if re.match(REGEX_HEIGHT_CM_PATTERN, height_str):
        return int(height_str.split()[0])
    elif match := re.match(REGEX_HEIGHT_FT_PATTERN, height_str):
        ft, inch = match.groups()
        return round(int(ft) * 30.48 + int(inch) * 2.54)
    else:
        raise InvalidColumnValueError(
            PLAYER_HEIGHT,
            f"Unexpected value: \"{height_str}\". Height should be in cm or ft/inch format")
    
def transform_weight(weight_str):
    if re.match(REGEX_WEIGHT_KG_PATTERN, weight_str):
        return int(weight_str.split()[0])
    elif match := re.match(REGEX_WEIGHT_LB_PATTERN, weight_str):
        lb = match.group(1)
        return round(int(lb) * 0.453592)
    else:
        raise InvalidColumnValueError(
            PLAYER_WEIGHT,
            f"Unexpected value: \"{weight_str}\". Weight should be in kg or lb format")

def transform_distance(distance_str):
    if distance_str == '-':
        return 0
    if distance_str[-2:] == 'mi':
        # already in miles
        return float(distance_str[:-2])
    elif distance_str[-2:] == 'km':
        # convert km to miles
        in_km = float(distance_str[:-2])
        return round(in_km * 0.621371, 1)
    else:
        raise InvalidColumnValueError(
            DIST,
            f"Unexpected value: \"{distance_str}\". Distance should be in km or mi format")

def parse_player_position_str(position_str) -> tuple:
    """
    Parse the player's position string into a tuple of position indicators.
    """
    positions = [0, 0, 0, 0, 0, 0]
    pos_groups = position_str.split(',')
    for group in pos_groups:
        p = group.split()

        # edge case
        if p[0] == 'GK':
            positions[0] = 1
            continue
        if p[0] == 'DM':
            positions[3] = 1
            continue

        pos = p[0].split('/')   # D WB M AM ST
        side = p[1].strip('()')  # R L C

        if 'D' in pos and 'C' in side:
            positions[1] = 1
        if any(x in pos for x in ['D', 'WB']) and any(x in side for x in ['R', 'L']):
            positions[2] = 1
        if any(x in pos for x in ['DM', 'M']) and 'C' in side:
            positions[3] = 1
        if any(x in pos for x in ['M', 'AM']) and any(x in side for x in ['R', 'L']) or \
            ('AM' in pos and 'C' in side):
            positions[4] = 1
        if 'ST' in pos:
            positions[5] = 1
    return tuple(positions)

def add_player_position_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add player position columns to the DataFrame.
    """
    pos_array = df[PLAYER_POSITION].apply(parse_player_position_str)
    pos_df = pd.DataFrame(pos_array.tolist(), index=df.index)
    pos_df.columns = [GOALKEEPER, CENTERBACK, FULLBACK, MIDFIELDER, ATT_MID_WINGER, FORWARD]
    return df.join(pos_df)

def preprocess_player_dataframe(df):
    """
    Preprocess player dataframe by cleaning, transforming, and standardizing data.
    
    Args:
        df: Raw player DataFrame with required columns
        
    Returns:
        pd.DataFrame: Preprocessed DataFrame with cleaned and transformed data
        
    Raises:
        InvalidColumnValueError: If any column value has unexpected format
    """
    df = df.dropna(subset=[PLAYER_UID])                             # Drop rows with no player UID
    df = df.drop(columns=['Rec', 'Inf'], errors='ignore')           # Drop columns not useful for analysis
    df = df.drop(columns=[DIST_90], errors='ignore')                # Drop as not exported correctly by FM24 (all zeros)
    df = df[df[MINS] != '-']                                        # Drop players with no minutes played

    # Use player UID as index & Sort by UID
    df[PLAYER_UID] = df[PLAYER_UID].astype(str).str.replace(',', '')
    df = df.set_index(PLAYER_UID).sort_index()

    df[PLAYER_HEIGHT] = df[PLAYER_HEIGHT].apply(transform_height).astype(int)
    df[PLAYER_WEIGHT] = df[PLAYER_WEIGHT].apply(transform_weight).astype(int)
    df[PLAYER_MAX_TRANSFER_VALUE] = df[PLAYER_TRANSFER_VALUE].astype(str).apply(
        find_max_transfer_value).astype(float)
    df[DIST] = df[DIST].apply(transform_distance).astype(float)

    # Assign types for numeric columns
    df[list(PRESET_NUMERIC_FIELDS)] = df[list(PRESET_NUMERIC_FIELDS)].replace('-', 0).fillna(0)
    df[list(PRESET_NUMERIC_FIELDS)] = df[list(PRESET_NUMERIC_FIELDS)].apply(pd.to_numeric, errors='coerce')

    # Assign types for percentage columns
    df[list(PRESET_PERCENT_FIELDS)] = df[list(PRESET_PERCENT_FIELDS)].replace('-', '0%')
    df[list(PRESET_PERCENT_FIELDS)] = df[list(PRESET_PERCENT_FIELDS)].apply(
        lambda x: pd.to_numeric(x.str.rstrip('%'), errors='coerce') / 100).fillna(0)
    
    return df