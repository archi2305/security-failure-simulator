import streamlit as st

from utils.state import init_state
from utils.style import apply_theme, end_card, start_card


st.set_page_config(page_title="SecureSphere", page_icon="🛡️", layout="wide")
init_state()
apply_theme()

st.title("SecureSphere - Interactive Cybersecurity Learning & Analysis Platform")
st.markdown(
    '<p class="hero-text">Use the sidebar pages to explore simulations, security controls, tools, dashboard metrics, and activity logs.</p>',
    unsafe_allow_html=True,
)

start_card("How to Use")
st.markdown(
    """
    - Open **Dashboard** to track simulations, login attempts, and security score
    - Run attacks in **Attack Simulation Lab** with step-by-step flow and explanations
    - Use **Secure System** for registration/login, RBAC, and file encryption demo
    - Try **Security Tools** for hashing, password analysis, and input checking
    - Review **Activity Logs** to see user/system events in table format
    """
)
end_card()

st.caption("Built for academic evaluation with modular design for a 3-member team.")