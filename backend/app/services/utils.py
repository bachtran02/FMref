import pandas as pd
import numpy as np
import logging
from typing import Set, List

from ..errors.errors import MissingColumnsError

logger = logging.getLogger(__name__)

def verify_columns(df: pd.DataFrame, required_columns: Set[str]) -> None:
    """
    Verify that the DataFrame contains all required columns.
    
    Args:
        df: DataFrame to validate
        required_columns: Set of required column names
        
    Raises:
        MissingColumnsError: If any required columns are missing
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise MissingColumnsError(missing_columns)

def series_ratio_with_fallback(num: pd.Series, denom: pd.Series, fallback: float = 0) -> pd.Series:
    """
    Calculate series ratio with a fallback value if denominator is zero or NaN.
    
    Args:
        num: Numerator series
        denom: Denominator series
        fallback: Value to use when division is invalid
        
    Returns:
        pd.Series: Ratio with fallback for invalid divisions
    """
    result = np.where((denom != 0) & (~denom.isna()), num / denom, fallback)
    return pd.Series(result, index=num.index)

def log_dropped_rows(initial_count: int, final_count: int, reason: str) -> None:
    """Log the number of rows dropped during processing."""
    dropped = initial_count - final_count
    if dropped > 0:
        logger.info(f"Dropped {dropped} rows ({dropped/initial_count*100:.1f}%): {reason}")

def safe_apply_transform(
    series: pd.Series, 
    transform_func, 
    column_name: str,
    default_value = None
) -> pd.Series:
    """
    Safely apply a transformation function with error handling.
    
    Args:
        series: Series to transform
        transform_func: Function to apply
        column_name: Column name for error messages
        default_value: Value to use if transformation fails
        
    Returns:
        pd.Series: Transformed series
    """
    try:
        return series.apply(transform_func)
    except Exception as e:
        logger.error(f"Error transforming {column_name}: {e}")
        if default_value is not None:
            return pd.Series([default_value] * len(series), index=series.index)
        raise