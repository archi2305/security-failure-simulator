import streamlit as st
import hashlib

st.set_page_config(page_title="Security Simulator", layout="centered")

# -----------------------------
# TITLE
# -----------------------------
st.title("🔐 Security Failure Case Study Simulator")

st.write("This application demonstrates how security failures lead to cyber attacks and how they can be prevented.")

# -----------------------------
# SCENARIO SELECTION
# -----------------------------
scenario = st.selectbox(
    "Select a Security Failure Scenario:",
    [
        "Weak Encryption",
        "No Integrity Check",
        "No Authentication",
        "Man-in-the-Middle Attack",
        "Poor Access Control"
    ]
)

# -----------------------------
# RUN SIMULATION
# -----------------------------
if st.button("Run Simulation"):

    st.subheader(f"🔎 Scenario: {scenario}")

    # =====================================================
    # 1. WEAK ENCRYPTION
    # =====================================================
    if scenario == "Weak Encryption":

        st.write("🔓 Demonstrating weak encryption using small key...")

        message = "HELLO"
        key = 2  # weak key

        encrypted = ""
        for char in message:
            encrypted += chr(ord(char) + key)

        st.write(f"Plain Text: {message}")
        st.write(f"Encrypted Text: {encrypted}")

        st.warning("⚠ Attacker starts brute force attack...")

        for k in range(1, 6):
            attempt = ""
            for char in encrypted:
                attempt += chr(ord(char) - k)

            st.write(f"Trying key {k}: {attempt}")

            if attempt == message:
                st.success("✅ Message cracked successfully!")

        st.error("❌ Confidentiality Failed due to weak key")

        st.info("✔ Prevention: Use strong encryption (AES with large key size)")

    # =====================================================
    # 2. NO INTEGRITY CHECK
    # =====================================================
    elif scenario == "No Integrity Check":

        st.write("📩 Sending message without integrity protection...")

        message = "Pay 5000"
        st.write(f"Original Message: {message}")

        tampered_message = "Pay 9000"

        st.warning("⚠ Message intercepted and modified!")
        st.write(f"Tampered Message: {tampered_message}")

        st.error("❌ Receiver cannot detect change (No Integrity Check)")

        st.subheader("🔐 Applying Hash for Integrity Check")

        original_hash = hashlib.sha256(message.encode()).hexdigest()
        tampered_hash = hashlib.sha256(tampered_message.encode()).hexdigest()

        st.write(f"Original Hash: {original_hash}")
        st.write(f"Tampered Hash: {tampered_hash}")

        if original_hash != tampered_hash:
            st.success("✅ Integrity Violation Detected!")

        st.info("✔ Prevention: Use hashing (SHA-256) to ensure integrity")

    # =====================================================
    # 3. NO AUTHENTICATION
    # =====================================================
    elif scenario == "No Authentication":

        st.write("🔓 System without authentication...")

        username = st.text_input("Enter username:")

        if st.button("Login"):
            st.warning(f"⚠ Access granted to {username} without password!")

            st.write("Attacker logged in as admin and modified sensitive data.")

            st.error("❌ Authentication Failed")

            st.info("✔ Prevention: Use password authentication + hashing + OTP")

    # =====================================================
    # 4. MAN-IN-THE-MIDDLE ATTACK
    # =====================================================
    elif scenario == "Man-in-the-Middle Attack":

        st.write("📡 Sending message over insecure network...")

        message = "HELLO USER"

        st.write(f"Sender sends: {message}")

        st.warning("⚠ Attacker intercepts the message!")
        st.write(f"Attacker reads: {message}")

        st.error("❌ Confidentiality Failed")

        st.subheader("🔐 Applying Encryption")

        encrypted = "X7@#91$!"
        st.write(f"Encrypted Message: {encrypted}")

        st.success("✅ Attacker cannot understand encrypted data")

        st.info("✔ Prevention: Use encryption during transmission (HTTPS, TLS)")

    # =====================================================
    # 5. POOR ACCESS CONTROL
    # =====================================================
    elif scenario == "Poor Access Control":

        st.write("👤 User Role: Student")

        action = st.selectbox("Select Action:", ["View Data", "Delete Records"])

        if st.button("Perform Action"):

            if action == "Delete Records":
                st.warning("⚠ Student was able to delete records!")

                st.error("❌ Authorization Failed")

                st.info("✔ Prevention: Implement Role-Based Access Control (RBAC)")

            else:
                st.success("✅ Action allowed safely")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Developed for Information Security Project | Educational Use Only")