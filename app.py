import streamlit as st
import hashlib

# Page configuration
st.set_page_config(
    page_title="Security Simulator",
    layout="wide"
)

# Simple summary function
def show_summary(attack, principle, prevention):
    st.subheader("Simulation Summary")

    col1, col2, col3 = st.columns(3)

    col1.write("Attack Type:")
    col1.success(attack)

    col2.write("Failed Principle:")
    col2.error(principle)

    col3.write("Prevention:")
    col3.info(prevention)

# Sidebar for navigation
st.sidebar.title("Simulator")

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

run = st.sidebar.button("Run Simulation")

st.sidebar.markdown("---")
st.sidebar.write("This project demonstrates basic security failures.")

# Main heading
st.title("Security Failure Case Study Simulator")
st.write("This tool shows how security mistakes lead to attacks and how to prevent them.")

st.markdown("---")

# Run simulation
if run:

    st.subheader(f"Scenario: {scenario}")

    # 1. Weak Encryption
    if scenario == "Weak Encryption":

        # Simple encryption using small key
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

        st.warning("Trying brute force attack")

        # Brute force logic
        for k in range(1, 6):
            attempt = ""
            for c in encrypted:
                attempt += chr(ord(c) - k)

            st.write(f"Key {k}: {attempt}")

            if attempt == message:
                st.success("Message cracked")

        st.error("Confidentiality failed")

        show_summary(
            "Brute Force Attack",
            "Confidentiality",
            "Use strong encryption like AES"
        )

    # 2. No Integrity Check
    elif scenario == "No Integrity Check":

        message = "Pay 5000"
        tampered = "Pay 9000"

        col1, col2 = st.columns(2)

        col1.write("Original Message")
        col1.code(message)

        col2.write("Tampered Message")
        col2.code(tampered)

        st.error("No integrity protection")

        # Hash comparison
        h1 = hashlib.sha256(message.encode()).hexdigest()
        h2 = hashlib.sha256(tampered.encode()).hexdigest()

        st.write("Original Hash:")
        st.code(h1)

        st.write("Tampered Hash:")
        st.code(h2)

        if h1 != h2:
            st.success("Change detected using hash")

        show_summary(
            "Message Tampering",
            "Integrity",
            "Use hashing like SHA-256"
        )

    # 3. No Authentication
    elif scenario == "No Authentication":

        user = st.text_input("Enter Username")

        # No password check, so anyone gets access
        if user:
            st.warning(f"Access granted to {user} without password")

            st.write("User can access sensitive data")

            st.error("Authentication failed")

            show_summary(
                "Unauthorized Access",
                "Authentication",
                "Use password and multi-factor authentication"
            )

    # 4. Man-in-the-Middle Attack
    elif scenario == "Man-in-the-Middle Attack":

        msg = "HELLO USER"

        col1, col2 = st.columns(2)

        col1.write("Sender sends")
        col1.code(msg)

        col2.write("Attacker reads")
        col2.code(msg)

        st.error("Data is visible to attacker")

        st.write("After encryption:")

        encrypted = "X7@#91$!"
        st.code(encrypted)

        st.success("Attacker cannot understand encrypted data")

        show_summary(
            "MITM Attack",
            "Confidentiality",
            "Use HTTPS and encryption"
        )

    # 5. Poor Access Control
    elif scenario == "Poor Access Control":

        action = st.selectbox("Select Action", ["View Data", "Delete Records"])

        # No proper role restriction
        if action == "Delete Records":
            st.warning("User deleted records without permission")

            st.error("Authorization failed")

            show_summary(
                "Privilege Misuse",
                "Authorization",
                "Use role-based access control"
            )
        else:
            st.success("Safe action allowed")

# Footer
st.markdown("---")
st.caption("Information Security Mini Project using Streamlit")