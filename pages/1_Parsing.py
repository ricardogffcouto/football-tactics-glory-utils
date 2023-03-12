import datetime

from parsers import TeamParser
import pandas as pd
import datetime
from constants import *
import os
from utils import streamlit as st_utils
import streamlit as st


STOP = False

def merge_player_lists(player_lists):
    # Create an empty list to store the DataFrames
    df_list = []

    # Loop over each CSV file in player_lists
    for file in player_lists:
        df = pd.read_csv(file)
        df_list.append(df)

    # Concatenate the DataFrames in the list
    merged_df = pd.concat(df_list, axis=0)

    filename = f'{PLAYER_LISTS_PATH}/player_list_{datetime.datetime.now()}.csv'

    # Save the resulting DataFrame to a new CSV file
    merged_df.to_csv(filename, index=False)

    return filename

def save_players(players):
    df = pd.DataFrame(players)
    if not os.path.exists(PLAYER_LISTS_PATH):
        os.mkdirs(PLAYER_LISTS_PATH)
    filename = f"{PLAYER_LISTS_PATH}/players_{datetime.datetime.now()}.csv"
    df.to_csv(filename, index=False)
    return filename

def get_last_team_id():
    csv_files = [f for f in os.listdir(PLAYER_LISTS_PATH) if f.startswith('player_list') and f.endswith('.csv')]
    file_times = [os.path.getctime(os.path.join(PLAYER_LISTS_PATH, f)) for f in csv_files]
    combined_list = list(zip(csv_files, file_times))
    sorted_list = sorted(combined_list, key=lambda x: x[1], reverse=True)
    last_player_list_filename = sorted_list[0][0]
    player_list = pd.read_csv(f"{PLAYER_LISTS_PATH}/{last_player_list_filename}")
    return player_list.tail(1)['team_id'].iloc[0]

def parse_teams(batch_size=1000, team_amount=None, resume=False):
    team_ids = os.listdir(SCREENSHOT_PATH)
    players = []
    player_lists = []

    teams_to_parse = team_ids
    if resume:
        last_team_id = get_last_team_id()
        teams_to_parse = team_ids[team_ids.index(last_team_id):]

    expected_time_seconds = st_utils.format_time(len(teams_to_parse) * 30)
    progress_bar = st.progress(0, text=f"Parsed teams: 0 / {len(teams_to_parse)}. Expected time: {expected_time_seconds}")

    for i, team_id in enumerate(teams_to_parse):
        team = TeamParser(team_id)
        players += team.parse_players()
        percentage_done = int((i+1)*100/len(teams_to_parse))
        expected_time_seconds = st_utils.format_time((len(teams_to_parse) - (i + 1)) * 30)
        progress_bar.progress(percentage_done, text=f"Parsed teams: {i} / {len(teams_to_parse)}. Expected time: {expected_time_seconds}")
        if len(players) > batch_size:
            player_lists.append(save_players(players))
            players = []
        if (team_amount and i >= team_amount) or STOP:
            player_lists.append(save_players(players))
            break

    player_list_filename = merge_player_lists(player_lists)
    st.write("Done!")
    st.download_button("Download player list", player_list_filename)

def stop():
    global STOP
    STOP = True

st.write('# Football Tactics and Glory')
st.write('## Scouting')
start_button = st.button("Start!")
resume_button = st.button("Resume!")
if start_button or resume_button:
    container = st.empty()
    stop_button = container.button('Stop', on_click=stop)
    parse_teams()
    if stop_button:
        stop_button.disabled = True
        stop_button.text = 'Writing player files...'
