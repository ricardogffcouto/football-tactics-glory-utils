import os
from dataclasses import dataclass

import pandas as pd

# Set the directory where the CSV files are stored
csv_directory = 'player_lists'

# Get a list of all CSV files in the directory
csv_files = [os.path.join(csv_directory, f) for f in os.listdir(csv_directory) if f.endswith('.csv')]

# Read each CSV file into a separate dataframe and store them in a list
dataframes = [pd.read_csv(file) for file in csv_files]

# Concatenate all dataframes in the list into a single dataframe
df = pd.concat(dataframes, ignore_index=True)

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

def skill_search(df, skill, skill_level):
    return df[((df['skill_1'] == skill) & (df['skill_1_level'] == skill_level)) | ((df['skill_2'] == skill) & (df['skill_2_level'] == skill_level))]

def pos_search(df, pos):
    return df[df['pos'].isin(pos)]

def attr_search(df, attr, value):
    return df[df[attr] >= value]


df = df[df['gift'] <= 5]
long_pass_df = skill_search(
    pos_search(
        df,
        ["RM"],
    ),
    Skill.LONG_PASS,
    2,
)
shortlist = [
    "24b00b31-96c9-40a4-b5d1-6c74c4918943",
    "0afa8292-1395-409a-9e17-f2131ca7a46f",
]

df = df[df["id"].isin(shortlist)]
df
