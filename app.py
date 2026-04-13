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
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 45%, #312e81 100%);
        color: #e2e8f0;
    }
    h1, h2, h3, h4 {
        color: #f8fafc !important;
        letter-spacing: 0.3px;
    }
    .hero-text {
        font-size: 1.08rem;
        color: #cbd5e1;
        margin-bottom: 1.2rem;
    }
    .card {
        background: rgba(15, 23, 42, 0.62);
        border: 1px solid rgba(148, 163, 184, 0.24);
        border-radius: 16px;
        padding: 1.1rem 1.1rem 0.8rem 1.1rem;
        margin-bottom: 1rem;
        box-shadow: 0 12px 28px rgba(2, 6, 23, 0.30);
        transition: all 0.25s ease;
    }
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 34px rgba(59, 130, 246, 0.22);
        border-color: rgba(96, 165, 250, 0.38);
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 650;
        margin-bottom: 0.3rem;
        color: #dbeafe;
    }
    .summary-title {
        font-size: 1.18rem;
        font-weight: 700;
        margin-top: 0.2rem;
        margin-bottom: 0.5rem;
        color: #ede9fe;
    }
    div[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.92);
        border-right: 1px solid rgba(148, 163, 184, 0.25);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to show simulation animation
def show_simulation_animation():
    progress = st.progress(0, text="Running simulation...")
    for i in range(1, 101, 25):
        time.sleep(0.03)
        progress.progress(i, text=f"Running simulation... {i}%")
    progress.empty()

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
st.sidebar.title("🛡️ Security Simulator")
st.sidebar.markdown("---")
st.sidebar.write("This project demonstrates basic security failures.")
st.sidebar.caption("Navigate scenarios using tabs in the main view.")

# Main UI
st.title("🛡️ Security Failure Case Study Simulator")
st.markdown(
    '<p class="hero-text">This tool demonstrates how common security mistakes lead to attacks and how to prevent them.</p>',
    unsafe_allow_html=True
)

st.markdown("---")

# Scenario tabs
tabs = st.tabs(
    [
        "🔓 Weak Encryption",
        "🧩 No Integrity Check",
        "🔐 No Authentication",
        "🕵️ MITM Attack",
        "🚫 Poor Access Control"
    ]
)

# -----------------------------
# 1. Weak Encryption
# -----------------------------
with tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔓 Scenario: Weak Encryption</div>', unsafe_allow_html=True)
    with st.spinner("Simulating brute force attack..."):
        show_simulation_animation()

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
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧩 Scenario: No Integrity Check</div>', unsafe_allow_html=True)
    with st.spinner("Checking data integrity..."):
        show_simulation_animation()

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
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔐 Scenario: No Authentication</div>', unsafe_allow_html=True)
    with st.spinner("Evaluating login flow..."):
        show_simulation_animation()

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
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🕵️ Scenario: Man-in-the-Middle Attack</div>', unsafe_allow_html=True)
    with st.spinner("Simulating network interception..."):
        show_simulation_animation()

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
with tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚫 Scenario: Poor Access Control</div>', unsafe_allow_html=True)
    with st.spinner("Checking access rules..."):
        show_simulation_animation()

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