import streamlit as st
import hashlib

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Security Simulator",
    page_icon="🔐",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS (PREMIUM LOOK)
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: #ffffff;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.stSelectbox div {
    border-radius: 10px;
}
.block-container {
    padding: 2rem 3rem;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #1c1f26;
    margin-bottom: 20px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SUMMARY FUNCTION
# -----------------------------
def show_summary(attack, principle, prevention):
    st.markdown("### 📊 Simulation Summary")
    col1, col2, col3 = st.columns(3)

    col1.success(f"**Attack**\n\n{attack}")
    col2.error(f"**Failed Principle**\n\n{principle}")
    col3.info(f"**Prevention**\n\n{prevention}")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🔐 Simulator")

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

run = st.sidebar.button("🚀 Run Simulation")

st.sidebar.markdown("---")
st.sidebar.info(
    "📘 This simulator demonstrates how security failures lead to cyber attacks.\n\nBuilt using Python & Streamlit."
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
# 🔐 Security Failure Case Study Simulator
### 🧪 Visualize Security Failures & Attacks
""")

st.markdown("---")

# -----------------------------
# MAIN LOGIC
# -----------------------------
if run:

    st.subheader(f"🔎 Scenario: {scenario}")

    # =====================================================
    # 1. WEAK ENCRYPTION
    # =====================================================
    if scenario == "Weak Encryption":

        message = "HELLO"
        key = 2

        encrypted = "".join(chr(ord(c)+key) for c in message)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📥 Original")
            st.code(message)

        with col2:
            st.markdown("### 🔐 Encrypted")
            st.code(encrypted)

        st.warning("⚠ Brute force attack in progress...")

        for k in range(1, 6):
            attempt = "".join(chr(ord(c)-k) for c in encrypted)
            st.write(f"Trying key {k}: {attempt}")

            if attempt == message:
                st.success("✅ Message cracked!")

        st.error("❌ Confidentiality Failed")

        show_summary(
            "Brute Force Attack",
            "Confidentiality",
            "Use AES with strong key sizes"
        )

    # =====================================================
    # 2. INTEGRITY
    # =====================================================
    elif scenario == "No Integrity Check":

        message = "Pay 5000"
        tampered = "Pay 9000"

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📩 Original Message")
            st.code(message)

        with col2:
            st.markdown("### ⚠ Tampered Message")
            st.code(tampered)

        st.error("❌ No integrity protection")

        h1 = hashlib.sha256(message.encode()).hexdigest()
        h2 = hashlib.sha256(tampered.encode()).hexdigest()

        st.markdown("### 🔐 Hash Comparison")
        st.code(f"Original: {h1}")
        st.code(f"Tampered: {h2}")

        if h1 != h2:
            st.success("✅ Integrity violation detected!")

        show_summary(
            "Message Tampering",
            "Integrity",
            "Use SHA-256 hashing"
        )

    # =====================================================
    # 3. AUTHENTICATION
    # =====================================================
    elif scenario == "No Authentication":

        user = st.text_input("Enter Username")

        if st.button("Login"):
            st.warning(f"⚠ Access granted to {user} without password!")

            st.error("❌ Authentication Failed")

            show_summary(
                "Unauthorized Access",
                "Authentication",
                "Use password + MFA"
            )

    # =====================================================
    # 4. MITM
    # =====================================================
    elif scenario == "Man-in-the-Middle Attack":

        msg = "HELLO USER"

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📤 Sender")
            st.code(msg)

        with col2:
            st.markdown("### 🕵 Attacker Reads")
            st.code(msg)

        st.error("❌ Data exposed!")

        st.markdown("### 🔐 After Encryption")
        st.code("X7@#91$!")

        st.success("✅ Attacker cannot understand data")

        show_summary(
            "MITM Attack",
            "Confidentiality",
            "Use HTTPS / TLS"
        )

    # =====================================================
    # 5. ACCESS CONTROL
    # =====================================================
    elif scenario == "Poor Access Control":

        action = st.selectbox("Select Action", ["View Data", "Delete Records"])

        if st.button("Perform Action"):

            if action == "Delete Records":
                st.warning("⚠ Student deleted records!")

                st.error("❌ Authorization Failed")

                show_summary(
                    "Privilege Misuse",
                    "Authorization",
                    "Use RBAC"
                )
            else:
                st.success("✅ Safe action")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("🔐 Information Security Mini Project | Streamlit UI")