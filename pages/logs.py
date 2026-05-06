import streamlit as st

from utils.state import init_state
from utils.style import apply_theme, end_card, start_card


st.set_page_config(page_title="Logs | SecureSphere", page_icon="🧾", layout="wide")
init_state()
apply_theme()

st.title("Activity Logs")
st.markdown(
    '<p class="hero-text">Tracks login attempts, encryption usage, and simulation actions in memory.</p>',
    unsafe_allow_html=True,
)

start_card("Action History")
logs = st.session_state.activity_logs
if logs:
    st.dataframe(logs, use_container_width=True)
else:
    st.info("No logs yet. Run modules and actions first.")

c1, c2 = st.columns(2)
c1.metric("Total actions", len(logs))
if c2.button("Clear logs"):
    st.session_state.activity_logs = []
    st.success("Logs cleared.")
end_card()
