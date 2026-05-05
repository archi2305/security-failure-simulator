import streamlit as st

from utils.state import init_state
from utils.style import apply_theme, end_card, start_card


st.set_page_config(page_title="About | SecureSphere", page_icon="ℹ️", layout="wide")
init_state()
apply_theme()

st.title("About SecureSphere")
st.markdown(
    '<p class="hero-text">Academic multi-module cybersecurity platform for interactive learning and analysis.</p>',
    unsafe_allow_html=True,
)

start_card("Project Scope")
st.markdown(
    """
    SecureSphere demonstrates practical information security concepts through modular pages:
    Dashboard, Attack Simulation Lab, Secure System, Security Tools, and Activity Logs.
    The implementation intentionally avoids external databases to keep deployment simple.
    """
)
end_card()

start_card("Suggested 3-Member Contribution")
st.markdown(
    """
    - **Developer 1:** Attack Simulation Lab scenarios, step-by-step flow, explanations
    - **Developer 2:** Secure System (registration/login, hashing, RBAC, file encryption)
    - **Developer 3:** Dashboard/Tools/Logs, UI consistency, testing and documentation
    """
)
end_card()

st.caption("SecureSphere - Interactive Cybersecurity Learning & Analysis Platform")
