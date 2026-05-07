"""
database/db.py - SQLite database setup and CRUD operations
"""
import sqlite3
import os
import json
from contextlib import contextmanager
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "careerpath_ai.db")


@contextmanager
def get_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """Initialize the database and create tables if they don't exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT,
                avatar TEXT DEFAULT '👤'
            )
        """)
        
        # Add avatar to existing databases if missing
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN avatar TEXT DEFAULT '👤'")
        except Exception:
            pass

        # Sessions table for "Remember me"
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Saved roadmaps table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_roadmaps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                roadmap_key TEXT NOT NULL,
                saved_at TEXT NOT NULL,
                progress_json TEXT NOT NULL DEFAULT '{}',
                UNIQUE(user_id, roadmap_key),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # AI chat history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)


# ─── USER CRUD ───────────────────────────────────────────────────────────────

def create_user(username: str, email: str, password_hash: str, salt: str) -> int:
    """Create a new user. Returns the new user ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, salt, created_at) VALUES (?, ?, ?, ?, ?)",
            (username, email, password_hash, salt, datetime.now().isoformat())
        )
        return cursor.lastrowid


def get_user_by_email(email: str) -> dict | None:
    """Fetch a user by email address."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_user_by_id(user_id: int) -> dict | None:
    """Fetch a user by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_user_by_username(username: str) -> dict | None:
    """Fetch a user by username."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_last_login(user_id: int):
    """Update the last login timestamp."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET last_login = ? WHERE id = ?",
            (datetime.now().isoformat(), user_id)
        )


def update_user_profile(user_id: int, username: str, email: str, avatar: str):
    """Update a user's basic profile details (username, email, avatar)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = ?, email = ?, avatar = ? WHERE id = ?",
            (username, email, avatar, user_id)
        )


# ─── SESSION CRUD ─────────────────────────────────────────────────────────────

def create_session(user_id: int, token: str, expires_at: str) -> int:
    """Create a new session token."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO sessions (user_id, token, created_at, expires_at) VALUES (?, ?, ?, ?)",
            (user_id, token, datetime.now().isoformat(), expires_at)
        )
        return cursor.lastrowid


def get_session(token: str) -> dict | None:
    """Fetch a session by token, returns None if expired."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT s.*, u.username, u.email, u.avatar FROM sessions s JOIN users u ON s.user_id = u.id WHERE s.token = ?",
            (token,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        session = dict(row)
        if session["expires_at"] < datetime.now().isoformat():
            delete_session(token)
            return None
        return session


def delete_session(token: str):
    """Delete a session token."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))


def delete_user_sessions(user_id: int):
    """Delete all sessions for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))


# ─── SAVED ROADMAPS CRUD ─────────────────────────────────────────────────────

def save_roadmap(user_id: int, roadmap_key: str) -> bool:
    """Save a roadmap for the user. Returns True if newly saved, False if already existed."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM saved_roadmaps WHERE user_id = ? AND roadmap_key = ?",
            (user_id, roadmap_key)
        )
        existing = cursor.fetchone()
        if existing:
            return False
        cursor.execute(
            "INSERT INTO saved_roadmaps (user_id, roadmap_key, saved_at, progress_json) VALUES (?, ?, ?, ?)",
            (user_id, roadmap_key, datetime.now().isoformat(), "{}")
        )
        return True


def get_saved_roadmaps(user_id: int, sort_by: str = "recent") -> list[dict]:
    """Fetch all saved roadmaps for a user."""
    order_map = {
        "recent": "saved_at DESC",
        "alpha": "roadmap_key ASC"
    }
    order = order_map.get(sort_by, "saved_at DESC")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM saved_roadmaps WHERE user_id = ? ORDER BY {order}",
            (user_id,)
        )
        return [dict(row) for row in cursor.fetchall()]


def update_roadmap_progress(user_id: int, roadmap_key: str, progress_json: dict):
    """Update progress data for a saved roadmap."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE saved_roadmaps SET progress_json = ? WHERE user_id = ? AND roadmap_key = ?",
            (json.dumps(progress_json), user_id, roadmap_key)
        )


def remove_saved_roadmap(user_id: int, roadmap_key: str):
    """Remove a saved roadmap."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM saved_roadmaps WHERE user_id = ? AND roadmap_key = ?",
            (user_id, roadmap_key)
        )


def get_roadmap_progress(user_id: int, roadmap_key: str) -> dict:
    """Get progress JSON for a specific roadmap."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT progress_json FROM saved_roadmaps WHERE user_id = ? AND roadmap_key = ?",
            (user_id, roadmap_key)
        )
        row = cursor.fetchone()
        if row:
            return json.loads(row["progress_json"])
        return {}


# ─── CHAT HISTORY CRUD ───────────────────────────────────────────────────────

def save_chat_message(user_id: int, role: str, content: str):
    """Save a chat message."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, role, content, datetime.now().isoformat())
        )


def get_chat_history(user_id: int, limit: int = 50) -> list[dict]:
    """Get recent chat history for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit)
        )
        rows = cursor.fetchall()
        return list(reversed([dict(r) for r in rows]))


def clear_chat_history(user_id: int):
    """Clear all chat messages for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
