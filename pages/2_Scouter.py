import uuid

import streamlit as st
import utils.streamlit as st_utils
from constants import *
import search

st_utils.header('Scouting')

filter_list = []

mapping = {
    'Position': 'pos',
    'Age': 'age',
    'Giftedness': 'gift',
    'Accuracy': 'acc',
    'Passing': 'pas',
    'Defence': 'df',
    'Control': 'ctr',
    'Skill': 'skill',
}

def skill_filter(key):
    defaults = st.session_state.filter_list[key].get('values', [1, 100])
    col1, col2, col3 = st.columns(3)
    col1.selectbox("", SKILLS, default=defaults[0], on_change=update_filter, key=f"{key}_name", args=(key,))
    col2.number_input("Min", value=defaults[1], min_value=1, max_value=3, step=1, on_change=update_filter, key=f"{key}_min", args=(key,))
    col3.number_input("Min", value=defaults[2], min_value=1, max_value=3, step=1, on_change=update_filter, key=f"{key}_max", args=(key,))


def is_in_filter(key, options):
    default = st.session_state.filter_list[key].get('values', options[0])
    st.multiselect("", options, default=default, on_change=update_filter, key=f"{key}_values", args=(key,))

def min_max_filter(key):
    defaults = st.session_state.filter_list[key].get('values', [1, 100])
    col1, col2 = st.columns(2)
    col1.number_input("Min", value=defaults[0], min_value=1, step=1, on_change=update_filter, key=f"{key}_min", args=(key,))
    col2.number_input("Min", value=defaults[1], min_value=1, step=1, on_change=update_filter, key=f"{key}_max", args=(key,))

def new_filter(key):
    defaults = st.session_state.filter_list[key]
    col1, col2, col3 = st.columns([2, 5, 1])
    selected_filter_index = list(mapping.keys()).index(defaults['filter'])
    filter_name = col1.selectbox("", list(mapping.keys()), on_change=update_filter, key=f"{key}_filter_name", args=(key,), index=selected_filter_index)
    with col2:
        if filter_name == "Position":
            is_in_filter(key, POSITIONS)
        else:
            min_max_filter(key)
    with col3:
        st.button("X", on_click=delete_filter, args=(key,), key=f"{key}_delete")

def update_filter(key):
    st.session_state.filter_list[key] = {
        "filter": st.session_state[f"{key}_filter_name"],
        "values": st.session_state.get(f"{key}_values", []) or [
            st.session_state.get(f"{key}_min", 1),
            st.session_state.get(f"{key}_max", 1),
        ]
    }

def delete_filter(key):
    st.session_state.filter_list.pop(key)
def add_filter():
    st.session_state.filter_list[uuid.uuid4()] = {
        "filter": "Position",
        "values": [],
    }

def show_search_json():
    search_json = {}
    for key, value in st.session_state.filter_list.items():
        search_json[mapping[value['filter']]] = value['values']
    return st.json(search_json)

if not st.session_state.get("filter_list", None):
    st.session_state.filter_list = {}

# show_search_json()
# for key in st.session_state.filter_list.keys():
#     new_filter(key)
# st.button("Add Filter", on_click=add_filter)

tabs = st.tabs(["1", "2", "3", "4", "5", "6"])
for tab in tabs:
    with tab:
        search_json = st.text_area("Search JSON", key=uuid.uuid4())
        search_btn = st.button("Search", key=uuid.uuid4())
        if search_btn:
            df = search.Filter().apply(df, search_json)
            st.dataframe(df, key=uuid.uuid4())