import shutil
import streamlit as st
import pandas as pd
import datetime
import os
from utils import streamlit as st_utils
from parsers import TeamParser
from constants import SCREENSHOT_PATH

SESSION_ID = st.session_state["session_id"]
PLAYER_LISTS_SESSION_PATH = st_utils.get_player_lists_path(SESSION_ID)
SCREENSHOTS_SESSION_PATH = st_utils.get_screenshots_path(SESSION_ID)

def merge_player_lists(player_lists):
    # Create an empty list to store the DataFrames
    df_list = []

    # Loop over each CSV file in player_lists
    for file in player_lists:
        df = pd.read_csv(file)
        df_list.append(df)

    # Concatenate the DataFrames in the list
    merged_df = pd.concat(df_list, axis=0)

    # Save the resulting DataFrame to a new CSV file
    return merged_df.to_csv(index=False).encode("utf-8")

def save_players(players):
    df = pd.DataFrame(players)
    if not os.path.exists(PLAYER_LISTS_SESSION_PATH):
        os.makedirs(PLAYER_LISTS_SESSION_PATH)
    filename = f"{PLAYER_LISTS_SESSION_PATH}/players_{datetime.datetime.now()}.csv"
    df.to_csv(filename, index=False)
    return filename

def get_last_team_id():
    csv_files = [f for f in os.listdir(PLAYER_LISTS_SESSION_PATH) if f.startswith('players_') and f.endswith('.csv')]
    file_times = [os.path.getctime(os.path.join(PLAYER_LISTS_SESSION_PATH, f)) for f in csv_files]
    combined_list = list(zip(csv_files, file_times))
    sorted_list = sorted(combined_list, key=lambda x: x[1], reverse=True)
    last_player_list_filename = sorted_list[0][0]
    player_list = pd.read_csv(f"{PLAYER_LISTS_SESSION_PATH}/{last_player_list_filename}")
    return player_list.tail(1)['team_id'].iloc[0]

def parse_teams(batch_size=20, team_amount=1, resume=False):
    team_ids = os.listdir(SCREENSHOTS_SESSION_PATH)
    players = []
    player_lists = []

    teams_to_parse = team_ids
    if resume:
        last_team_id = get_last_team_id()
        teams_to_parse = team_ids[team_ids.index(last_team_id):]

    expected_time_seconds = st_utils.format_time(len(teams_to_parse) * 30)
    progress_bar = st.progress(0, text=f"Parsed teams: 0 / {len(teams_to_parse)}. Expected time: {expected_time_seconds}")

    for i, team_id in enumerate(teams_to_parse):
        team = TeamParser(
            team_id=team_id,
            session_id=SESSION_ID
        )
        players += team.parse_players()
        percentage_done = int((i+1)*100/len(teams_to_parse))
        expected_time_seconds = st_utils.format_time((len(teams_to_parse) - (i + 1)) * 30)

        if (team_amount and i + 1 >= team_amount):
            player_lists.append(save_players(players))
            break

        if len(players) > batch_size:
            player_lists.append(save_players(players))
            players = []

        progress_bar.progress(percentage_done,
                                  text=f"Parsed teams: {i + 1} / {len(teams_to_parse)}. Expected time: {expected_time_seconds}")

    player_list = merge_player_lists(player_lists)
    st.write("Done!")
    st.download_button(
        label="Download player list",
        data=player_list,
        file_name=f'player_list_{SESSION_ID}.csv',
        mime='text/csv',
    )
    shutil.rmtree(f"{SCREENSHOT_PATH}/{SESSION_ID}")


st.write('# Football Tactics and Glory')
st.write('## Scouting')
st.write(f"Session ID: {SESSION_ID}")

st.button("Start!", on_click=parse_teams)