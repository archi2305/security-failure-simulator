import streamlit as st
import hashlib
import time

# Page configuration
st.set_page_config(
    page_title="Security Simulator",
    layout="wide"
)

# Custom CSS for modern UI
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #f6f0ff 0%, #eef4ff 45%, #fff3f8 100%);
        color: #3d3b52;
        font-family: 'Inter', sans-serif;
    }
    .block-container {
        max-width: 930px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4 {
        color: #2f2c47 !important;
        letter-spacing: 0.2px;
    }
    .hero-text {
        font-size: 1.05rem;
        line-height: 1.65;
        color: #5d5a76;
        margin-bottom: 1rem;
    }
    .card {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(214, 209, 240, 0.75);
        border-radius: 18px;
        padding: 1.25rem 1.25rem 1rem 1.25rem;
        margin-bottom: 1.15rem;
        box-shadow: 0 10px 25px rgba(151, 156, 205, 0.18);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        transform: scale(1.01);
        box-shadow: 0 12px 28px rgba(159, 167, 222, 0.22);
    }
    .section-title {
        font-size: 1.32rem;
        font-weight: 650;
        margin-bottom: 0.6rem;
        color: #373553;
    }
    .summary-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 0.1rem;
        margin-bottom: 0.65rem;
        color: #3d3b5f;
    }
    div[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.7);
        border-right: 1px solid rgba(212, 208, 238, 0.85);
    }
    div[data-testid="stSidebar"] * {
        color: #3f3b5b !important;
    }
    .stMarkdown p {
        margin-bottom: 0.65rem;
    }
    div[data-baseweb="select"] > div {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to show subtle loading animation
def show_simulation_loader(text):
    with st.spinner(text):
        time.sleep(0.2)

# Function to show summary section
def show_summary(attack, principle, prevention):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="summary-title">✅ Simulation Summary</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.write("Attack Type:")
    col1.success(attack)

    col2.write("Failed Principle:")
    col2.error(principle)

    col3.write("Prevention:")
    col3.info(prevention)
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Security Simulator")
scenario = st.sidebar.selectbox(
    "Choose Scenario",
    [
        "Weak Encryption",
        "No Integrity Check",
        "No Authentication",
        "Man-in-the-Middle Attack",
        "Poor Access Control"
    ]
)
st.sidebar.caption("Minimal demo of common security failures.")

# Main UI
st.title("Security Failure Case Study Simulator")
st.markdown(
    '<p class="hero-text">This tool demonstrates how common security mistakes lead to attacks and how to prevent them.</p>',
    unsafe_allow_html=True
)

# -----------------------------
# 1. Weak Encryption
# -----------------------------
if scenario == "Weak Encryption":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Weak Encryption</div>', unsafe_allow_html=True)
    show_simulation_loader("Running simulation...")

    message = "HELLO"
    key = 2

    encrypted = ""
    for c in message:
        encrypted += chr(ord(c) + key)

    col1, col2 = st.columns(2)

    col1.write("Original Message")
    col1.code(message)

    col2.write("Encrypted Message")
    col2.code(encrypted)

    st.warning("⚠️ Trying brute force attack")

    for k in range(1, 6):
        attempt = ""
        for c in encrypted:
            attempt += chr(ord(c) - k)

        st.write(f"Key {k}: {attempt}")

        if attempt == message:
            st.success("✅ Message cracked")

    st.error("❌ Confidentiality failed")

    show_summary(
        "Brute Force Attack",
        "Confidentiality",
        "Use strong encryption like AES"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 2. No Integrity Check
# -----------------------------
elif scenario == "No Integrity Check":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">No Integrity Check</div>', unsafe_allow_html=True)
    show_simulation_loader("Running simulation...")

    message = "Pay 5000"
    tampered = "Pay 9000"

    col1, col2 = st.columns(2)

    col1.write("Original Message")
    col1.code(message)

    col2.write("Tampered Message")
    col2.code(tampered)

    st.error("❌ No integrity protection")

    h1 = hashlib.sha256(message.encode()).hexdigest()
    h2 = hashlib.sha256(tampered.encode()).hexdigest()

    st.write("Original Hash:")
    st.code(h1)

    st.write("Tampered Hash:")
    st.code(h2)

    if h1 != h2:
        st.success("✅ Change detected using hash")

    show_summary(
        "Message Tampering",
        "Integrity",
        "Use hashing like SHA-256"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 3. No Authentication
# -----------------------------
elif scenario == "No Authentication":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">No Authentication</div>', unsafe_allow_html=True)
    show_simulation_loader("Running simulation...")

    user = st.text_input("Enter Username")

    if user:
        st.warning(f"⚠️ Access granted to {user} without password")

        st.write("User can access sensitive data")

        st.error("❌ Authentication failed")

        show_summary(
            "Unauthorized Access",
            "Authentication",
            "Use password and multi-factor authentication"
        )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 4. MITM Attack
# -----------------------------
elif scenario == "Man-in-the-Middle Attack":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Man-in-the-Middle Attack</div>', unsafe_allow_html=True)
    show_simulation_loader("Running simulation...")

    msg = "HELLO USER"

    col1, col2 = st.columns(2)

    col1.write("Sender sends")
    col1.code(msg)

    col2.write("Attacker reads")
    col2.code(msg)

    st.error("❌ Data is visible to attacker")

    st.write("After encryption:")

    encrypted = "X7@#91$!"
    st.code(encrypted)

    st.success("✅ Attacker cannot understand encrypted data")

    show_summary(
        "MITM Attack",
        "Confidentiality",
        "Use HTTPS and encryption"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 5. Poor Access Control
# -----------------------------
elif scenario == "Poor Access Control":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Poor Access Control</div>', unsafe_allow_html=True)
    show_simulation_loader("Running simulation...")

    action = st.selectbox("Select Action", ["View Data", "Delete Records"])

    if action == "Delete Records":
        st.warning("⚠️ User deleted records without permission")

        st.error("❌ Authorization failed")

        show_summary(
            "Privilege Misuse",
            "Authorization",
            "Use role-based access control"
        )
    else:
        st.success("✅ Safe action allowed")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Information Security Mini Project using Streamlit")