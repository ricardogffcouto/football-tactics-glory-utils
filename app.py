import utils.streamlit as st_utils
import streamlit as st



st_utils('Utilities')
st.write("### 1. Team Parser")
st.write("""
The team parser is used to parse the teams from the screenshots.\n
It will parse the teams and save all the players to a csv file.\n
The csv file can be downloaded.
""")
st.write("### 2. Scouter")
st.write("""
The scouter is used to find players from the csv file.\n
You can filter, sort, and create a shortlist of players for your team.\n
The shortlist can be downloaded.
""")
st.write("### 3. Probability Calculator")
st.write("""
The probability calculator is used to calculate the probability of winning a duel during a match.\n
It also provides a quick reference for some usual values of duels.
""")
