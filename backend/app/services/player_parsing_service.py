import pandas as pd
import logging
from typing import Optional

from .player_preprocessing_service import (
    preprocess_player_dataframe,
    add_player_position_columns,
    add_custom_metrics,
    normalize_metrics
)
from .utils import verify_columns

from ..constants import *
from ..errors.errors import InvalidFileError, MissingColumnsError

logger = logging.getLogger(__name__)

REQUIRED_PLAYER_DATAFRAME_COLUMNS = {
    # Basic Player Info
    PLAYER_UID, PLAYER_NAME, PLAYER_AGE, PLAYER_HEIGHT, PLAYER_WEIGHT, 
    PLAYER_NAT, PLAYER_PREFERRED_FOOT, PLAYER_POSITION, PLAYER_CLUB, 
    PLAYER_DIVISION, PLAYER_SALARY, PLAYER_TRANSFER_VALUE,

    # All Stats (General + Chalkboard)
    AT_APPS, YEL, XG, SAVES_90, TGLS_90, TCONC_90, TCONC, TGLS, STARTS, 
    SHUTOUTS, RED, PTS_GM, POM, PEN_SC, PEN_SC_R, PEN_SV_R, PEN_SV, PEN_FAC, 
    PEN_ATT, NP_XG_90, NP_XG, MINS_LST_GL, MINS_LST_CONC, MINS_G, MINS, 
    INTS_CONC, INTS_AV_RAT, INTS_AST, INTS_APPS, GLS_90, CONC_90, CONC, 
    GLS, GM_WON, GM_MISS, GM_LOST, GM_DRAW, GM_W_R, FLS, FLS_AGST, XG_90, 
    XG_OP, XA_90, XA, AV_RAT, MINS_AV_GL, AST, APPS, AT_LG_GLS, AT_GLS, 
    AER_A_90, AER_A, TCK_90, TCK_C, TCK_A, TCK_R, SHOT_90, SHOT_OT_R, 
    SHOT_OT_90, SHOT_OT, SHOT_OUT_BOX_90, BLK_SHOT_90, BLK_SHOT, SHOTS, 
    SV_T, SV_P, SV_H, SV_R, PR_PASSES_90, PR_PASSES, PRES_C_90, PRES_C, 
    PRES_A_90, PRES_A, POSS_WON_90, POSS_LOST_90, PS_C_90, PS_C, PS_A_90, 
    PS_A, PAS_R, OP_KP_90, OP_KP, OP_CRS_C_90, OP_CRS_C, OP_CRS_A_90, 
    OP_CRS_A, OP_CR_R, OFF, MST_GL, K_TCK_90, K_TCK, K_PS_90, K_PS, 
    K_HDRS_90, INT_90, INT, SPRINTS_90, HDR_R, HDRS_W_90, HDRS_W, HDRS_L_90, 
    GLS_OUT_BOX, FK_SHOT, XSV_R, XG_PV_90, XG_PV, XG_SHOT, DRB_90, DRB, 
    DIST_90, DIST, CRS_C_90, CRS_C, CRS_A_90, CRS_A, CONV_R, CLR_90, CLR, 
    CCC, CH_C_90, BLK_90, BLK, ASTS_90
}

RETURNED_PLAYER_DATAFRAME_COLUMNS = {
    # Basic Player Info
    PLAYER_UID, PLAYER_NAME, PLAYER_AGE, PLAYER_HEIGHT, PLAYER_WEIGHT, 
    PLAYER_NAT, PLAYER_PREFERRED_FOOT, PLAYER_POSITION, PLAYER_CLUB, 
    PLAYER_DIVISION, PLAYER_SALARY, PLAYER_TRANSFER_VALUE,

    

}


def extract_tables_from_html(file) -> list[pd.DataFrame]:
    """
    Extract all tables from HTML file.
    
    Args:
        file: File-like object containing HTML
        
    Returns:
        list[pd.DataFrame]: List of extracted tables
        
    Raises:
        InvalidFileError: If no tables found or file is invalid
    """
    try:
        content = file.read()        
        tables = pd.read_html(content)
        
        if not tables:
            raise InvalidFileError("No tables found in HTML file")
        
        logger.info(f"Extracted {len(tables)} table(s) from HTML")
        return tables
        
    except ValueError as e:
        raise InvalidFileError(f"Failed to parse HTML: {str(e)}")
    except Exception as e:
        raise InvalidFileError(f"Unexpected error reading file: {str(e)}")
    

def validate_and_extract_player_data(tables: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Validate and extract player data from tables.
    
    Args:
        tables: List of DataFrames extracted from HTML
        
    Returns:
        pd.DataFrame: Raw player data with required columns only
        
    Raises:
        MissingColumnsError: If required columns are missing
    """
    # Assume first table contains player data
    raw_df = tables[0]
    
    # Verify all required columns exist
    verify_columns(raw_df, REQUIRED_PLAYER_DATAFRAME_COLUMNS)
    # Extract only required columns
    df = raw_df[list(REQUIRED_PLAYER_DATAFRAME_COLUMNS)].copy()
    
    logger.info(f"Validated and extracted {len(df)} player records")
    return df


def process_player_html(file) -> Optional[pd.DataFrame]:
    """
    Complete pipeline to process player data from HTML file.
    
    Pipeline steps:
    1. Extract tables from HTML
    2. Validate and extract required columns
    3. Preprocess data (clean, transform, standardize)
    4. Add position encodings
    5. Calculate custom metrics
    6. Normalize to per-90 values
    
    Args:
        file: File-like object containing HTML exported from Football Manager with player data
        
    Returns:
        pd.DataFrame: Fully processed player dataframe, or None if processing fails
        
    Raises:
        InvalidFileError: If file format is invalid
        MissingColumnsError: If required columns are missing
        InvalidColumnValueError: If data values are in unexpected format
    """
    try:
        logger.info("Starting player data processing pipeline")
        
        # Step 1: Extract tables
        tables = extract_tables_from_html(file)
        
        # Step 2: Validate and extract
        df = validate_and_extract_player_data(tables)
        
        # Step 3-6: Process pipeline
        df = preprocess_player_dataframe(df)
        df = add_player_position_columns(df)
        df = add_custom_metrics(df)
        df = normalize_metrics(df)
        
        logger.info(f"Successfully processed {len(df)} players with {len(df.columns)} columns")
        return df
        
    except (MissingColumnsError, InvalidFileError) as e:
        logger.error(f"Processing failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during processing: {str(e)}", exc_info=True)
        raise InvalidFileError(f"Failed to process player data: {str(e)}")