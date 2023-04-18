import os
from dataclasses import dataclass

import pandas as pd
from easyocr import easyocr

ATTRIBUTES = ["acc", "pas", "df", "ctr"]

@dataclass
class Skill:
    LONG_PASS = "Long Pass"
    RAINBOW_FLICK = "Rainbow"
    CANNON_KICK = "Cannon Kick"
    SLIDE_TACKLE = "Slide Tackle"
    LAYOFF_PASS = "Layoff Pass"
    OLYMPIC_KICK = "Olympic"
    REACTION = "Reaction"
    INTERCEPTION = "Interception"
    NUTMEG = "Nutmeg"
    PLAYING_OUT = "Playing out"
    HEAD_PLAY = "Head Play"
    THROW_IN = "Throw In"
    STRONG_GOALKEEPER = "Strong Goalkeeper"

@dataclass
class Filter:
    def skill(self, df, skill, skill_min=1, skill_max=3):
        return df[((df['skill_1'] == skill) & (df['skill_1_level'] >= skill_min) & (df['skill_1_level'] <= skill_max)) | (
                    (df['skill_2'] == skill) & (df['skill_2_level'] >= skill_min) & (df['skill_2_level'] <= skill_max))]
    def is_in(self, df, attr, l):
        return df[df[attr].isin(l)]

    def min_max(self, df, attr, attr_min, attr_max):
        return df[(df[attr] >= attr_min) & (df[attr] <= attr_max)]

    def apply(self, df, search_json):
        for key in search_json:
            if key == 'pos':
                df = self.is_in(df, "pos", search_json['pos'])
            elif key == 'skills':
                for skill in search_json['skills']:
                    df = self.skill(df, skill['name'], skill['min'], skill['max'])
            else:
                df = self.min_max(df, key, search_json[key][0], search_json[key][1])
        return df

def load_data(data_id):
    # Set the directory where the CSV files are stored
    csv_directory = f'player_lists/{data_id}'

    # Get a list of all CSV files in the directory
    csv_files = [os.path.join(csv_directory, f) for f in os.listdir(csv_directory) if f.endswith('.csv')]

    # Read each CSV file into a separate dataframe and store them in a list
    dataframes = [pd.read_csv(file) for file in csv_files]

    # Concatenate all dataframes in the list into a single dataframe
    df = pd.concat(dataframes, ignore_index=True)

    df = df[df['is_filtered'] == False]

    for attr in ATTRIBUTES:
        df[f"{attr}_skew"] = (df[attr] / df[ATTRIBUTES].mean(axis=1)).round(1)

    # Max attr skew
    df["max_attr_skew"] = (df[ATTRIBUTES].max(axis=1) / df[ATTRIBUTES].mean(axis=1)).round(1)

    return df

def view_dataframe(df):
    int_columns = ATTRIBUTES + ["gift", "age", "skill_1_level", "skill_2_level"]
    df[int_columns] = df[int_columns].fillna(0).astype(int)

    SKILL_COLUMNS = ["skill_1", "skill_1_level", "skill_2", "skill_2_level"]

    view_columns = ["id", "pos", "age", "gift"] + ATTRIBUTES + SKILL_COLUMNS + ["max_attr_skew"]

    return df[view_columns]

long_pass_json = {
    "skills": [{
            "name": Skill.LONG_PASS,
            "min": 3,
            "max": 3,
    }],
    "pos": ["RM", "LM", "RD", "LD"]
}

long_pass_json_2 = {
    "skills": [{
            "name": Skill.LONG_PASS,
            "min": 3,
            "max": 3,
    }],
    "acc": [1, 100],
    "pas": [1, 100],
    "df": [1, 100],
    "ctr": [1, 100],
    "age": [16, 30],
    "pos": ["M", "CM", "MF"]
}


cannon_goals_json = {
    "skills": [{
        "name": Skill.CANNON_KICK,
        "min": 3,
        "max": 3,
    }],
    "pos": ["M", "MF", "FW"]
}

am_acc_json = {
    "acc": [100, 300],
    "pos": ["D", "M", "F", "AM"]
}

rainbow_goals_json = {
    "skills": [{
        "name": Skill.RAINBOW_FLICK,
        "min": 3,
        "max": 3,
    }],
    "pos": ["M", "MF", "FW"]
}

head_goals_json = {
    "skills": [{
        "name": Skill.HEAD_PLAY,
        "min": 3,
        "max": 3,
    }],
    "gift": [1, 2],
    "pos": ["CF"]
}

dm_slide_tackle_json = {
    "skills": [{
        "name": Skill.SLIDE_TACKLE,
        "min": 3,
        "max": 3,
    }],
    "gift": [1, 2],
    "pos": ["D", "M", "DM"]
}

gk_skills_json = {
    "skills": [{
        "name": Skill.STRONG_GOALKEEPER,
        "min": 1,
        "max": 3,
    }, {
        "name": Skill.PLAYING_OUT,
        "min": 1,
        "max": 3,
    }],
}

cd_json = {
    "pos": ["CD"],
    "df": [120, 300],
    "skills": [{
        "name": Skill.HEAD_PLAY,
        "min": 1,
        "max": 3,
    }]
}


rf_lf_cannon_json = {
    "pos": ["LF"],
    "ctr": [100, 300],
    "skills": [{
        "name": Skill.CANNON_KICK,
        "min": 2,
        "max": 3,
    }]
}

slide_long_json = {
    "skills": [{
        "name": Skill.SLIDE_TACKLE,
        "min": 1,
        "max": 3,
    }, {
        "name": Skill.LAYOFF_PASS,
        "min": 1,
        "max": 3,
    }],
}

mf_slide_json = {
    "skills": [{
        "name": Skill.SLIDE_TACKLE,
        "min": 3,
        "max": 3,
    }],
    "pos": ["M", "MF", "FW"]
}

slide_cannon_json = {
    "skills": [{
        "name": Skill.SLIDE_TACKLE,
        "min": 2,
        "max": 3,
    }, {
        "name": Skill.CANNON_KICK,
        "min": 1,
        "max": 3,
    }],
    "pos": ["M", "MF", "FW"]
}

am_acc_json = {
    "acc": [100, 300],
    "pos": ["AM"],
}

cf_acc_json = {
    "pos": ["CF"],
    "acc": [150, 300],
}

df_df_json = {
    "pos": ["D", "DF", "CD"],
    "df": [150, 300],
}

rf_lf_ctr_acc_json = {
    "pos": ["LF"],
    "ctr": [140, 300],
    "acc": [80, 300],
}

current_filter = gk_skills_json

data_id = "2032-07"

df = load_data(data_id)
filtered_df = Filter().apply(df, current_filter)

view_df = view_dataframe(filtered_df)

shortlist = [
    "f2f19df7-da29-4943-9c47-5495fc1ea9b4",
]

shortlist_df = df[df["id"].isin(shortlist)]

run_ocr = True
if run_ocr:
    reader = easyocr.Reader(['en'])

    for player in shortlist_df.to_dict(orient="records"):
        team_folder = f"screenshots/{data_id}/screenshots/{player['team_id']}"
        team_name = reader.readtext(f"{team_folder}/team_name.png")
        if len(team_name):
            team_name = team_name[0][1]
        else:
            team_name = None
        shortlist_df.loc[shortlist_df["id"] == player["id"], "team_name"] = team_name
        shortlist_df["country"] = shortlist_df["team_name"].str.split("(").str[1].str.replace(")", "")

shortlist_df