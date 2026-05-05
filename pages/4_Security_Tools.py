import hashlib
import time

import streamlit as st

from utils.security import (
    basic_input_security_check,
    caesar_encrypt,
    check_password_strength,
    xor_encrypt_to_base64,
)
from utils.state import add_log, init_state
from utils.style import apply_theme, end_card, explain, start_card


def loader(text: str) -> None:
    with st.spinner(text):
        time.sleep(0.25)


st.set_page_config(page_title="Security Tools | SecureSphere", page_icon="🛠️", layout="wide")
init_state()
apply_theme()

st.title("Security Tools")
st.markdown(
    '<p class="hero-text">A toolkit for quick security checks, hashing, and encryption comparison.</p>',
    unsafe_allow_html=True,
)

tabs = st.tabs(
    [
        "Hash Generator",
        "Password Strength Analyzer",
        "Encryption Comparison",
        "Input Security Checker",
    ]
)

with tabs[0]:
    start_card("Hash Generator (SHA-256 / MD5)")
    text = st.text_area("Enter text", "SecureSphere")
    algo = st.selectbox("Algorithm", ["SHA-256", "MD5"])
    if st.button("Generate Hash"):
        loader("Generating hash...")
        digest = (
            hashlib.sha256(text.encode()).hexdigest()
            if algo == "SHA-256"
            else hashlib.md5(text.encode()).hexdigest()
        )
        add_log("hash_generated", f"Generated {algo} hash", actor=st.session_state.current_user or "guest")
        st.code(digest)
    end_card()

with tabs[1]:
    start_card("Password Strength Analyzer")
    candidate = st.text_input("Enter password", type="password", key="tool_pw")
    if candidate:
        label, score, feedback = check_password_strength(candidate)
        st.write(f"Score: **{score}/5**")
        if label == "Weak":
            st.error(f"Strength: {label}")
        elif label == "Moderate":
            st.warning(f"Strength: {label}")
        else:
            st.success(f"Strength: {label}")
        if feedback:
            st.write("Suggestions:")
            for note in feedback:
                st.write(f"- {note}")
        add_log("password_checked", f"Password strength analyzed ({label})", actor=st.session_state.current_user or "guest")
    end_card()

with tabs[2]:
    start_card("Encryption Comparison (Weak vs Stronger Demo)")
    plain = st.text_input("Message", "HELLO TEAM")
    weak_key = st.slider("Weak key (Caesar shift)", 1, 5, 2)
    if st.button("Compare Encryption"):
        loader("Comparing encryption outputs...")
        weak_out = caesar_encrypt(plain, weak_key)
        strong_out = xor_encrypt_to_base64(plain, "StrongTeamKey@2026")
        c1, c2 = st.columns(2)
        c1.write("Weak (Caesar)")
        c1.code(weak_out)
        c2.write("Stronger Demo (XOR + base64)")
        c2.code(strong_out)
        explain(
            "Weak methods are easier to reverse. Production systems use tested standards "
            "such as AES-GCM with secure key management."
        )
        add_log("encryption_compared", "Weak vs stronger encryption output compared", actor=st.session_state.current_user or "guest")
    end_card()

with tabs[3]:
    start_card("Input-Based Security Checker")
    sample_input = st.text_area("Enter an input string to inspect", "admin' OR '1'='1")
    if st.button("Analyze Input"):
        loader("Analyzing input...")
        issues = basic_input_security_check(sample_input)
        if issues:
            st.error("Potential risky patterns detected:")
            for issue in issues:
                st.write(f"- {issue}")
        else:
            st.success("No obvious risky pattern found in this simple check.")
        st.caption("Rule-based checker for educational use.")
        add_log("input_checked", f"Input checked, issues found: {len(issues)}", actor=st.session_state.current_user or "guest")
    end_card()
