import uuid

import streamlit as st
from constants import *
import io
import zipfile
import os
from utils import streamlit as st_utils

st.write('# Football Tactics and Glory')
st.write('## Scouting')

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

SESSION_ID = st.session_state.session_id

st.write(f"Session ID: {SESSION_ID}")

screenshots_file = st.file_uploader("Upload screenshots.zip", "zip")
if screenshots_file is not None:
    with io.BytesIO(screenshots_file.read()) as zip_stream:
        with zipfile.ZipFile(zip_stream, 'r') as zip_archive:
            st.write("Extracting files...")
            st.write("This process may take up to a minute.")
            zip_archive.extractall(f"{SCREENSHOT_PATH}/{SESSION_ID}")
            st.write("Files extracted successfully!")
            team_amount = len(os.listdir(st_utils.get_screenshots_path(SESSION_ID)))
            expected_time_seconds = st_utils.format_time(team_amount * 30)
            st.write(f"Expected time: {expected_time_seconds}")
            st.write("You can go to the Parsing page")



