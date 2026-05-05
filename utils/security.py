import base64
import hashlib


def hash_password(password: str, algorithm: str = "sha256") -> str:
    if algorithm.lower() == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    return hashlib.sha256(password.encode()).hexdigest()


def check_password_strength(password: str) -> tuple[str, int, list[str]]:
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters.")
    if any(ch.isupper() for ch in password):
        score += 1
    else:
        feedback.append("Add an uppercase letter.")
    if any(ch.islower() for ch in password):
        score += 1
    else:
        feedback.append("Add a lowercase letter.")
    if any(ch.isdigit() for ch in password):
        score += 1
    else:
        feedback.append("Add a number.")
    if any(not ch.isalnum() for ch in password):
        score += 1
    else:
        feedback.append("Add a special character.")

    if score <= 2:
        label = "Weak"
    elif score <= 4:
        label = "Moderate"
    else:
        label = "Strong"
    return label, score, feedback


def caesar_encrypt(message: str, key: int) -> str:
    return "".join(chr(ord(ch) + key) for ch in message)


def xor_encrypt_to_base64(plain_text: str, key: str) -> str:
    if not key:
        return ""
    key_bytes = key.encode()
    data = plain_text.encode()
    encrypted_bytes = bytes(
        byte ^ key_bytes[index % len(key_bytes)] for index, byte in enumerate(data)
    )
    return base64.b64encode(encrypted_bytes).decode()


def xor_decrypt_from_base64(encrypted_text: str, key: str) -> str:
    if not key:
        return ""
    key_bytes = key.encode()
    try:
        encrypted_bytes = base64.b64decode(encrypted_text.encode())
    except Exception:
        return "Invalid encrypted input."
    decrypted_bytes = bytes(
        byte ^ key_bytes[index % len(key_bytes)] for index, byte in enumerate(encrypted_bytes)
    )
    try:
        return decrypted_bytes.decode()
    except UnicodeDecodeError:
        return "Decryption failed for this key."


def basic_input_security_check(user_input: str) -> list[str]:
    issues = []
    lowered = user_input.lower()
    patterns = [
        ("sql injection keyword", [" or ", " union ", " drop ", "--", "' or '1'='1"]),
        ("script injection keyword", ["<script", "javascript:"]),
        ("path traversal keyword", ["../", "..\\"]),
    ]
    for issue_name, keys in patterns:
        if any(key in lowered for key in keys):
            issues.append(issue_name)
    return issues
