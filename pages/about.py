import streamlit as st

from utils.state import init_state
from utils.style import apply_theme, end_card, start_card


st.set_page_config(page_title="About | SecureSphere", page_icon="ℹ️", layout="wide")
init_state()
apply_theme()

st.title("About SecureSphere")
st.markdown(
    '<p class="hero-text">Cybersecurity Learning & Analysis Platform with practical authentication, encryption, signatures, and key exchange demos.</p>',
    unsafe_allow_html=True,
)

start_card("Module Overview")
st.markdown(
    """
    - **Dashboard (`app.py`)**: live metrics and navigation entry
    - **Attack Simulation Lab (`pages/simulator.py`)**: weak encryption, MITM, DH secure-vs-insecure
    - **Secure System (`pages/secure_system.py`)**: bcrypt auth, RBAC, AES(Fernet) file/text encryption
    - **Security Tools (`pages/tools.py`)**: RSA signatures, hash generator, password analyzer
    - **Logs (`pages/logs.py`)**: action history in memory
    """
)
end_card()

start_card("Suggested 3-Developer Split")
st.markdown(
    """
    - Developer 1: Attack lab scenarios and learning flow
    - Developer 2: Secure system authentication, RBAC, encryption workflows
    - Developer 3: Security tools, dashboard, logging, and documentation
    """
)
end_card()
