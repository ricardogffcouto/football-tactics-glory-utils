import streamlit as st
import utils.streamlit as st_utils
import search

st_utils.header('Scouting')

filter_list = []

player_filter = st_utils.PlayerFilter()

if st.session_state.get("dataframe", None) is not None:
    st.session_state.dataframe = search.load_data("5c1560a2-ce92-45a9-b3e0-277d051a27c0")

player_filter.draw()
filtered_df = search.Filter().apply(st.session_state.get("dataframe", None), player_filter.search_json)

if filtered_df is not None:
    view_df = search.view_dataframe(filtered_df).sort_values(by="max_attr_skew", ascending=False)
    st.dataframe(view_df)