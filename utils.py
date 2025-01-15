import re
import numpy as np

FONT_NORMAL_FILE = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Regular.ttf'
FONT_ITALIC_FILE = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Italic.ttf'
FONT_BOLD_FILE = 'https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/RobotoSlab[wght].ttf'

def find_max_transfer_value_regex_func(value_string):
    """
    
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