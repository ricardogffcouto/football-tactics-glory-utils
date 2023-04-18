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

st.markdown(
    """
    <style>
        .stSelectbox > label,
        .stNumberInput > label,
        .stMultiSelect > label {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

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

def search_json():
    search_json = {}
    for key, value in st.session_state.filter_list.items():
        search_json[mapping[value['filter']]] = value['values']
    return search_json

if not st.session_state.get("filter_list", None):
    st.session_state.filter_list = {}

if st.session_state.get("dataframe", None) is not None:
    st.session_state.dataframe = search.load_data("5c1560a2-ce92-45a9-b3e0-277d051a27c0")

for key in st.session_state.filter_list.keys():
    new_filter(key)

col1, col2, col3, col4 = st.columns(4)
col1.button("Add Filter", on_click=add_filter)
col2.button("Import Filters")
col3.button("Export Filters")
col4.button("Clear Filters")

filtered_df = search.Filter().apply(st.session_state.dataframe, search_json())
view_df = search.view_dataframe(filtered_df).sort_values(by="max_attr_skew", ascending=False)
st.dataframe(view_df)