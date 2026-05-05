import streamlit as st

from utils.state import init_state
from utils.style import apply_theme, end_card, start_card


st.set_page_config(page_title="Dashboard | SecureSphere", page_icon="📊", layout="wide")
init_state()
apply_theme()

st.title("Dashboard")
st.markdown(
    '<p class="hero-text">Overview of platform activity and security posture.</p>',
    unsafe_allow_html=True,
)

stats = st.session_state.stats
col1, col2, col3 = st.columns(3)
col1.metric("Simulations Run", stats["simulations_run"])
col2.metric("Login Attempts", stats["login_attempts"])
col3.metric("Security Score", f'{stats["security_score"]}/100')

start_card("Platform Trends")
chart_data = {
    "metric": ["Simulations", "Login Attempts", "Security Score"],
    "value": [
        stats["simulations_run"],
        stats["login_attempts"],
        stats["security_score"],
    ],
}
st.bar_chart(chart_data, x="metric", y="value")
end_card()

start_card("Quick Insights")
if stats["security_score"] >= 80:
    st.success("Security posture is currently good for this demo system.")
elif stats["security_score"] >= 60:
    st.warning("Security posture is moderate. Run more secure checks.")
else:
    st.error("Security posture is low. Review controls in Secure System and Tools.")
end_card()
