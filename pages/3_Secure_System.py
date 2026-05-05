import time

import streamlit as st

from utils.security import (
    check_password_strength,
    hash_password,
    xor_decrypt_from_base64,
    xor_encrypt_to_base64,
)
from utils.state import add_log, bump_login_attempts, init_state
from utils.style import apply_theme, end_card, explain, start_card


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
    new_user = st.text_input("New username", key="reg_user")
    new_password = st.text_input("New password", type="password", key="reg_pass")
    new_role = st.selectbox("Role", ["user", "admin"], key="reg_role")

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
    end_card()

with tabs[1]:
    start_card("Login")
    username = st.text_input("Username", key="login_username_page")
    password = st.text_input("Password", type="password", key="login_password_page")
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
    end_card()

with tabs[2]:
    start_card("Password Strength Checker")
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
    end_card()

with tabs[3]:
    start_card("Role-Based Access Control")
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
    explain("RBAC enforces least privilege by allowing actions based on assigned user role.")
    end_card()

with tabs[4]:
    start_card("File Upload and Encryption/Decryption")
    uploaded = st.file_uploader("Upload a text file", type=["txt"])
    key = st.text_input("Encryption key", value="team3-key", key="file_key")

    file_text = ""
    if uploaded:
        file_text = uploaded.getvalue().decode("utf-8", errors="ignore")
        st.text_area("Uploaded content preview", file_text, height=120, disabled=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Encrypt Uploaded Text"):
            loader("Encrypting file text...")
            if not file_text:
                st.error("Upload a text file first.")
            else:
                encrypted = xor_encrypt_to_base64(file_text, key)
                st.session_state.encrypted_text = encrypted
                add_log("file_encrypted", "Uploaded text encrypted", actor=st.session_state.current_user or "guest")
                st.code(encrypted)

    with col2:
        encrypted_input = st.text_area(
            "Encrypted text to decrypt",
            st.session_state.encrypted_text,
            key="enc_input",
        )
        if st.button("Decrypt Text"):
            loader("Decrypting text...")
            decrypted = xor_decrypt_from_base64(encrypted_input, key)
            add_log("file_decrypted", "Encrypted text decrypted", actor=st.session_state.current_user or "guest")
            st.code(decrypted)
    st.caption("Educational demonstration only. This is not production-grade cryptography.")
    end_card()
