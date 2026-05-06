import streamlit as st

from utils.state import init_state
from utils.style import apply_theme, end_card, start_card


st.set_page_config(page_title="Dashboard | SecureSphere", page_icon="📊", layout="wide")
init_state()
apply_theme()

st.title("Dashboard")
st.markdown(
    '<p class="hero-text">Overview of your learning progress and system security posture.</p>',
    unsafe_allow_html=True,
)
st.info("These numbers update as you run simulations, test logins, and use tools.")

stats = st.session_state.stats
col1, col2, col3 = st.columns(3)
col1.metric("Simulations Run", stats["simulations_run"])
col2.metric("Login Attempts", stats["login_attempts"])
col3.metric("Security Score", f'{stats["security_score"]}/100')

start_card("Platform Trends")
st.bar_chart(
    {
        "Simulations": [stats["simulations_run"]],
        "Login Attempts": [stats["login_attempts"]],
        "Security Score": [stats["security_score"]],
    }
)
end_card()

start_card("Quick Insights")
if stats["security_score"] >= 80:
    st.success("Security posture is currently good for this demo system.")
elif stats["security_score"] >= 60:
    st.warning("Security posture is moderate. Run more secure checks.")
else:
    st.error("Security posture is low. Review controls in Secure System and Tools.")
st.markdown("#### What this means")
st.write("- More secure actions generally improve the educational security score.")
st.write("- Failed login attempts and risky actions should be reviewed in Activity Logs.")
end_card()
