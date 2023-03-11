DEBUG = False
#DEBUG = True

SCREENSHOT_PATH = "screenshots"
SKILLS_MODEL_FILE = "models/skills.h5"
SKILL_LEVEL_MODEL_FILE = "models/skill_level.h5"

TARGET_SIZE = (224, 224)

# PLAYER COORDINATES
PLAYERS_TABLE = {
    "X1": 305,
    "X2": 955,
    "Y1": 230,
    "Y2": 952,
    "INITIAL_ATTRIBUTE_X": 290,
    "ATTRIBUTE_W": 42,
    "SKILL_W": 55,
    "SK_LVL_Y": 25,
    "SK_LVL_X": 40,
    "SK_LVL_W": 14,
    "SK_LVL_H": 14,
    "INITIAL_X": 305,
    "FIRST_PLAYER_Y": 232,
    "PLAYER_H": 40,
    "PLAYER_GAP": 2,
    "GIFT_H": 20,
    "STAR_W": 10,
}

SKILL_POT = {
    "X1": 2,
    "X2": 18,
    "Y1": 0,
    "Y2": 15,
}

SKILL_LEVEL = {
    "X1": 38,
    "X2": 54,
    "Y1": 24,
    "Y2": 40,
}

MAX_GIFT = 5

PLAYER_COORDINATES = {
    'pos': 0,
    'pos_img': 50,
    'name': 85,
    'gift': 235,
    'acc': PLAYERS_TABLE["INITIAL_ATTRIBUTE_X"],
    'pas': PLAYERS_TABLE["INITIAL_ATTRIBUTE_X"] + PLAYERS_TABLE["ATTRIBUTE_W"],
    'df': PLAYERS_TABLE["INITIAL_ATTRIBUTE_X"] + PLAYERS_TABLE["ATTRIBUTE_W"] * 2,
    'ctr': PLAYERS_TABLE["INITIAL_ATTRIBUTE_X"] + PLAYERS_TABLE["ATTRIBUTE_W"] * 3,
    'lvl': PLAYERS_TABLE["INITIAL_ATTRIBUTE_X"] + PLAYERS_TABLE["ATTRIBUTE_W"] * 4,
    'age': PLAYERS_TABLE["INITIAL_ATTRIBUTE_X"] + PLAYERS_TABLE["ATTRIBUTE_W"] * 5,
    'skill_1': PLAYERS_TABLE["INITIAL_ATTRIBUTE_X"] + PLAYERS_TABLE["ATTRIBUTE_W"] * 6,
    'skill_2': PLAYERS_TABLE["INITIAL_ATTRIBUTE_X"] + PLAYERS_TABLE["ATTRIBUTE_W"] * 6 + PLAYERS_TABLE["SKILL_W"],
    'end': PLAYERS_TABLE["INITIAL_ATTRIBUTE_X"] + PLAYERS_TABLE["ATTRIBUTE_W"] * 6 + PLAYERS_TABLE["SKILL_W"] * 2
}

SPLIT_PLAYER_KEYS = {
    'gift': ['gift', 'info'],
    'skill_1': ['skill_1', 'skill_1_level'],
    'skill_2': ['skill_2', 'skill_2_level'],
}

PLAYER_PRICE = {
    "X1": 820,
    "X2": 1120,
    "Y1": 525,
    "Y2": 555,
}

PLAYERS_IN_TEAM_INFO = {
    "X1": 955,
    "X2": 1010,
    "Y1": 625,
    "Y2": 660,
}

ACHIEVEMENTS_BTN = {
    "X": 1470,
    "Y": 155,
}

PLAYERS_PER_LIST = 17

ELEMENTS_PER_TABLE = PLAYERS_PER_LIST

TEAM_SCREEN = {
    "X1": PLAYERS_TABLE["X1"],
    "X2": 1130,
    "Y1": 0,
    "Y2": PLAYERS_TABLE["Y2"],
}

TEAM_SCREEN_TOP_INFO = {
    "X1": 270,
    "X2": 1130,
    "Y1": 0,
    "Y2": 130,
}

TEAM_NAME = {
    "X1": 685,
    "X2": TEAM_SCREEN_TOP_INFO["X2"],
    "Y1": 45,
    "Y2": 85,
}

POSITIONS = [
    "?", "GK", "SW", "LD", "CD", "RD", "DM", "LM", "CM", "RM", "AM", "LW", "CF", "RW", "G", "D", "M", "A", "DF", "MF", "FW"
]

SKILLS = [
    "Rainbow",
    "Nutmeg",
    "Cannon Kick",
    "Slide Tackle",
    "Long Pass",
    "Layoff Pass",
    "Olympic Kick",
    "Reaction",
    "Interception",
    "Strong Goalkeeper",
    "Playing out",
    "Head Play",
    "Throw in",
    "None",
]

TABLE_X = 600
TABLE_INITIAL_Y = 250
TABLE_18_Y = 948
TABLE_H = 42
BUY_BTN_X = 1550
BTN_X = 1320
BTN_Y = 1040
SCROLL_X = 288
SCROLL_Y1 = 450
SCROLL_Y2 = 880

DIVISION_INITIAL_X = 400
DIVISION_Y = 150
DIVISION_W = 270

DIVISION_TEAMS_FULL = [8, 12, 14, 16, 18]
DIVISION_TEAMS_PREMIER = [18]

