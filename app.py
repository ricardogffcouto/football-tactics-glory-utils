import streamlit as st
from constants import *
import io
import zipfile
import os
from utils import streamlit as st_utils

st.write('# Football Tactics and Glory')
st.write('## Scouting')

screenshots_file = st.file_uploader("Upload screenshots.zip", "zip")
if screenshots_file is not None:
    with io.BytesIO(screenshots_file.read()) as zip_stream:
        with zipfile.ZipFile(zip_stream, 'r') as zip_archive:
            st.write("Extracting files...")
            zip_archive.extractall(CURRENT_PATH)
            st.write("Files extracted successfully!")
            team_amount = len(os.listdir(SCREENSHOT_PATH))
            expected_time_seconds = st_utils.format_time(team_amount * 30)
            st.write(f"Expected time: {expected_time_seconds}")
            if st.button("Start!"):
                st_utils.nav_page("Parsing")




