import streamlit as st
import hashlib

st.set_page_config(page_title="Security Simulator", layout="centered")

st.title("🔐 Security Failure Case Study Simulator")

st.write("This application demonstrates how security failures lead to cyber attacks.")

# Scenario selection
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

# Run button
if st.button("Run Simulation"):

    st.subheader(f"🔎 Scenario: {scenario}")

    # -----------------------------
    # 1. WEAK ENCRYPTION
    # -----------------------------
    if scenario == "Weak Encryption":

        st.write("🔓 Demonstrating weak encryption using small key...")

        message = "HELLO"
        key = 2  # weak key

        # Simple Caesar Cipher
        encrypted = ""
        for char in message:
            encrypted += chr(ord(char) + key)

        st.write(f"Plain Text: {message}")
        st.write(f"Encrypted Text: {encrypted}")

        st.warning("⚠ Attacker starts brute force attack...")

        # Brute force
        for k in range(1, 5):
            attempt = ""
            for char in encrypted:
                attempt += chr(ord(char) - k)

            st.write(f"Trying key {k}: {attempt}")

            if attempt == message:
                st.success("✅ Message cracked successfully!")

        st.error("❌ Confidentiality Failed due to weak key")

        st.info("✔ Prevention: Use strong encryption (AES with large key size)")

    # -----------------------------
    # 2. NO INTEGRITY CHECK
    # -----------------------------
    elif scenario == "No Integrity Check":

        st.write("📩 Sending message without integrity protection...")

        message = "Pay 5000"

        st.write(f"Original Message: {message}")

        # Attacker modifies message
        tampered_message = "Pay 9000"

        st.warning("⚠ Message intercepted and modified!")

        st.write(f"Tampered Message: {tampered_message}")

        st.error("❌ Receiver cannot detect change (No Integrity Check)")

        st.subheader("🔐 Applying Hash for Integrity Check")

        # Hashing
        original_hash = hashlib.sha256(message.encode()).hexdigest()
        tampered_hash = hashlib.sha256(tampered_message.encode()).hexdigest()

        st.write(f"Original Hash: {original_hash}")
        st.write(f"Tampered Hash: {tampered_hash}")

        if original_hash != tampered_hash:
            st.success("✅ Integrity Violation Detected!")

        st.info("✔ Prevention: Use hashing (SHA-256) to ensure integrity")

    # -----------------------------
    # OTHER CASES (NEXT PHASE)
    # -----------------------------
    else:
        st.info("🚧 This scenario will be implemented in next phase.")