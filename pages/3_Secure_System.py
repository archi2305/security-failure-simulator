import time

import streamlit as st

from utils.security import (
    check_password_strength,
    hash_password,
    xor_decrypt_from_base64,
    xor_encrypt_to_base64,
)
from utils.state import add_log, bump_login_attempts, init_state
from utils.style import apply_theme, end_card, start_card


def loader(text: str) -> None:
    with st.spinner(text):
        time.sleep(0.25)


st.set_page_config(page_title="Secure System | SecureSphere", page_icon="🔐", layout="wide")
init_state()
apply_theme()

st.title("Secure System")
st.markdown(
    '<p class="hero-text">Registration, login, hashing, role-based access, and file encryption/decryption.</p>',
    unsafe_allow_html=True,
)

tabs = st.tabs(
    ["User Registration", "Login", "Password Checker", "RBAC", "File Encryption/Decryption"]
)

with tabs[0]:
    start_card("User Registration")
    st.info(
        "**What is this?** Create a user account. Internally, the system stores a hash of the password, not plain text."
    )
    new_user = st.text_input("New username", key="reg_user")
    new_password = st.text_input("New password", type="password", key="reg_pass")
    new_role = st.selectbox("Role", ["user", "admin"], key="reg_role")

    if new_password:
        st.markdown("#### Before vs After (Plain vs Hashed Password)")
        c1, c2 = st.columns(2)
        c1.write("Before (plain password)")
        c1.code(new_password)
        c2.write("After (stored hash)")
        c2.code(hash_password(new_password))

    if st.button("Register User"):
        loader("Registering user...")
        if not new_user or not new_password:
            st.error("Username and password are required.")
        elif new_user in st.session_state.users_db:
            st.error("Username already exists.")
        else:
            st.session_state.users_db[new_user] = {
                "password_hash": hash_password(new_password),
                "role": new_role,
            }
            add_log("register", f"New user registered: {new_user} ({new_role})", actor="system")
            st.success(f"User '{new_user}' registered successfully.")
    st.markdown("#### What happens step-by-step")
    st.write("Step 1: User enters username, password, and role.")
    st.write("Step 2: Password is converted into a hash.")
    st.write("Step 3: Only hashed password is stored in memory.")
    st.success("Result: Registration follows a safer password storage approach.")
    end_card()

with tabs[1]:
    start_card("Login")
    st.info(
        "**What is this?** Authentication verifies user identity by comparing entered password hash with stored hash."
    )
    username = st.text_input("Username", key="login_username_page")
    password = st.text_input("Password", type="password", key="login_password_page")
    st.markdown("#### Internal system view")
    st.write("Input password -> hash generated -> compare with stored hash")
    if st.button("Login"):
        loader("Checking credentials...")
        bump_login_attempts()
        record = st.session_state.users_db.get(username)
        if record and record["password_hash"] == hash_password(password):
            st.session_state.current_user = username
            add_log("login_success", f"{username} logged in", actor=username)
            st.success(f"Welcome, {username}.")
        else:
            add_log("login_failed", f"Failed login attempt for '{username or 'unknown'}'")
            st.error("Invalid username or password.")

    if st.session_state.current_user:
        current = st.session_state.current_user
        role = st.session_state.users_db[current]["role"]
        st.info(f"Logged in as: {current} ({role})")
        if st.button("Logout"):
            add_log("logout", f"{current} logged out", actor=current)
            st.session_state.current_user = None
            st.success("Logged out.")
    st.markdown("#### Why this matters")
    st.warning("Without authentication checks, anyone could claim any username.")
    st.success("Prevention: Always verify credentials and protect sessions.")
    end_card()

with tabs[2]:
    start_card("Password Strength Checker")
    st.info("**What is this?** This checks if a password is easy or hard to break.")
    candidate = st.text_input("Enter password", type="password", key="strength_password")
    if candidate:
        label, score, feedback = check_password_strength(candidate)
        if label == "Weak":
            st.error(f"Strength: {label} ({score}/5)")
        elif label == "Moderate":
            st.warning(f"Strength: {label} ({score}/5)")
        else:
            st.success(f"Strength: {label} ({score}/5)")
        if feedback:
            st.write("Suggestions:")
            for note in feedback:
                st.write(f"- {note}")
    st.markdown("#### Result")
    st.success("This helps users create stronger passwords before account creation.")
    end_card()

with tabs[3]:
    start_card("Role-Based Access Control")
    st.info(
        "**What is this?** RBAC (Role-Based Access Control) decides which actions each role can perform."
    )
    current = st.session_state.current_user
    if not current:
        st.warning("Login first to test role-based restrictions.")
    else:
        role = st.session_state.users_db[current]["role"]
        st.info(f"Current user: {current} ({role})")
        st.success("Allowed: View profile")
        if role == "admin":
            if st.button("Admin Action: Reset All User Sessions"):
                add_log("admin_action", "Reset all user sessions", actor=current)
                st.success("Admin action completed.")
        else:
            st.error("Restricted: Admin actions are available only to admin role.")
    st.markdown("#### Why it happened")
    st.warning("Users can be blocked from sensitive features when their role is limited.")
    st.success("Prevention: Map permissions carefully to each role.")
    end_card()

with tabs[4]:
    start_card("File Upload and Encryption/Decryption")
    st.info(
        "**What is this?** Demonstrates protection of uploaded text using simple encryption and decryption."
    )
    uploaded = st.file_uploader("Upload a text file", type=["txt"])
    key = st.text_input("Encryption key", value="team3-key", key="file_key")

    file_text = ""
    if uploaded:
        file_text = uploaded.getvalue().decode("utf-8", errors="ignore")
        st.text_area("Uploaded content preview", file_text, height=120, disabled=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Encrypt Uploaded Text"):
            loader("Processing...")
            if not file_text:
                st.error("Upload a text file first.")
            else:
                encrypted = xor_encrypt_to_base64(file_text, key)
                st.session_state.encrypted_text = encrypted
                add_log("file_encrypted", "Uploaded text encrypted", actor=st.session_state.current_user or "guest")
                st.code(encrypted)
                st.success("Result: Plain text changed into unreadable encrypted text.")

    with col2:
        encrypted_input = st.text_area(
            "Encrypted text to decrypt",
            st.session_state.encrypted_text,
            key="enc_input",
        )
        if st.button("Decrypt Text"):
            loader("Processing...")
            decrypted = xor_decrypt_from_base64(encrypted_input, key)
            add_log("file_decrypted", "Encrypted text decrypted", actor=st.session_state.current_user or "guest")
            st.code(decrypted)
            st.info("System internally uses key + reversible transformation for this demo.")
    st.caption("Educational demonstration only. This is not production-grade cryptography.")
    end_card()
