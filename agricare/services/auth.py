
import hashlib
import hmac
import secrets
import sqlite3

from agricare.database.db import get_connection


# -----------------------------
# Password Security
# -----------------------------

def hash_password(password):
    """Securely hash a password using PBKDF2."""

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return salt.hex() + "$" + password_hash.hex()


def verify_password(password, stored_hash):
    """Verify a password against its stored hash."""

    try:
        salt_hex, hash_hex = stored_hash.split("$")

        salt = bytes.fromhex(salt_hex)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            200000
        )

        return hmac.compare_digest(new_hash.hex(), hash_hex)

    except (ValueError, TypeError):
        return False


# -----------------------------
# Farmer Registration
# -----------------------------

def register_user(
    full_name,
    email,
    phone,
    password,
    village="",
    district="",
    state="",
    preferred_language="English"
):

    full_name = full_name.strip()
    email = email.strip().lower()
    phone = phone.strip()

    if not full_name or not email or not phone or not password:
        return False, "All required fields must be filled.", None

    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address.", None

    if len(password) < 8:
        return False, "Password must contain at least 8 characters.", None

    password_hash = hash_password(password)

    try:
        with get_connection() as conn:

            cursor = conn.execute(
                """
                INSERT INTO users (
                    full_name,
                    email,
                    phone,
                    password_hash,
                    village,
                    district,
                    state,
                    preferred_language
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    full_name,
                    email,
                    phone,
                    password_hash,
                    village.strip(),
                    district.strip(),
                    state.strip(),
                    preferred_language
                )
            )

            user_id = cursor.lastrowid

            return True, "Registration successful!", user_id

    except sqlite3.IntegrityError as error:

        error_message = str(error).lower()

        if "email" in error_message:
            return False, "This email is already registered.", None

        if "phone" in error_message:
            return False, "This phone number is already registered.", None

        return False, "Registration failed due to duplicate information.", None


# -----------------------------
# Farmer Login
# -----------------------------

def authenticate_user(email, password):

    email = email.strip().lower()

    with get_connection() as conn:

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

    if user is None:
        return None

    if verify_password(password, user["password_hash"]):
        return dict(user)

    return None
