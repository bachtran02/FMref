import pandas as pd

from player_preprocessing_service import preprocess_player_dataframe, add_player_position_columns
from utils import verify_columns

from ..constants import *
from ..errors.errors import InvalidFileError, MissingColumnsError

REQUIRED_PLAYER_DATAFRAME_COLUMNS = {
    # Basic Player Info
    PLAYER_UID, PLAYER_NAME, PLAYER_AGE, PLAYER_HEIGHT, PLAYER_WEIGHT, PLAYER_NAT, PLAYER_PREFERRED_FOOT,
    PLAYER_POSITION, PLAYER_CLUB, PLAYER_DIVISION, PLAYER_SALARY, PLAYER_TRANSFER_VALUE,

    # All Stats (General + Chalkboard)
    AT_APPS, YEL, XG, SAVES_90, TGLS_90, TCONC_90, TCONC, TGLS, STARTS, SHUTOUTS, RED, PTS_GM, POM,
    PEN_SC_R, PEN_SV_R, PEN_SV, PEN_FAC, PEN_ATT, NP_XG_90, NP_XG, MINS_LST_GL, MINS_LST_CONC, MINS_G,
    MINS, INTS_CONC, INTS_AV_RAT, INTS_AST, INTS_APPS, GLS_90, CONC_90, CONC, GLS, GM_WON, GM_MISS,
    GM_LOST, GM_DRAW, GM_W_R, FLS, FLS_AGST, XG_90, XG_OP, XA_90, XA, AV_RAT, MINS_AV_GL, AST, APPS,
    AT_LG_GLS, AT_GLS, AER_A_90, AER_A, TCK_90, TCK_C, TCK_A, TCK_R, SHOT_90, SHOT_OT_R, SHOT_OT_90,
    SHOT_OT, SHOT_OUT_BOX_90, BLK_SHOT_90, BLK_SHOT, SHOTS, SV_T, SV_P, SV_H, SV_R, PR_PASSES_90,
    PR_PASSES, PRES_C_90, PRES_C, PRES_A_90, PRES_A, POSS_WON_90, POSS_LOST_90, PS_C_90, PS_C, PS_A_90,
    PS_A, PAS_R, OP_KP_90, OP_KP, OP_CRS_C_90, OP_CRS_C, OP_CRS_A_90, OP_CRS_A, OP_CR_R, OFF, MST_GL,
    K_TCK_90, K_TCK, K_PS_90, K_PS, K_HDRS_90, INT_90, INT, SPRINTS_90, HDR_R, HDRS_W_90, HDRS_W,
    HDRS_L_90, GLS_OUT_BOX, FK_SHOT, XSV_R, XG_PV_90, XG_PV, XG_SHOT, DRB_90, DRB, DIST_90, DIST,
    CRS_C_90, CRS_C, CRS_A_90, CRS_A, CONV_R, CLR_90, CLR, CCC, CH_C_90, BLK_90, BLK, ASTS_90
}


def process_player_html(file):
    
    try:
        tables = pd.read_html(file.read())
        if not tables:
            raise InvalidFileError("No tables found in HTML file")

        raw_df = tables[0]
        verify_columns(raw_df, REQUIRED_PLAYER_DATAFRAME_COLUMNS)

        # extract only required columns
        df = raw_df[list(REQUIRED_PLAYER_DATAFRAME_COLUMNS)].copy()
        df = preprocess_player_dataframe(df)
        df = add_player_position_columns(df)

        # Return only the required columns
        return None

    except (MissingColumnsError, InvalidFileError) as e:
        raise e
