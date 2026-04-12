import streamlit as st

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
    
    st.info("Simulation will be implemented in next phase.")

    st.write("👉 This will demonstrate how this security failure leads to an attack.")