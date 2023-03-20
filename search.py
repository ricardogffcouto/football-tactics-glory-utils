import os
from dataclasses import dataclass

import pandas as pd

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
    PLAYING_OUT = "Playing Out"
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

def load_data():
    # Set the directory where the CSV files are stored
    csv_directory = 'player_lists/388df3f9-b2ae-4aa6-8a39-2101f0005e07'

    # Get a list of all CSV files in the directory
    csv_files = [os.path.join(csv_directory, f) for f in os.listdir(csv_directory) if f.endswith('.csv')]

    # Read each CSV file into a separate dataframe and store them in a list
    dataframes = [pd.read_csv(file) for file in csv_files]

    # Concatenate all dataframes in the list into a single dataframe
    df = pd.concat(dataframes, ignore_index=True)

    # Attribute skewedness
    for attr in ATTRIBUTES:
        df[f"{attr}_skew"] = df[attr] / df[ATTRIBUTES].mean(axis=1)

    # Max attr skew
    df["max_attr_skew"] = df[ATTRIBUTES].max(axis=1) / df[ATTRIBUTES].mean(axis=1)

    return df

long_pass_json = {
    "skills": [{
            "name": Skill.LONG_PASS,
            "min": 2,
            "max": 3,
    }],
    "gift": [1, 2],
    "pos": ["RM", "LM", "RD", "LD"]
}

cannon_goals_json = {
    "skills": [{
        "name": Skill.CANNON_KICK,
        "min": 3,
        "max": 3,
    }],
    "gift": [1, 2],
    "pos": ["M", "MF", "FW"]
}

rainbow_goals_json = {
    "skills": [{
        "name": Skill.RAINBOW_FLICK,
        "min": 3,
        "max": 3,
    }],
    "gift": [1, 2],
    "pos": ["M", "MF", "FW"]
}

df = load_data()
df = Filter().apply(df, rainbow_goals_json)
df
