"""
auth/auth.py - Authentication, registration, session management
"""
import hashlib
import os
import secrets
import json
from datetime import datetime, timedelta

from database.db import (
    create_user, get_user_by_email, get_user_by_username,
    update_last_login, create_session, get_session,
    delete_session, delete_user_sessions
)

SESSION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".session")


def _generate_salt() -> str:
    return secrets.token_hex(32)


def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()


def _generate_token() -> str:
    return secrets.token_urlsafe(64)


# ─── REGISTRATION ─────────────────────────────────────────────────────────────

def register_user(username: str, email: str, password: str) -> dict:
    """
    Register a new user.
    Returns {"success": True, "user_id": int} or {"success": False, "error": str}
    """
    if len(username.strip()) < 3:
        return {"success": False, "error": "Username must be at least 3 characters."}
    if len(password) < 6:
        return {"success": False, "error": "Password must be at least 6 characters."}
    if "@" not in email or "." not in email:
        return {"success": False, "error": "Please enter a valid email address."}

    if get_user_by_email(email):
        return {"success": False, "error": "An account with this email already exists."}
    if get_user_by_username(username):
        return {"success": False, "error": "Username is already taken."}

    salt = _generate_salt()
    pw_hash = _hash_password(password, salt)

    try:
        user_id = create_user(username.strip(), email.strip().lower(), pw_hash, salt)
        return {"success": True, "user_id": user_id}
    except Exception as e:
        return {"success": False, "error": f"Registration failed: {str(e)}"}


# ─── LOGIN ────────────────────────────────────────────────────────────────────

def login_user(email: str, password: str, remember_me: bool = False) -> dict:
    """
    Authenticate a user.
    Returns {"success": True, "user": {...}, "token": str} or {"success": False, "error": str}
    """
    user = get_user_by_email(email.strip().lower())
    if not user:
        return {"success": False, "error": "No account found with this email."}

    expected_hash = _hash_password(password, user["salt"])
    if expected_hash != user["password_hash"]:
        return {"success": False, "error": "Incorrect password. Please try again."}

    update_last_login(user["id"])

    token = _generate_token()
    expires = (datetime.now() + timedelta(days=30 if remember_me else 1)).isoformat()
    create_session(user["id"], token, expires)

    if remember_me:
        _save_session_file(token)

    return {
        "success": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        },
        "token": token
    }


# ─── SESSION ──────────────────────────────────────────────────────────────────

def _save_session_file(token: str):
    """Save session token to local file."""
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump({"token": token}, f)
    except Exception:
        pass


def _load_session_file() -> str | None:
    """Load session token from local file."""
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                return data.get("token")
    except Exception:
        pass
    return None


def _clear_session_file():
    """Remove stored session file."""
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
    except Exception:
        pass


def check_saved_session() -> dict | None:
    """
    Check if a valid saved session exists.
    Returns user dict or None.
    """
    token = _load_session_file()
    if not token:
        return None
    session = get_session(token)
    if not session:
        _clear_session_file()
        return None
    return {
        "id": session["user_id"],
        "username": session["username"],
        "email": session["email"],
        "token": token
    }


def logout_user(user_id: int, token: str = None):
    """Log out the user, optionally deleting a specific token or all tokens."""
    if token:
        delete_session(token)
    else:
        delete_user_sessions(user_id)
    _clear_session_file()
