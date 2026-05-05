import streamlit as st

from utils.state import init_state
from utils.style import apply_theme, end_card, start_card


st.set_page_config(page_title="Activity Logs | SecureSphere", page_icon="🧾", layout="wide")
init_state()
apply_theme()

st.title("Activity Logs")
st.markdown(
    '<p class="hero-text">In-memory action logs captured across all modules.</p>',
    unsafe_allow_html=True,
)

start_card("Log Table")
logs = st.session_state.activity_logs
if logs:
    st.dataframe(logs, use_container_width=True)
else:
    st.info("No logs yet. Perform actions in other modules to populate logs.")

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Logs", len(logs))
with col2:
    if st.button("Clear Logs"):
        st.session_state.activity_logs = []
        st.success("Logs cleared.")
end_card()
