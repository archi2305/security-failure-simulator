import streamlit as st

from utils.state import init_state
from utils.style import apply_theme, end_card, start_card


st.set_page_config(page_title="SecureSphere", page_icon="🛡️", layout="wide")
init_state()
apply_theme()

st.title("SecureSphere - Interactive Cybersecurity Learning & Analysis Platform")
st.markdown(
    '<p class="hero-text">This app teaches cybersecurity concepts in simple language with step-by-step visual explanations.</p>',
    unsafe_allow_html=True,
)

start_card("How to Use")
st.info("Start from **1_Dashboard**, then open each module from the sidebar page list.")
st.markdown(
    """
    - Open **Dashboard** to understand project stats first
    - Go to **Attack Simulation Lab** to see attacks and why they work
    - Use **Secure System** to understand registration, login, hashing, and role checks
    - Try **Security Tools** for hands-on hashing, password checks, and input checks
    - Finish at **Activity Logs** to review what actions were performed
    """
)
st.success("Tip: Read each section top-to-bottom. Every module follows a learning flow.")
end_card()

st.caption("Built for academic evaluation with modular design for a 3-member team.")