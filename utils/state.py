from datetime import datetime

import streamlit as st

from utils.security import hash_password


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def init_state() -> None:
    if "users_db" not in st.session_state:
        st.session_state.users_db = {
            "admin": {"password_hash": hash_password("Admin@123"), "role": "admin"},
            "student": {"password_hash": hash_password("User@123"), "role": "user"},
        }
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "stats" not in st.session_state:
        st.session_state.stats = {
            "simulations_run": 0,
            "login_attempts": 0,
            "security_score": 72,
        }
    if "activity_logs" not in st.session_state:
        st.session_state.activity_logs = []
    if "encrypted_text" not in st.session_state:
        st.session_state.encrypted_text = ""


def add_log(action: str, details: str, actor: str = "system") -> None:
    st.session_state.activity_logs.append(
        {
            "time": now_text(),
            "actor": actor,
            "action": action,
            "details": details,
        }
    )


def bump_simulations() -> None:
    st.session_state.stats["simulations_run"] += 1
    st.session_state.stats["security_score"] = min(
        100, st.session_state.stats["security_score"] + 1
    )


def bump_login_attempts() -> None:
    st.session_state.stats["login_attempts"] += 1
