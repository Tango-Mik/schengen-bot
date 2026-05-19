import streamlit as st
import json
from datetime import datetime

# ✅ Page config
st.set_page_config(page_title="Schengen Monitor", layout="wide")

st.title("🌍 Schengen Appointment Monitor")
st.write("Live tracking of visa appointment systems")

# ✅ Load state
def load_state():
    with open("state.json", "r") as f:
        return json.load(f)

state = load_state()

# ✅ Country list
countries = ["france", "italy", "spain", "netherlands", "germany"]

# ✅ Display cards
cols = st.columns(len(countries))

for i, country in enumerate(countries):
    with cols[i]:
        st.subheader(country.upper())

        key = f"{country}_content"

        if key in state and state[key]:
            st.success("✅ Monitoring Active")
        else:
            st.warning("⚠️ Initializing")

        st.write(f"Last checked: {datetime.now().strftime('%H:%M:%S')}")

# ✅ Divider
st.divider()

# ✅ Show raw state (debug)
with st.expander("🔍 View Raw State Data"):
    st.json(state)