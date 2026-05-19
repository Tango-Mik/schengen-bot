import streamlit as st
import requests
from datetime import datetime

# ✅ CONFIG
GITHUB_USERNAME = "Tango-Mik"
REPO_NAME = "schengen-bot"
BRANCH = "main"

STATE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH}/state.json"


# ✅ Page config
st.set_page_config(page_title="Schengen Monitor", layout="wide")

st.title("🌍 Schengen Appointment Monitor")
st.caption("Live monitoring of visa appointment systems")

# ✅ Load state from GitHub (LIVE DATA)
def load_state():
    try:
        response = requests.get(STATE_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch state.json (Status: {response.status_code})")
            return {}
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}

state = load_state()


# ✅ Countries
countries = ["france", "italy", "spain", "netherlands", "germany"]

# ✅ Display UI
cols = st.columns(len(countries))

for i, country in enumerate(countries):
    with cols[i]:
        st.subheader(country.upper())

        key = f"{country}_content"

        if key in state and state[key]:
            st.success("✅ Active")
        else:
            st.warning("⚠️ Initializing")

        st.caption(f"Last refresh: {datetime.now().strftime('%H:%M:%S')}")

# ✅ Divider
st.divider()

# ✅ Auto refresh note
st.caption("🔄 Auto-refresh browser for latest data (or reload page)")

# ✅ Debug view
with st.expander("🔍 View Raw State Data"):
    st.json(state)
