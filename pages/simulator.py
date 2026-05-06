import time

import streamlit as st

from utils.crypto import caesar_encrypt, decrypt_text_fernet, derive_fernet_key_from_secret, encrypt_text_fernet
from utils.key_exchange import dh_generate_public, dh_generate_shared_secret
from utils.state import add_log, bump_simulations, init_state
from utils.style import apply_theme, end_card, start_card


def loader() -> None:
    with st.spinner("Processing..."):
        time.sleep(0.3)


def learning_block(what: str, how: list[str], why: str) -> None:
    st.info(f"**What is happening:** {what}")
    st.markdown("#### How it works")
    for i, step in enumerate(how, start=1):
        st.write(f"Step {i}: {step}")
    st.success(f"**Why it is important:** {why}")


st.set_page_config(page_title="Simulator | SecureSphere", page_icon="🧪", layout="wide")
init_state()
apply_theme()

st.title("Attack Simulation Lab")
st.markdown(
    '<p class="hero-text">Understand how attacks happen, then compare with secure communication methods.</p>',
    unsafe_allow_html=True,
)

scenario = st.selectbox(
    "Choose simulation",
    ["Weak Encryption", "Man-in-the-Middle", "Diffie-Hellman Secure vs Insecure"],
)

if scenario == "Weak Encryption":
    start_card("Weak Encryption")
    loader()
    bump_simulations()
    add_log("simulation_run", scenario, actor=st.session_state.current_user or "guest")

    message = "HELLO"
    encrypted = caesar_encrypt(message, 2)
    guessed = caesar_encrypt(encrypted, -2)

    c1, c2, c3 = st.columns(3)
    c1.write("Input")
    c1.code(message)
    c2.write("Processing")
    c2.code(f"Weak Caesar encryption -> {encrypted}")
    c3.write("Output")
    c3.code(guessed)

    st.warning("Attack: attacker brute-forces tiny key space and recovers original text.")
    learning_block(
        "The message is protected with a weak algorithm.",
        [
            "System encrypts message using a simple character shift.",
            "Attacker tests a few keys quickly.",
            "Plain text is recovered.",
        ],
        "Weak encryption fails confidentiality.",
    )
    end_card()

elif scenario == "Man-in-the-Middle":
    start_card("MITM Simulation")
    loader()
    bump_simulations()
    add_log("simulation_run", scenario, actor=st.session_state.current_user or "guest")

    c1, c2, c3 = st.columns(3)
    c1.write("Original message")
    c1.code("Transfer amount: 1000")
    c2.write("Attack happening")
    c2.code("Attacker intercepts and reads message")
    c3.write("Result")
    c3.code("Sensitive information leaked")

    st.warning("Attack success: communication is visible because transport is insecure.")
    learning_block(
        "An attacker sits between sender and receiver.",
        [
            "Sender transmits data over an insecure channel.",
            "Attacker reads or modifies packets in transit.",
            "Receiver cannot detect interception.",
        ],
        "Secure channels (TLS + key agreement) prevent message exposure.",
    )
    end_card()

else:
    start_card("Diffie-Hellman Key Exchange (Secure vs Insecure)")
    loader()
    bump_simulations()
    add_log("simulation_run", scenario, actor=st.session_state.current_user or "guest")

    prime = 23
    generator = 5
    alice_private = 6
    bob_private = 15

    alice_public = dh_generate_public(prime, generator, alice_private)
    bob_public = dh_generate_public(prime, generator, bob_private)
    alice_secret = dh_generate_shared_secret(bob_public, alice_private, prime)
    bob_secret = dh_generate_shared_secret(alice_public, bob_private, prime)

    st.info("**What is happening:** Alice and Bob generate a shared secret without sending it directly.")
    st.markdown("#### Step-by-step values")
    c1, c2 = st.columns(2)
    c1.code(
        f"Public values:\nprime={prime}, generator={generator}\n\nAlice private={alice_private}\nAlice public={alice_public}"
    )
    c2.code(
        f"Bob private={bob_private}\nBob public={bob_public}\n\nAlice secret={alice_secret}\nBob secret={bob_secret}"
    )

    shared_key = derive_fernet_key_from_secret(alice_secret)
    sample = "HELLO BOB - SECRET MESSAGE"
    secure_cipher = encrypt_text_fernet(sample, shared_key)
    secure_plain = decrypt_text_fernet(secure_cipher, shared_key)

    st.markdown("#### Insecure vs secure communication")
    x1, x2 = st.columns(2)
    x1.warning("Insecure channel example")
    x1.code(sample)
    x2.success("Secure DH-derived key + AES(Fernet)")
    x2.code(secure_cipher)

    st.markdown("#### Result")
    st.success(f"Decrypted back with shared key: {secure_plain}")
    learning_block(
        "Even if attacker sees public values, the shared secret stays private.",
        [
            "Alice and Bob exchange only public values.",
            "Both compute same shared secret independently.",
            "Shared secret is converted to encryption key and used for secure message exchange.",
        ],
        "DH enables secure key setup over insecure networks.",
    )
    end_card()
