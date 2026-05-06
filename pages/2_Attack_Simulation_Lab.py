import hashlib
import time

import streamlit as st

from utils.security import caesar_encrypt
from utils.state import add_log, bump_simulations, init_state
from utils.style import apply_theme, end_card, start_card


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


def learning_sections(
    what_is_this: str,
    steps: list[str],
    original_view: str,
    attack_view: str,
    result_view: str,
    result_type: str,
    why_text: str,
    prevent_text: str,
) -> None:
    st.info(f"**What is this?** {what_is_this}")
    st.markdown("#### What happens step-by-step")
    show_steps(steps)

    st.markdown("#### Visual simulation")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**Original message/data**")
    c1.code(original_view)
    c2.markdown("**Attack happening**")
    c2.code(attack_view)
    c3.markdown("**Result**")
    c3.code(result_view)

    if result_type == "error":
        st.error("Security failure observed in this simulation.")
    elif result_type == "warning":
        st.warning("Risk is visible in this simulation.")
    else:
        st.success("Secure outcome shown in this simulation.")

    st.markdown("#### Why it happened")
    st.warning(why_text)
    st.markdown("#### How to prevent it")
    st.success(prevent_text)


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
    learning_sections(
        what_is_this="A weak encryption method with tiny key space.",
        steps=[
            "System encrypts message with a very simple shift.",
            "Attacker tries multiple keys one by one.",
            "Correct key appears quickly and plaintext is exposed.",
        ],
        original_view=message,
        attack_view=f"Cipher text captured: {encrypted}",
        result_view="Attacker decodes message: HELLO",
        result_type="error",
        why_text="The encryption is too simple, so attackers can test all keys quickly.",
        prevent_text="Use strong modern encryption (AES) and safe key management.",
    )
    show_summary("Brute Force", "Confidentiality", "Use modern encryption such as AES.")
    end_card()

elif scenario == "No Integrity Check":
    start_card("No Integrity Check")
    show_simulation_loader("Running integrity simulation...")
    record_run(scenario)
    original_msg = "Pay 5000"
    tampered_msg = "Pay 9000"
    learning_sections(
        what_is_this="A tampering attack where message content changes in transit.",
        steps=[
            "Sender shares the original payment instruction.",
            "Attacker edits amount during transmission.",
            "Receiver trusts modified message when integrity checks are absent.",
        ],
        original_view=original_msg,
        attack_view=tampered_msg,
        result_view="Receiver acts on wrong amount.",
        result_type="error",
        why_text="No integrity verification exists before using message content.",
        prevent_text="Use hashes/MAC/signatures to validate message integrity.",
    )
    h1 = hashlib.sha256(original_msg.encode()).hexdigest()
    h2 = hashlib.sha256(tampered_msg.encode()).hexdigest()
    st.write("Hash check after adding integrity control:")
    st.code(f"Original hash: {h1}\nTampered hash: {h2}")
    show_summary("Message Tampering", "Integrity", "Use hashing and MAC validation.")
    end_card()

elif scenario == "No Authentication":
    start_card("No Authentication")
    show_simulation_loader("Running auth simulation...")
    record_run(scenario)
    username = st.text_input("Enter a username")
    learning_sections(
        what_is_this="An authentication failure where identity is not verified.",
        steps=[
            "A user enters only a username.",
            "System skips password or second-factor checks.",
            "Unauthorized person receives access.",
        ],
        original_view="Login request from user",
        attack_view="No password validation",
        result_view="Access granted to unknown identity",
        result_type="error",
        why_text="The system does not verify who is requesting access.",
        prevent_text="Require password checks and optional MFA for sensitive access.",
    )
    if username:
        st.warning(f"Access granted to {username} without verification.")
    show_summary("Unauthorized Access", "Authentication", "Require password and MFA.")
    end_card()

elif scenario == "Man-in-the-Middle Attack":
    start_card("Man-in-the-Middle Attack")
    show_simulation_loader("Running MITM simulation...")
    record_run(scenario)
    learning_sections(
        what_is_this="A communication attack where attacker reads data in transit.",
        steps=[
            "Sender sends message over insecure channel.",
            "Attacker intercepts network traffic.",
            "Plain text message is visible to attacker.",
        ],
        original_view="HELLO USER",
        attack_view="Traffic intercepted by attacker",
        result_view="Message content leaked",
        result_type="error",
        why_text="Data is sent without secure transport encryption.",
        prevent_text="Use HTTPS/TLS and certificate validation.",
    )
    show_summary("MITM", "Confidentiality", "Use HTTPS and certificate validation.")
    end_card()

elif scenario == "Poor Access Control":
    start_card("Poor Access Control")
    show_simulation_loader("Running authorization simulation...")
    record_run(scenario)
    action = st.selectbox("Requested action", ["View Data", "Delete Records"])
    learning_sections(
        what_is_this="An authorization issue where users can do actions beyond permission.",
        steps=[
            "User logs into the app.",
            "System does not verify role permissions.",
            "Sensitive action can be executed by wrong user.",
        ],
        original_view="Normal allowed action: View Data",
        attack_view=f"Unauthorized request: {action}",
        result_view="Possible privilege misuse",
        result_type="warning",
        why_text="Role checks are weak or missing for critical actions.",
        prevent_text="Apply RBAC and least privilege checks before sensitive actions.",
    )
    if action == "Delete Records":
        st.error("Unauthorized delete executed.")
    else:
        st.success("Safe action selected.")
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
    learning_sections(
        what_is_this="A guessing attack using common passwords.",
        steps=[
            "Attacker tries dictionary/common passwords.",
            "Weak password is matched after few attempts.",
            "Account is compromised.",
        ],
        original_view="Protected account with weak password",
        attack_view="Repeated login guesses",
        result_view="Password discovered",
        result_type="error",
        why_text="Weak and short passwords are easy to guess.",
        prevent_text="Use strong password policy, lockout controls, and MFA.",
    )
    show_summary("Password Brute Force", "Authentication", "Use strong password policy + MFA.")
    end_card()

elif scenario == "SQL Injection Demo":
    start_card("SQL Injection Demo (Safe)")
    show_simulation_loader("Running SQLi simulation...")
    record_run(scenario)
    user_input = st.text_input("Username input", "admin' OR '1'='1")
    query = f"SELECT * FROM users WHERE username = '{user_input}' AND password='x';"
    learning_sections(
        what_is_this="An input-based attack that changes SQL behavior.",
        steps=[
            "App directly inserts user input into SQL query.",
            "Malicious pattern changes query logic.",
            "System may bypass normal authentication checks.",
        ],
        original_view="Expected username: admin",
        attack_view=user_input,
        result_view="Query logic manipulated",
        result_type="error",
        why_text="Input is not safely handled before database query.",
        prevent_text="Use parameterized queries and input validation.",
    )
    st.write("Vulnerable query using direct string concatenation:")
    st.code(query, language="sql")
    st.write("Safer pattern:")
    st.code("SELECT * FROM users WHERE username = ? AND password = ?;", language="sql")
    show_summary("SQL Injection", "Integrity/Authentication", "Use prepared statements.")
    end_card()

elif scenario == "Session Hijacking Concept":
    start_card("Session Hijacking Concept")
    show_simulation_loader("Running session attack simulation...")
    record_run(scenario)
    learning_sections(
        what_is_this="An attack where stolen session token is reused.",
        steps=[
            "User logs in and receives active session token.",
            "Attacker steals token from unsafe environment/channel.",
            "Attacker uses same token to impersonate user.",
        ],
        original_view="Legitimate token: sess_9483_userA",
        attack_view="Token copied by attacker",
        result_view="Attacker gains user session",
        result_type="error",
        why_text="Session token protection and lifecycle controls are weak.",
        prevent_text="Use secure cookies, short expiry, and token rotation.",
    )
    show_summary("Session Hijacking", "Session Management", "Use secure cookie flags + rotation.")
    end_card()

elif scenario == "File Tampering Attack":
    start_card("File Tampering Attack")
    show_simulation_loader("Running file tampering simulation...")
    record_run(scenario)
    original = "Marks: StudentA=78"
    tampered = "Marks: StudentA=98"
    learning_sections(
        what_is_this="A file integrity attack where content is altered after storage.",
        steps=[
            "File is stored without integrity checks.",
            "Attacker modifies data in the file.",
            "System trusts tampered content as real.",
        ],
        original_view=original,
        attack_view=tampered,
        result_view="Modified record is accepted",
        result_type="error",
        why_text="No checksum/signature verification before reading file.",
        prevent_text="Use file hashing, digital signatures, and access controls.",
    )
    original_hash = hashlib.sha256(original.encode()).hexdigest()
    tampered_hash = hashlib.sha256(tampered.encode()).hexdigest()
    st.code(f"Original hash: {original_hash}\nTampered hash: {tampered_hash}")
    show_summary("File Tampering", "Integrity", "Use hashes, signatures, and access control.")
    end_card()
