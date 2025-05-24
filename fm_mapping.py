PLAYER_AGE                  = 'Age'
PLAYER_BEST_POSITION        = 'Best Pos'
PLAYER_CLUB                 = 'Club'
PLAYER_DIVISION             = 'Division'
PLAYER_HEIGHT               = 'Height'
PLAYER_NAME                 = 'Name'
PLAYER_NAT                  = 'Nat'
PLAYER_POSITION             = 'Position'
PLAYER_PREFERRED_FOOT       = 'Preferred Foot'
PLAYER_SALARY               = 'Salary'
PLAYER_TRANSFER_VALUE       = 'Transfer Value'
PLAYER_MAX_TRANSFER_VALUE   = 'Max Transfer Value'
PLAYER_UID                  = 'UID'
PLAYER_WEIGHT               = 'Weight'

AER_A_90                    = 'Aer A/90'
AST                         = 'Ast'
ASTS_90                     = 'Asts/90'
AV_RAT                      = 'Av Rat'
BLK_90                      = 'Blk/90'
CCC                         = 'CCC'
CCC_90                      = 'CC Chance/90'
CH_C_90                     = 'Ch C/90'
CLR_90                      = 'Clr/90'
CONV_R                      = 'Conv %'                          # goals per shot
CONV_OT_R                   = 'Conv oT %'                       # goals per shot on target
DEF_ACT                     = 'Def Act'                         # defensive actions
DEF_ACT_90                  = 'Def Act/90'                      # defensive actions per 90
DIST                        = 'Distance'
DIST_90                     = 'Dist/90'
DRB_90                      = 'Drb/90'
FA                          = 'FA'
FA_90                       = 'FA/90'
FLS                         = 'Fls'
FLS_90                      = 'Fls/90'
GL_MST                      = 'Gl Mst'
GL_MST_90                   = 'Gl Mst/90'
GLS                         = 'Gls'
GLS_90                      = 'Gls/90'
GLS_AST                     = 'Gls + Ast'
GLS_AST_90                  = 'Gls + Ast/90'
HDR_R                       = 'Hdr %'
HDRS_L_90                   = 'Hdrs L/90'
HDRS_W_90                   = 'Hdrs W/90'
INT                         = 'Itc'
INT_90                      = 'Int/90'
K_HDRS_90                   = 'K Hdrs/90'
K_TCK_90                    = 'K Tck/90'
MINS                        = 'Mins'
NP_G                        = 'NP-G'                           # non-penalty goals
NP_G_90                     = 'NP-G/90'
NP_G_XA                     = 'npxG + xAG'
NP_G_XA_90                  = 'npxG + xAG/90'
NP_XG                       = 'NP-xG'
NP_XG_90                    = 'NP-xG/90'
NP_XG_OP                    = 'npxG-OP'
NP_XG_OP_90                 = 'npxG-OP/90'
NP_XG_SHOT                  = 'npxG/Shot'
OFF                         = 'Off'
OFF_90                      = 'Off/90'
OP_CR_R                     = 'OP-Cr %'
OP_CRS_A_90                 = 'OP-Crs A/90'
OP_CRS_C_90                 = 'OP-Crs C/90'
OP_KP_90                    = 'OP-KP/90'
PAS_R                       = 'Pas %'
PEN_S                       = 'Pens S'
PENS                        = 'Pens'
PENS_R                      = 'Pen/R'
POSS_LOST_90                = 'Poss Lost/90'
POSS_NET_90                 = 'Poss Net/90'
POSS_WON_90                 = 'Poss Won/90'
PR_PASSES_90                = 'Pr passes/90'
PR_PASSES_R                 = 'Pr passes R'                     # ratio of passes that is "progressive"
PRES_A_90                   = 'Pres A/90'
PRES_C_90                   = 'Pres C/90'
PRES_R                      = 'Pres R'                          # pressure success rate
PS_A_90                     = 'Ps A/90'
PS_C_90                     = 'Ps C/90'
RED                         = 'Red'
RED_90                      = 'Red/90'
SHOT_R                      = 'Shot %'
SHOT_90                     = 'Shot/90'
SHT_90                      = 'ShT/90'                          # shots on target per 90
SPRINTS_90                  = 'Sprints/90'
TCK_A                       = 'Tck A'
TCK_A_90                    = 'Tck A/90'
TCK_W                       = 'Tck W'
TCK_R                       = 'Tck R'
TCK_90                      = 'Tck/90'
TCON_90                     = 'Tcon/90'
TGLS_90                     = 'Tgls/90'
XA                          = 'xA'
XA_90                       = 'xA/90'
XG                          = 'xG'
XG_90                       = 'xG/90'
XG_OP                       = 'xG-OP'
XG_OP_90                    = 'xG-OP/90'
YEL                         = 'Yel'
YEL_90                      = 'Yel/90'


PLAYER_BASE_INFO = (
    PLAYER_AGE,
    PLAYER_BEST_POSITION,
    PLAYER_CLUB,
    PLAYER_DIVISION,
    PLAYER_NAME,
    PLAYER_NAT,
    PLAYER_POSITION,
    PLAYER_PREFERRED_FOOT,
    PLAYER_SALARY,
    PLAYER_TRANSFER_VALUE,
    PLAYER_UID
)

PRESET_PERCENT_FIELDS = (SHOT_R, CONV_R, PAS_R, OP_CR_R, TCK_R, HDR_R)
PRESET_NUMERIC_FIELDS = (
    AER_A_90,
    AST,
    ASTS_90,
    AV_RAT,
    BLK_90,
    CCC,
    CH_C_90,
    CLR_90,
    CONV_R,
    DIST,
    DIST_90,
    DRB_90,
    FA,
    FLS,
    GL_MST,
    GLS,
    GLS_90,
    HDR_R,
    HDRS_L_90,
    HDRS_W_90,
    INT,
    INT_90,
    K_HDRS_90,
    K_TCK_90,
    MINS,
    NP_XG,
    NP_XG_90,
    OFF,
    OP_CR_R,
    OP_CRS_A_90,
    OP_CRS_C_90,
    OP_KP_90,
    PAS_R,
    PEN_S,
    PENS,
    PENS_R,
    POSS_LOST_90,
    POSS_WON_90,
    PR_PASSES_90,
    PRES_A_90,
    PRES_C_90,
    PS_A_90,
    PS_C_90,
    RED,
    SHOT_R,
    SHOT_90,
    SHT_90,
    SPRINTS_90,
    TCK_A,
    TCK_R,
    TCK_W,
    TCK_90,
    TCON_90,
    TGLS_90,
    XA,
    XA_90,
    XG,
    XG_90,
    XG_OP,
    YEL,
)

CUSTOM_FIELDS = (
    CCC_90,
    CONV_OT_R,
    DEF_ACT,
    DEF_ACT_90,
    FA_90,
    FLS_90,
    GLS_AST,
    GLS_AST_90,
    GL_MST_90,
    NP_G,
    NP_G_90,
    NP_G_XA,
    NP_G_XA_90,
    NP_XG_OP,
    NP_XG_OP_90,
    NP_XG_SHOT,
    OFF_90,
    POSS_NET_90,
    PR_PASSES_R,
    PRES_R,
    RED_90,
    TCK_A_90,
    XG_OP_90,
    YEL_90,
)