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