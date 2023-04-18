import streamlit as st
import time
from screenshot_managers import FullScreenshotManager
from utils import streamlit as st_utils
import logging

# Create StreamHandler
handler = logging.StreamHandler()

# Add StreamHandler to root logger
logging.getLogger().addHandler(handler)


st.session_state.session_id = st.text_input("Session ID")
SESSION_ID = st.session_state.get("session_id", None)
SCREENSHOTS_SESSION_PATH = st_utils.get_screenshots_path(SESSION_ID)

def start_screenshots():
    st.write("Starting... 3 seconds...")
    time.sleep(3)
    manager = FullScreenshotManager(
        screenshots_id=SESSION_ID,
        country_amount=st.session_state.country_amount,
        current_country_rank=st.session_state.your_country_rank,
    )
    manager.save()


st_utils.header('Player Loading')
st.write(SESSION_ID)
st.number_input("Countries in Continent", value=1, min_value=1, max_value=50, step=1, key="country_amount")
st.number_input("Your Country Rank", value=1, min_value=1, max_value=50, step=1, key="your_country_rank")
expected_time_seconds = st.session_state.get("country_amount", 1) * 18 * 2 + (8 + 12 + 14 + 16) * 2
st.write(f"Expected time: {st_utils.format_time(expected_time_seconds)}")
st.button("Start!", on_click=start_screenshots)


