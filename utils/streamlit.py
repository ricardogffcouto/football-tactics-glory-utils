import uuid
from dataclasses import dataclass
import json
import streamlit as st
from constants import *

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    st.components.v1.html(nav_script)


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02d} hours and {minutes:02d} minutes"
    else:
        return f"{minutes:02d} minutes"

def get_screenshots_path(session_id):
    return f"{SCREENSHOT_PATH}/{session_id}/screenshots"

def get_player_lists_path(session_id):
    return f"{PLAYER_LISTS_PATH}/{session_id}"

def header(subtitle):
    st.write('# Football Tactics and Glory')
    st.write(f'## {subtitle}')


class PlayerFilter:
    MAPPING = {
        'Position': 'pos',
        'Age': 'age',
        'Giftedness': 'gift',
        'Accuracy': 'acc',
        'Passing': 'pas',
        'Defence': 'df',
        'Control': 'ctr',
        'Skill': 'skill',
        'Level': 'lvl',
    }
    def __init__(self):
        self.container_id: uuid.UUID = uuid.uuid4()

        if not st.session_state.get(str(self.container_id), None):
            st.session_state[str(self.container_id)] = {}

    def _skill_filter(self, key):
        defaults = self.filter_container[key].get('values', [1, 3])
        col1, col2, col3 = st.columns(3)
        col1.selectbox("", SKILLS, on_change=self._update_filter, key=self._key_id(key, "name"), args=(key,))
        col2.number_input("Min", value=defaults[0], min_value=1, max_value=3, step=1, on_change=self._update_filter, key=self._key_id(key, "min"), args=(key,))
        col3.number_input("Max", value=defaults[1], min_value=1, max_value=3, step=1, on_change=self._update_filter, key=self._key_id(key, "max"), args=(key,))

    def _is_in_filter(self, key, options):
        default = self.filter_container[key].get('values', options[0])
        st.multiselect("", options, default=default, on_change=self._update_filter, key=self._key_id(key, "values"), args=(key,))

    def _min_max_filter(self, key):
        defaults = self.filter_container[key].get('values', [1, 100])
        col1, col2 = st.columns(2)
        col1.number_input("Min", value=defaults[0], min_value=1, step=1, on_change=self._update_filter, key=self._key_id(key, "min"), args=(key,))
        col2.number_input("Max", value=defaults[1], min_value=1, step=1, on_change=self._update_filter, key=self._key_id(key, "max"), args=(key,))

    def _draw_filter(self, key):
        defaults = self.filter_container[key]
        col1, col2, col3 = st.columns([2, 5, 1])
        selected_filter_index = list(self.MAPPING.keys()).index(defaults['filter'])
        filter_name = col1.selectbox("", list(self.MAPPING.keys()), on_change=self._update_filter, key=self._key_id(key, "filter_name"), args=(key,), index=selected_filter_index)
        with col2:
            if filter_name == "Position":
                self._is_in_filter(key, POSITIONS)
            elif filter_name == "Skill":
                self._skill_filter(key)
            else:
                self._min_max_filter(key)
        with col3:
            st.button("X", on_click=self._delete_filter, args=(key,), key=self._key_id(key, "delete"))

    def _update_filter(self, key):
        self.filter_container[key] = {
            "filter": st.session_state[self._key_id(key, "filter_name")],
            "values": st.session_state.get(self._key_id(key, "values"), []) or [
                st.session_state.get(self._key_id(key, "min"), 1),
                st.session_state.get(self._key_id(key, "max"), 1),
            ]
        }

    def _delete_filter(self, key):
        self.filter_container.pop(key)

    def _add_filter(self):
        self.filter_container[str(uuid.uuid4())] = {
            "filter": "Position",
            "values": [],
        }

    def _clear_filters(self):
        st.session_state[self.container_id] = {}

    def _import_filters(self):
        pass

    def _export_filters(self):
        with open("data.json", "w") as outfile:
            json.dump(self.search_json, outfile)


    def _key_id(self, key, value):
        return f"{self.container_id}_{key}_{value}"

    @property
    def filter_container(self):
        return st.session_state[str(self.container_id)]

    @property
    def search_json(self):
        search_json = {}
        for key, value in self.filter_container.items():
            search_json[self.MAPPING[value['filter']]] = value['values']
        return search_json

    def draw(self):
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

        for key in self.filter_container.keys():
            self._draw_filter(key)

        col1, col2 = st.columns(2)
        col1.button("Add", on_click=self._add_filter)
        col2.button("Clear", on_click=self._clear_filters)
        filter_choices = st.expander("Filter Import/Export")

        with filter_choices:
            st.write("Current Filter JSON")
            st.json(self.search_json)
            st.file_uploader("Import", type="json", on_change=self._import_filters)
            st.text_input("Name")
            st.button("Export", on_click=self._export_filters)
