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
APPS                        = 'Apps'                            # appearances
AST                         = 'Ast'
ASTS_90                     = 'Asts/90'
ATT_MID_WINGER              = 'Att-Mid/Winger'
AV_RAT                      = 'Av Rat'
BLK_90                      = 'Blk/90'
BLK_PAS_90                  = 'Pass Blckd/90'                   # blocked passes per 90
BLK_SHT_90                  = 'Shts Blckd/90'
CCC                         = 'CCC'
CCC_90                      = 'CC Chance/90'
CENTERBACK                  = 'Centerback'
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
FORWARD                     = 'Forward'
FULLBACK                    = 'Fullback'
GL_MST                      = 'Gl Mst'
GL_MST_90                   = 'Gl Mst/90'
GLS                         = 'Gls'
GLS_90                      = 'Gls/90'
GLS_AST                     = 'Gls + Ast'
GLS_AST_90                  = 'Gls + Ast/90'
GOALKEEPER                  = 'Goalkeeper'
HDR_R                       = 'Hdr %'
HDRS_L_90                   = 'Hdrs L/90'
HDRS_W_90                   = 'Hdrs W/90'
INT                         = 'Itc'
INT_90                      = 'Int/90'
K_HDRS_90                   = 'K Hdrs/90'
K_TCK_90                    = 'K Tck/90'
MIDFIELDER                  = 'Midfielder'
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
PEN_S_90                    = 'Pens S/90'                       # penalty kicks scored per 90
PENS                        = 'Pens'
PENS_90                     = 'Pens/90'                         # penalty kicks attempted per 90
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
TCK_INT                     = 'Tck + Int'                       # tackles won + interceptions
TCK_INT_90                  = 'Tck + Int/90'                    # tackles won + interceptions per 90
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

PRESET_PERCENT_FIELDS = (SHOT_R, CONV_R, PAS_R, OP_CR_R, TCK_R, HDR_R, PENS_R)
PRESET_NUMERIC_FIELDS = (
    AER_A_90,
    AST,
    ASTS_90,
    AV_RAT,
    BLK_90,
    BLK_SHT_90,
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

PER90_METRICS_READABLE_NAME_MAPPING = {
    AER_A_90:           ('Aerials Attempted', 'Aerial Duels\nAttempted'),
    ASTS_90:            ('Assists', 'Assists'),
    BLK_90:             ('Blocks', 'Blocks'),
    BLK_PAS_90:         ('Passes Blocked', 'Passes\nBlocked'),
    BLK_SHT_90:         ('Shots Blocked', 'Shots\nBlocked'),
    CH_C_90:            ('Chances Created', 'Chances\nCreated'),
    CLR_90:             ('Clearances', 'Clearances'),
    CONV_OT_R:          ('Goals/Shot on Target', 'Goals/Shot OT'),
    CONV_R:             ('Goals/Shot', 'Goals/Shot'),
    DEF_ACT_90:         ('Defensive Actions', 'Defensive\nActions'),
    DIST_90:            ('Distance Covered', 'Distance\nCovered'),
    DRB_90:             ('Dribbles', 'Dribbles'),
    FA_90:              ('Fouls Drawn', 'Fouls\nDrawn'),
    FLS_90:             ('Fouls Committed', 'Fouls\nCommitted'),
    GLS_90:             ('Goals', 'Goals'),
    GLS_AST_90:         ('Goals + Assists', 'Goals + Assists'),
    HDRS_L_90:          ('Aerials Lost', 'Aerials\nLost'),
    HDRS_W_90:          ('Aerials Won', 'Aerials\nWon'),
    HDR_R:              ('% Aerials Won', '% Aerials Won'),
    INT_90:             ('Interceptions', 'Interceptions'),
    K_HDRS_90:          ('Key Headers', 'Key Headers'),
    K_TCK_90:           ('Key Tackles', 'Key Tackles'),
    NP_G_90:            ('Non-Penalty Goals', 'Non-Penalty\nGoals'),
    NP_G_XA_90:         ('npxG + xA', 'npxG + xA'),
    NP_XG_90:           ('npxG: Non-Penalty XG', 'Non-Penalty XG'),
    NP_XG_OP_90:        ('Non-Penalty Goals - npxG', 'npxG\nOverperformance'),
    NP_XG_SHOT:         ('npxG/Shot', 'npxG/Shot'),
    OFF_90:             ('Offsides', 'Offsides'),
    OP_CRS_A_90:        ('Open-play Crosses Attempted', 'Open-play\nCrosses\nAttempted'),
    OP_CRS_C_90:        ('Open-play Crosses Completed', 'Open-play\nCrosses\nCompleted'),
    OP_CR_R:            ('Open-play Crosses %', 'Open-play\nCrosses %'),
    OP_KP_90:           ('Open-play Key Passes', 'Open-play\nKey Passes'),
    PAS_R:              ('Pass Completion %', 'Pass\nCompletion %'),
    PEN_S_90:           ('Penalty Kicks Made', 'Penalty Kicks\nMade'),
    PENS_90:            ('Penalty Kicks Attempted', 'Penalty Kicks\nAttempted'),
    PENS_R:             ('Penalty Kicks %', 'Penalty Kicks %'),
    POSS_LOST_90:       ('Possession Lost', 'Possession\nLost'),
    POSS_NET_90:        ('Net Possession Gain', 'Possession\nNet'),
    POSS_WON_90:        ('Possession Won', 'Possession\nWon'),
    PR_PASSES_90:       ('Progressive Passes', 'Progressive\nPasses'),
    PR_PASSES_R:        ('Progressive Passes %', 'Progressive\nPasses %'),
    PRES_A_90:          ('Pressures Applied', 'Pressures\nApplied'),
    PRES_C_90:          ('Pressures Completed', 'Pressures\nCompleted'),
    PRES_R:             ('Pressure Success %', 'Pressure\nSuccess %'),
    PS_A_90:            ('Passes Attempted', 'Passes\nAttempted'),
    PS_C_90:            ('Passes Completed', 'Passes\nCompleted'),
    RED_90:             ('Red Cards', 'Red Cards'),
    SHOT_90:            ('Shots', 'Shots'),
    SHOT_R:             ('Shots On Target %', 'Shots\nOn Target %'),
    SHT_90:             ('Shots On Target', 'Shots\nOn Target'),
    SPRINTS_90:         ('Sprints', 'Sprints'),
    TCK_90:             ('Tackles Won', 'Tackles Won'),
    TCK_A_90:           ('Tackles', 'Tackles'),
    TCK_INT_90:         ('Tkl + Int', 'Tkl + Int'),
    TCK_R:              ('Tackle Success %', 'Tackle Success %'),
    XA_90:              ('xA: Expected Assists', 'Expected\nAssists'),
    XG_90:              ('xG: Expected Goals', 'xG'),
    XG_OP_90:           ('Goals - xG', 'xG\nOverperformance'),
    YEL_90:             ('Yellow Cards', 'Yellow Cards'),
}

PER90_METRICS_PIZZA_DISPLAY = {
    GLS_90:           {'type': 'att', 'display': 'Goals'},
    XG_90:            {'type': 'att', 'display': 'xG'},
    NP_XG_90:         {'type': 'att', 'display': 'Non-penalty\nxG'},
    SHOT_90:          {'type': 'att', 'display': 'Shots'},
    SHOT_R:           {'type': 'att', 'display': 'Shot\nOn Target %'},
    CONV_R:           {'type': 'att', 'display': 'Conversion %'},
    XG_OP_90:         {'type': 'att', 'display': 'xG\nOverperformance'},

    ASTS_90:          {'type': 'att', 'display': 'Assists'},
    XA_90:            {'type': 'att', 'display': 'Expected\nAssists'},
    PS_A_90:          {'type': 'pos', 'display': 'Passes\nAttempted'},
    PAS_R:            {'type': 'pos', 'display': 'Pass\nCompletion %'},
    PS_C_90:          {'type': 'pos', 'display': 'Passes\nCompleted'},
    PR_PASSES_90:     {'type': 'pos', 'display': 'Progressive\nPasses'},
    PR_PASSES_R:      {'type': 'pos', 'display': 'Progressive\nPasses %'},
    OP_KP_90:         {'type': 'att', 'display': 'Open-play\nKey Passes'},
    OP_CRS_A_90:      {'type': 'att', 'display': 'Open-play\nCrosses\nAttempted'},
    OP_CR_R:          {'type': 'att', 'display': 'Open-play\nCross %'},
    OP_CRS_C_90:      {'type': 'att', 'display': 'Open-play\nCrosses\nCompleted'},
    CH_C_90:          {'type': 'att', 'display': 'Chances\nCreated'},
    DRB_90:           {'type': 'pos', 'display': 'Dribbles\nCompleted'},
    POSS_WON_90:      {'type': 'pos', 'display': 'Possession\nWon'},
    POSS_LOST_90:     {'type': 'pos', 'display': 'Possession\nLost'},
    POSS_NET_90:      {'type': 'pos', 'display': 'Possession\nNet'},
    FA_90:            {'type': 'pos', 'display': 'Fouls Against'},

    TCK_90:           {'type': 'def', 'display': 'Tackles Won'},
    TCK_R:            {'type': 'def', 'display': 'Tackle Won %'},
    K_TCK_90:         {'type': 'def', 'display': 'Key Tackles'},
    TCK_A_90:         {'type': 'def', 'display': 'Tackles\nAttempted'},
    BLK_90:           {'type': 'def', 'display': 'Blocks'},
    INT_90:           {'type': 'def', 'display': 'Interceptions'},
    CLR_90:           {'type': 'def', 'display': 'Clearances'},
    DEF_ACT_90:       {'type': 'def', 'display': 'Defensive\nActions'},
    AER_A_90:         {'type': 'def', 'display': 'Aerial Duels\nAttempted'},
    HDR_R:            {'type': 'def', 'display': 'Headers\nWon %'},
    HDRS_W_90:        {'type': 'def', 'display': 'Headers\nWon'},
    HDRS_L_90:        {'type': 'def', 'display': 'Headers\nLost'},
    K_HDRS_90:        {'type': 'def', 'display': 'Key Headers'},
    PRES_A_90:        {'type': 'def', 'display': 'Pressures\nAttempted'},
    PRES_C_90:        {'type': 'def', 'display': 'Pressures\nCompleted'},
    PRES_R:           {'type': 'def', 'display': 'Pressures\n Completed %'},
    SPRINTS_90:       {'type': 'def', 'display': 'High-intensity\nSprints'},
    DIST_90:          {'type': 'def', 'display': 'Distance\nCovered'},
    FLS_90:           {'type': 'def', 'display': 'Fouls Made'},
}

PER90_PERCENTILE_STANDARD_STATS = (
    GLS_90,
    ASTS_90,
    GLS_AST_90,
    NP_G_90,
    PEN_S_90,
    PENS_90,
    YEL_90,
    RED_90,
    XG_90,
    NP_XG_90,
    XA_90,
    NP_G_XA_90,
    PR_PASSES_90,
)

PER90_PERCENTILE_SHOOTING_STATS = (
    GLS_90,
    SHOT_90,
    SHT_90,
    SHOT_R,
    CONV_R,
    CONV_OT_R,
    PEN_S_90,
    PENS_90,
    PENS_R,
    XG_90,
    NP_XG_90,
    NP_XG_SHOT,
    XG_OP_90,
    NP_XG_OP_90,
)

PER90_PERCENTILE_PASSING_STATS = (
    PS_C_90,
    PS_A_90,
    PAS_R,
    ASTS_90,
    XA_90,
    OP_KP_90,
    CH_C_90,
    OP_CRS_C_90,
    OP_CRS_A_90,
    OP_CR_R,
    PR_PASSES_90,
)

PER90_PERCENTILE_DEFENDING_STATS = (
    TCK_A_90,
    TCK_90,
    TCK_R,
    K_TCK_90,
    BLK_90,
    BLK_SHT_90,
    BLK_PAS_90,
    INT_90,
    TCK_INT_90,
    CLR_90,
    PRES_A_90,
    PRES_C_90,
    PRES_R,
)

PER90_PERCENTILE_POSSESSION_STATS = (
    DRB_90,
    POSS_WON_90,
    POSS_LOST_90,
    POSS_NET_90,
)

PER90_PERCENTILE_MISC_STATS = (
    YEL_90,
    RED_90,
    FLS_90,
    FA_90,
    OFF_90,
    DIST_90,
    SPRINTS_90,
    AER_A_90,
    HDRS_W_90,
    HDRS_L_90,
    HDR_R,
    K_HDRS_90,
)

PER90_OTHER_STATS = (
    PR_PASSES_R,
    DEF_ACT_90,
)

INVERTED_PERCENTILE_FIELDS = (
    YEL_90, RED_90, POSS_LOST_90, FLS_90, OFF_90, HDRS_L_90,
)

POSITION_GROUPS = (
    CENTERBACK, FULLBACK, MIDFIELDER, ATT_MID_WINGER, FORWARD
)
