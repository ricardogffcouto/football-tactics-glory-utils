import streamlit as st
import utils.streamlit as st_utils
import search

st_utils.header('Scouting')

filter_list = []

if st.session_state.get("player_filter") is None:
    st.session_state["player_filter"] = st_utils.PlayerFilter()

st.session_state.player_filter.draw()

if st.session_state.get("dataframe") is not None:
    st.session_state.dataframe = search.load_data("2032-07")

filtered_df = search.Filter().apply(st.session_state.get("dataframe"), st.session_state.get("player_filter").search_json)

if filtered_df is not None:
    view_df = search.view_dataframe(filtered_df).sort_values(by="max_attr_skew", ascending=False)
    st.dataframe(view_df)