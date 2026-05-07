import time

import streamlit as st

from components.ui import card, run_step_animation
from utils.crypto import caesar_encrypt, decrypt_text_fernet, derive_fernet_key_from_secret, encrypt_text_fernet
from utils.key_exchange import dh_generate_public, dh_generate_shared_secret
from utils.state import add_log, bump_simulations, init_state
from utils.style import apply_theme


def loader() -> None:
    with st.spinner("Processing..."):
        time.sleep(0.3)


def learning_block(what: str, how: list[str], why: str) -> None:
    st.info(f"**What is happening:** {what}")
    st.markdown("#### How it works")
    for i, step in enumerate(how, start=1):
        st.write(f"Step {i}: {step}")
    st.success(f"**Why it is important:** {why}")


st.set_page_config(page_title="Simulator | SecureSphere", layout="wide")
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
    with card("Weak Encryption"):
        plain_text = st.text_input("Input text", "HELLO USER", key="weak_plain")
        shift_key = st.number_input("Custom shift key", min_value=1, max_value=10, value=3, key="weak_key")

        st.markdown("#### Visual flow")
        st.markdown("Sender -> Encryption -> Transmission -> Attacker -> Receiver")

        if st.button("Start Simulation", key="weak_start"):
            loader()
            run_step_animation(
                [
                    ("info", "Step 1: Sender encrypts message using weak Caesar shift."),
                    ("warning", "Step 2: Attacker intercepts cipher text and starts brute force."),
                    ("error", "Step 3: Attacker recovers original message."),
                ]
            )

            bump_simulations()
            add_log("simulation_run", scenario, actor=st.session_state.current_user or "guest")
            encrypted = caesar_encrypt(plain_text, int(shift_key))

            c1, c2, c3 = st.columns(3)
            c1.write("Input")
            c1.code(plain_text)
            c2.write("Encrypted")
            c2.code(encrypted)
            c3.write("Brute-force results")
            brute_lines = []
            for k in range(1, 6):
                brute_lines.append(f"k={k}: {caesar_encrypt(encrypted, -k)}")
            c3.code("\n".join(brute_lines))

            st.warning("Attack result: weak key space makes brute-force easy.")
            learning_block(
                "A weak encryption method is used with a small shift key.",
                [
                    "Sender applies a simple shift to each character.",
                    "Attacker tries nearby keys quickly.",
                    "One guess reveals original message.",
                ],
                "Weak encryption can break confidentiality quickly.",
            )

elif scenario == "Man-in-the-Middle":
    with card("MITM Simulation"):
        original_message = st.text_input("Input message", "Transfer amount: 1000", key="mitm_msg")
        modify_toggle = st.toggle("Attacker modifies message", value=True, key="mitm_toggle")
        modified_message = st.text_input(
            "Modified message by attacker",
            "Transfer amount: 9000",
            key="mitm_modified",
            disabled=not modify_toggle,
        )

        st.markdown("#### Visual flow")
        st.markdown("Sender -> Transmission -> Attacker -> Receiver")

        if st.button("Start Simulation", key="mitm_start"):
            loader()
            run_step_animation(
                [
                    ("info", "Step 1: Sender sends original message."),
                    ("warning", "Step 2: Attacker intercepts transmission."),
                    ("error", "Step 3: Receiver gets altered or exposed message."),
                ]
            )

            bump_simulations()
            add_log("simulation_run", scenario, actor=st.session_state.current_user or "guest")
            intercepted = original_message
            received = modified_message if modify_toggle else original_message

            c1, c2, c3, c4 = st.columns(4)
            c1.write("Original")
            c1.code(original_message)
            c2.write("Intercepted")
            c2.code(intercepted)
            c3.write("Modified")
            c3.code(modified_message if modify_toggle else "No modification")
            c4.write("Received")
            c4.code(received)

            if modify_toggle:
                st.error("Breach: receiver trusted attacker-modified message.")
            else:
                st.warning("Breach: attacker read sensitive message in transit.")
            learning_block(
                "An attacker intercepts communication channel.",
                [
                    "Sender transmits data.",
                    "Attacker reads or changes data while in transit.",
                    "Receiver cannot verify authenticity without protection.",
                ],
                "Insecure channels can leak or alter critical information.",
            )

else:
    with card("Diffie-Hellman Key Exchange (Secure vs Insecure)"):
        col_a, col_b = st.columns(2)
        with col_a:
            prime = st.number_input("Prime (p)", min_value=5, value=23, step=1, key="dh_prime")
            generator = st.number_input("Generator (g)", min_value=2, value=5, step=1, key="dh_gen")
        with col_b:
            alice_private = st.number_input("Alice private key", min_value=2, value=6, step=1, key="dh_a")
            bob_private = st.number_input("Bob private key", min_value=2, value=15, step=1, key="dh_b")

        sample = st.text_input("Message for secure exchange", "HELLO BOB - SECRET MESSAGE", key="dh_message")
        st.markdown("#### Visual flow")
        st.markdown("Alice -> Public exchange -> Shared secret -> Encryption -> Bob")

        if st.button("Start Simulation", key="dh_start"):
            loader()
            run_step_animation(
                [
                    ("info", "Step 1: Alice and Bob compute and exchange public values."),
                    ("info", "Step 2: Both derive shared secret independently."),
                    ("success", "Step 3: Shared key encrypts message securely."),
                ]
            )

            bump_simulations()
            add_log("simulation_run", scenario, actor=st.session_state.current_user or "guest")

            alice_public = dh_generate_public(int(prime), int(generator), int(alice_private))
            bob_public = dh_generate_public(int(prime), int(generator), int(bob_private))
            alice_secret = dh_generate_shared_secret(int(bob_public), int(alice_private), int(prime))
            bob_secret = dh_generate_shared_secret(int(alice_public), int(bob_private), int(prime))

            c1, c2 = st.columns(2)
            c1.code(
                f"Public parameters:\np={prime}, g={generator}\n\nAlice public={alice_public}\nBob public={bob_public}"
            )
            c2.code(f"Alice shared secret={alice_secret}\nBob shared secret={bob_secret}")

            shared_key = derive_fernet_key_from_secret(alice_secret)
            secure_cipher = encrypt_text_fernet(sample, shared_key)
            secure_plain = decrypt_text_fernet(secure_cipher, shared_key)

            x1, x2 = st.columns(2)
            x1.warning("Insecure communication")
            x1.code(sample)
            x2.success("Secure communication (DH + Fernet)")
            x2.code(secure_cipher)

            st.success(f"Decrypted output with shared key: {secure_plain}")
            learning_block(
                "Shared secret is generated without directly sending it.",
                [
                    "Both users exchange only public numbers.",
                    "Each side computes the same shared secret locally.",
                    "Shared secret secures communication using symmetric encryption.",
                ],
                "Key exchange is essential for secure communication setup.",
            )
