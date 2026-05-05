import hashlib
import time

import streamlit as st

from utils.security import caesar_encrypt
from utils.state import add_log, bump_simulations, init_state
from utils.style import apply_theme, end_card, explain, start_card


def show_simulation_loader(text: str) -> None:
    with st.spinner(text):
        time.sleep(0.25)


def show_steps(steps: list[str]) -> None:
    for index, step in enumerate(steps, start=1):
        st.write(f"Step {index}: {step}")


def record_run(scenario_name: str) -> None:
    bump_simulations()
    user = st.session_state.current_user or "guest"
    add_log("simulation_run", scenario_name, actor=user)


def show_summary(attack: str, failed_principle: str, prevention: str) -> None:
    c1, c2, c3 = st.columns(3)
    c1.write("Attack")
    c1.success(attack)
    c2.write("Failed Principle")
    c2.error(failed_principle)
    c3.write("Defense")
    c3.info(prevention)


st.set_page_config(page_title="Attack Simulation Lab | SecureSphere", page_icon="🧪", layout="wide")
init_state()
apply_theme()

st.title("Attack Simulation Lab")
st.markdown(
    '<p class="hero-text">Interactive attack demonstrations with explanation and step-by-step view.</p>',
    unsafe_allow_html=True,
)

scenario = st.selectbox(
    "Choose Simulation",
    [
        "Weak Encryption",
        "No Integrity Check",
        "No Authentication",
        "Man-in-the-Middle Attack",
        "Poor Access Control",
        "Password Brute Force Attack",
        "SQL Injection Demo",
        "Session Hijacking Concept",
        "File Tampering Attack",
    ],
)

if scenario == "Weak Encryption":
    start_card("Weak Encryption")
    show_simulation_loader("Running weak encryption demo...")
    record_run(scenario)
    message = "HELLO"
    encrypted = caesar_encrypt(message, 2)
    st.code(f"Original: {message}\nEncrypted: {encrypted}")
    show_steps(
        [
            "Message is encrypted with weak Caesar shift.",
            "Attacker tries small key range.",
            "Correct key is found quickly and plaintext is exposed.",
        ]
    )
    explain("Weak algorithms and small key-space are easy to break through brute force.")
    show_summary("Brute Force", "Confidentiality", "Use modern encryption such as AES.")
    end_card()

elif scenario == "No Integrity Check":
    start_card("No Integrity Check")
    show_simulation_loader("Running integrity simulation...")
    record_run(scenario)
    original_msg = "Pay 5000"
    tampered_msg = "Pay 9000"
    st.code(f"Original: {original_msg}\nTampered: {tampered_msg}")
    show_steps(
        [
            "Sender transmits financial message.",
            "Attacker modifies amount during transit.",
            "Receiver accepts changed message if integrity checks are missing.",
        ]
    )
    h1 = hashlib.sha256(original_msg.encode()).hexdigest()
    h2 = hashlib.sha256(tampered_msg.encode()).hexdigest()
    st.write("Hash check after adding integrity control:")
    st.code(f"Original hash: {h1}\nTampered hash: {h2}")
    explain("Integrity controls detect unauthorized changes in data.")
    show_summary("Message Tampering", "Integrity", "Use hashing and MAC validation.")
    end_card()

elif scenario == "No Authentication":
    start_card("No Authentication")
    show_simulation_loader("Running auth simulation...")
    record_run(scenario)
    username = st.text_input("Enter a username")
    show_steps(
        [
            "User enters only username.",
            "System grants access without password check.",
            "Any identity can access sensitive resources.",
        ]
    )
    if username:
        st.warning(f"Access granted to {username} without verification.")
    explain("Authentication ensures identity verification before access is granted.")
    show_summary("Unauthorized Access", "Authentication", "Require password and MFA.")
    end_card()

elif scenario == "Man-in-the-Middle Attack":
    start_card("Man-in-the-Middle Attack")
    show_simulation_loader("Running MITM simulation...")
    record_run(scenario)
    st.code("Sender -> HELLO USER\nAttacker intercepts -> HELLO USER")
    show_steps(
        [
            "Sender transmits plaintext message.",
            "Attacker intercepts traffic in transit.",
            "Without encryption, message content is readable.",
        ]
    )
    explain("TLS/HTTPS prevents attackers from reading or tampering with communication.")
    show_summary("MITM", "Confidentiality", "Use HTTPS and certificate validation.")
    end_card()

elif scenario == "Poor Access Control":
    start_card("Poor Access Control")
    show_simulation_loader("Running authorization simulation...")
    record_run(scenario)
    action = st.selectbox("Requested action", ["View Data", "Delete Records"])
    show_steps(
        [
            "User authenticates into application.",
            "System fails to check role permissions.",
            "Sensitive actions can be misused.",
        ]
    )
    if action == "Delete Records":
        st.error("Unauthorized delete executed.")
    else:
        st.success("Safe action selected.")
    explain("Authorization controls should enforce role-based permissions.")
    show_summary("Privilege Misuse", "Authorization", "Implement RBAC and least privilege.")
    end_card()

elif scenario == "Password Brute Force Attack":
    start_card("Password Brute Force Attack")
    show_simulation_loader("Running brute-force simulation...")
    record_run(scenario)
    target_password = "A1b"
    guesses = ["123", "admin", "A1b", "pass123"]
    for attempt, guess in enumerate(guesses, start=1):
        if guess == target_password:
            st.success(f"Attempt {attempt}: password found -> {guess}")
            break
        st.write(f"Attempt {attempt}: {guess} (failed)")
    show_steps(
        [
            "Attacker picks common passwords from dictionary.",
            "Weak/short password is eventually matched.",
            "Account is compromised.",
        ]
    )
    explain("Strong passwords, lockout, and MFA reduce brute-force success.")
    show_summary("Password Brute Force", "Authentication", "Use strong password policy + MFA.")
    end_card()

elif scenario == "SQL Injection Demo":
    start_card("SQL Injection Demo (Safe)")
    show_simulation_loader("Running SQLi simulation...")
    record_run(scenario)
    user_input = st.text_input("Username input", "admin' OR '1'='1")
    query = f"SELECT * FROM users WHERE username = '{user_input}' AND password='x';"
    st.write("Vulnerable query using direct string concatenation:")
    st.code(query, language="sql")
    show_steps(
        [
            "Application builds SQL query from direct input.",
            "Malicious payload alters query logic.",
            "Authentication bypass may happen.",
        ]
    )
    st.write("Safer pattern:")
    st.code("SELECT * FROM users WHERE username = ? AND password = ?;", language="sql")
    explain("Use parameterized queries and validation to prevent injection.")
    show_summary("SQL Injection", "Integrity/Authentication", "Use prepared statements.")
    end_card()

elif scenario == "Session Hijacking Concept":
    start_card("Session Hijacking Concept")
    show_simulation_loader("Running session attack simulation...")
    record_run(scenario)
    st.code("Legitimate token: sess_9483_userA\nAttacker copies token and impersonates user")
    show_steps(
        [
            "User logs in and receives active session token.",
            "Attacker steals token via insecure channel/device.",
            "Attacker reuses token to access account.",
        ]
    )
    explain("Secure cookies, short token expiry, and token rotation reduce session hijacking risk.")
    show_summary("Session Hijacking", "Session Management", "Use secure cookie flags + rotation.")
    end_card()

elif scenario == "File Tampering Attack":
    start_card("File Tampering Attack")
    show_simulation_loader("Running file tampering simulation...")
    record_run(scenario)
    original = "Marks: StudentA=78"
    tampered = "Marks: StudentA=98"
    st.code(f"Original file line: {original}\nTampered line: {tampered}")
    show_steps(
        [
            "File is stored without integrity verification.",
            "Attacker edits the file content.",
            "System trusts modified file as valid.",
        ]
    )
    original_hash = hashlib.sha256(original.encode()).hexdigest()
    tampered_hash = hashlib.sha256(tampered.encode()).hexdigest()
    st.code(f"Original hash: {original_hash}\nTampered hash: {tampered_hash}")
    explain("Checksum/hash comparison can detect tampering in important files.")
    show_summary("File Tampering", "Integrity", "Use hashes, signatures, and access control.")
    end_card()
