import re
import numpy as np
import pandas as pd
from scipy import stats

from fm_mapping import *

FONT_NORMAL_FILE = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Regular.ttf'
FONT_ITALIC_FILE = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Italic.ttf'
FONT_BOLD_FILE = 'https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/RobotoSlab[wght].ttf'

REGEX_HEIGHT_CM_PATTERN = r'(\d+)\scm'
REGEX_HEIGHT_FT_PATTERN = r'(\d+)\'(\d+)\"'
REGEX_WEIGHT_KG_PATTERN = r'(\d+)\skg'
REGEX_WEIGHT_LB_PATTERN = r'(\d+)\slb'

def find_max_transfer_value_regex_func(value_string):
    """
    Find the maximum transfer value from transfer value string.
    """

    pattern = r'£(\d+\.*\d*[MK]*)'
    
    if (found := re.findall(pattern, value_string)):
        s = found[-1]
        if len(s) == 1:
            return 0
        val, unit = float(s[:-1]), s[-1] 
        if unit == 'M':
            val *= 1_000_000
        elif unit == 'K':
            val *= 1000
        return val
    elif value_string == 'Not for Sale':
        return float('inf')
    elif value_string in ('Unknown', 'nan'):
        return np.nan
    else:
        raise Exception('unknown format')
    
def find_first_row():
    pass
    
def transform_height(height_str):
    if re.match(REGEX_HEIGHT_CM_PATTERN, height_str):
        return int(height_str.split()[0])
    elif match := re.match(REGEX_HEIGHT_FT_PATTERN, height_str):
        ft, inch = match.groups()
        return round(int(ft) * 30.48 + int(inch) * 2.54)
    else:
        raise ValueError(f"Invalid height format: {height_str}")
    
def transform_weight(weight_str):
    if re.match(REGEX_WEIGHT_KG_PATTERN, weight_str):
        return int(weight_str.split()[0])
    elif match := re.match(REGEX_WEIGHT_LB_PATTERN, weight_str):
        lb = match.group(1)
        return round(int(lb) * 0.453592)
    else:
        raise ValueError(f"Invalid weight format: {weight_str}")

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
        raise ValueError(f"Invalid distance format: {distance_str}")
    
def parse_position(position_str) -> tuple:
    """
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
    
def player_stats_to_tuple_data(player_stats: dict, stats_to_include: dict, df):
    """
    Convert player stats to a tuple of tuples for FBref-like HTML table rendering.
    """

    res = []
    for key in stats_to_include:
        percentile = 0
        stat = player_stats.get(key, 0)
        if stat is not None and not np.isnan(stat):
            percentile = stats.percentileofscore(df[key], stat, kind='rank')
            if np.isnan(percentile):
                percentile = 0
            percentile = round(percentile)

            # Invert percentile for certain fields
            if key in INVERTED_PERCENTILE_FIELDS:
                percentile = 100 - percentile

            percentile = max(1, min(99, percentile))

        field_tuple = (stats_to_include[key], round(stat, 2), percentile)
        res.append(field_tuple)
    return res
    
def series_ratio_with_fallback(num: pd.Series, denom: pd.Series, fallback=0):
    """
    Calculate series ratio with a fallback value if denominator is zero or NaN.
    """
    return np.where(denom != 0, num / denom, fallback)

def render_percentile_box(perc):
    color = (
        "#3aaf3a" if perc >= 90 else
        "#5caf5c" if perc >= 80 else
        "#66af66" if perc >= 70 else
        "#82af82" if perc >= 60 else
        "#9baf9b" if perc >= 50 else
        "#afafaf" if perc >= 40 else
        "#af9191" if perc >= 30 else
        "#af6c6c" if perc >= 20 else
        "#af5f5f" if perc >= 10 else
        "#af3c3c"
    )
    return f'''
        <div style="display: flex;">
            <div align="center" style="min-width: 22px; display: inline-block;">{perc}</div>
            <div style="width: 200px;">
                <div style="width: {perc}%; height: 100%; background-color: {color};"></div>
            </div>
        </div>
    '''
    
stats_table_css = """
<style>
    table {
        border-collapse: collapse;
        font-size: 14px;
        border: 1px solid #888;
    }

    thead th {
        font-weight: bold;
        text-align: center;
        vertical-align: middle;
        background-color: #f5f5f5;
        border: 1px solid #888;
        padding: 3px 4px;
    }

    td {
        padding: 3px 4px;
        text-align: right;
        border-bottom: 1px solid #ddd;
        border-right: 1px solid #888;
        vertical-align: middle;
    }

    td:last-child {
        border-right: none;
    }
    tr:last-child td {
        border-bottom: 1px solid #888;
}
</style>
"""