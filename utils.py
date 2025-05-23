import re
import numpy as np

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
            val *= 1_000_000_000
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
    
def player_stats_to_tuple_data(player_stats: dict):
    """
    Convert player stats to a tuple of tuples for FBref-like HTML table rendering.
    """




    return tuple(
        (stat['stat'], stat['per90'], stat['percentile'])
        for stat in player_stats
    )
    pass
    
def render_perc_box(perc):
    color = (
        "#4CAF50" if perc >= 60 else
        "#9E9E9E" if perc >= 40 else
        "#E57373"
    )
    return f'''
        <div style="display: flex;">
            <div align="center" style="min-width: 22px; display: inline-block;">{perc}</div>
            <div style="width: 150px;">
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
        padding: 6px 8px;
    }

    td {
        padding: 6px 8px;
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