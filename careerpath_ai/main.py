"""
main.py - CareerPath AI entry point
"""
import sys
import os

# ── Dependency check ──────────────────────────────────────────────────────────
REQUIRED = ["customtkinter", "PIL", "requests", "dotenv"]
missing = []
for pkg in REQUIRED:
    try:
        __import__(pkg)
    except ImportError:
        missing.append(pkg)

if missing:
    print("❌ Missing packages. Please run:")
    print("   pip install -r requirements.txt")
    print(f"   Missing: {', '.join(missing)}")
    sys.exit(1)

# ── Setup path ────────────────────────────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# ── Load .env ─────────────────────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv(os.path.join(script_dir, ".env"))

# ── Initialize database ───────────────────────────────────────────────────────
from database.db import init_database
init_database()

# ── Import roadmap data part 2 (merges into ROADMAPS) ────────────────────────
import core.roadmap_data2  # noqa: F401 — side-effect: populates ROADMAPS

# ── Check saved session ───────────────────────────────────────────────────────
from auth.auth import check_saved_session

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Window icon generation ────────────────────────────────────────────────────
def _make_icon(app: ctk.CTk):
    icon_path = os.path.join(script_dir, "assets", "icons", "app_icon.png")
    if not os.path.exists(icon_path):
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new("RGBA", (64, 64), (13, 15, 20, 255))
            draw = ImageDraw.Draw(img)
            draw.ellipse([4, 4, 60, 60], fill=(108, 99, 255, 255))
            draw.text((18, 16), "CP", fill="white")
            img.save(icon_path)
        except Exception:
            pass
    try:
        from PIL import Image
        from customtkinter import CTkImage
        img = Image.open(icon_path)
        # Use wm_iconphoto
        import tkinter as tk
        from PIL import ImageTk
        photo = ImageTk.PhotoImage(img.resize((32, 32)))
        app.wm_iconphoto(True, photo)
        app._icon_ref = photo  # prevent GC
    except Exception:
        pass


# ── Main App Controller ───────────────────────────────────────────────────────
class CareerPathApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("CareerPath AI — Your Intelligent Career Navigator")
        self.root.geometry("1280x800")
        self.root.minsize(900, 600)
        self._center_window()
        self.root.configure(fg_color="#0D0F14")

        _make_icon(self.root)

        self._current_frame = None
        self._user = None
        self._token = None

        # Check for saved session
        saved = check_saved_session()
        if saved:
            self._user = saved
            self._token = saved.get("token", "")
            self._show_app()
        else:
            self._show_login()

        self.root.mainloop()

    def _center_window(self):
        w, h = 1280, 800
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _clear_frame(self):
        if self._current_frame:
            self._current_frame.destroy()
            self._current_frame = None

    def _show_login(self):
        self._clear_frame()
        from ui.login_screen import LoginScreen
        frame = LoginScreen(self.root, on_login_success=self._on_login_success)
        frame.pack(fill="both", expand=True)
        self._current_frame = frame

    def _show_app(self):
        self._clear_frame()
        from ui.app_window import AppWindow
        frame = AppWindow(
            self.root,
            user=self._user,
            token=self._token,
            on_logout=self._on_logout
        )
        frame.pack(fill="both", expand=True)
        self._current_frame = frame

    def _on_login_success(self, user: dict, token: str):
        self._user = user
        self._token = token
        self._show_app()

    def _on_logout(self):
        self._user = None
        self._token = None
        self._show_login()


# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    CareerPathApp()
