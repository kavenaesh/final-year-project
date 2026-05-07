"""
shortcut_maker.py - CareerPath AI Desktop Shortcut Creator
Place this file in the ROOT of your CareerPath AI project folder.
Run it ONCE to create the desktop shortcut pointing to your real app.
"""
import os
import sys
import platform
import tkinter as tk
from tkinter import messagebox

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    pass

# ── Find the REAL main.py (CareerPath AI app) ────────────────────────────────
# This file (shortcut_maker.py) sits in the project root.
# The real app entry point is main.py in the SAME folder.
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
REAL_MAIN = os.path.join(THIS_DIR, "main.py")   # ← CareerPath AI main.py
APP_NAME  = "CareerPath AI"
ICON_ICO  = os.path.join(THIS_DIR, "app_icon.ico")
ICON_PNG  = os.path.join(THIS_DIR, "app_icon.png")


def create_icon():
    """Generates a modern, colorful Windows 10X style custom app icon if missing."""
    if os.path.exists(ICON_PNG) and os.path.exists(ICON_ICO):
        return

    try:
        from PIL import Image, ImageDraw, ImageFilter
    except ImportError:
        print("Pillow not installed. Cannot auto-generate icon.")
        return

    SIZE = 256
    MARGIN = 24
    RADIUS = 48

    base = Image.new('RGBA', (SIZE, SIZE), (255, 255, 255, 0))

    shadow = Image.new('RGBA', (SIZE, SIZE), (255, 255, 255, 0))
    s_draw = ImageDraw.Draw(shadow)
    shadow_box = [MARGIN, MARGIN + 12, SIZE - MARGIN, SIZE - MARGIN + 12]
    s_draw.rounded_rectangle(shadow_box, radius=RADIUS, fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    base.alpha_composite(shadow)

    gradient = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    color_top = (108, 99, 255)
    color_bottom = (0, 212, 170)

    for y in range(SIZE):
        ratio = y / SIZE
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        draw_y = ImageDraw.Draw(gradient)
        draw_y.line([(0, y), (SIZE, y)], fill=(r, g, b, 255))

    mask = Image.new('L', (SIZE, SIZE), 0)
    m_draw = ImageDraw.Draw(mask)
    box = [MARGIN, MARGIN, SIZE - MARGIN, SIZE - MARGIN]
    m_draw.rounded_rectangle(box, radius=RADIUS, fill=255)

    app_bg = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    app_bg.paste(gradient, (0, 0), mask=mask)
    base.alpha_composite(app_bg)

    symbol = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    sym_draw = ImageDraw.Draw(symbol)
    
    sym_draw.polygon([(100, 180), (100, 70), (160, 125)], fill=(255, 255, 255, 210))
    sym_draw.polygon([(100, 180), (160, 180), (200, 125), (140, 125)], fill=(255, 255, 255, 140))
    sym_shadow = symbol.filter(ImageFilter.GaussianBlur(3))

    base.alpha_composite(sym_shadow)
    base.alpha_composite(symbol)

    base.save(ICON_PNG, "PNG")
    base.save(ICON_ICO, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])

# ── Desktop path ─────────────────────────────────────────────────────────────
def get_desktop_path():
    if platform.system() == "Windows":
        return os.path.join(
            os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop"
        )
    return os.path.join(os.path.expanduser("~"), "Desktop")


# ── Shortcut creators ────────────────────────────────────────────────────────
def create_windows_shortcut():
    desktop = get_desktop_path()
    shortcut_path = os.path.join(desktop, f"{APP_NAME}.lnk")

    # Remove old shortcut so we can recreate fresh
    if os.path.exists(shortcut_path):
        try:
            os.remove(shortcut_path)
        except OSError:
            pass

    try:
        import win32com.client
        shell     = win32com.client.Dispatch("WScript.Shell")
        shortcut  = shell.CreateShortCut(shortcut_path)

        shortcut.Targetpath      = sys.executable          # python.exe
        shortcut.Arguments       = f'"{REAL_MAIN}"'        # → real main.py
        shortcut.WorkingDirectory = THIS_DIR               # project folder
        shortcut.Description     = "CareerPath AI – Your Intelligent Career Navigator"
        shortcut.WindowStyle     = 1                       # normal window

        if os.path.exists(ICON_ICO):
            shortcut.IconLocation = ICON_ICO

        shortcut.save()
        return True, shortcut_path

    except ImportError:
        # Fallback: .bat file (no pywin32 needed)
        bat_path = os.path.join(desktop, f"{APP_NAME}.bat")
        with open(bat_path, "w") as f:
            f.write(f'@echo off\n"{sys.executable}" "{REAL_MAIN}"\n')
        return True, bat_path

    except Exception as e:
        return False, str(e)


def create_linux_shortcut():
    desktop = get_desktop_path()
    shortcut_path = os.path.join(desktop, f"{APP_NAME}.desktop")

    icon = ICON_PNG if os.path.exists(ICON_PNG) else "utilities-terminal"
    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={APP_NAME}
Comment=CareerPath AI – Your Intelligent Career Navigator
Exec="{sys.executable}" "{REAL_MAIN}"
Icon={icon}
Terminal=false
StartupNotify=true
"""
    with open(shortcut_path, "w") as f:
        f.write(content)
    os.chmod(shortcut_path, 0o755)
    return True, shortcut_path


def create_macos_shortcut():
    desktop = get_desktop_path()
    shortcut_path = os.path.join(desktop, f"{APP_NAME}.command")

    with open(shortcut_path, "w") as f:
        f.write(f'#!/bin/bash\ncd "{THIS_DIR}"\n"{sys.executable}" "{REAL_MAIN}"\n')
    os.chmod(shortcut_path, 0o755)
    return True, shortcut_path


def make_shortcut():
    """Detect OS and create the correct desktop shortcut."""
    if not os.path.exists(REAL_MAIN):
        return False, f"Cannot find main.py at:\n{REAL_MAIN}\n\nMake sure shortcut_maker.py is in the project root folder."

    system = platform.system()
    if system == "Windows":
        return create_windows_shortcut()
    elif system == "Linux":
        return create_linux_shortcut()
    elif system == "Darwin":
        return create_macos_shortcut()
    else:
        return False, f"Unsupported OS: {system}"


# ── GUI ───────────────────────────────────────────────────────────────────────
class ShortcutMakerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CareerPath AI – Shortcut Installer")
        self.geometry("480x300")
        self.resizable(False, False)
        self.configure(bg="#0D0F14")

        # Window icon
        try:
            if platform.system() == "Windows" and os.path.exists(ICON_ICO):
                self.iconbitmap(ICON_ICO)
            elif os.path.exists(ICON_PNG):
                img = tk.PhotoImage(file=ICON_PNG)
                self.iconphoto(True, img)
                self._icon_ref = img
        except Exception:
            pass

        # ── UI ────────────────────────────────────────────────────────────
        card = tk.Frame(self, bg="#1A1D26", padx=30, pady=30)
        card.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(
            card, text="CareerPath AI", bg="#1A1D26", fg="#FFFFFF",
            font=("Helvetica", 20, "bold")
        ).pack()

        tk.Label(
            card, text="Desktop Shortcut Installer", bg="#1A1D26", fg="#888888",
            font=("Helvetica", 10)
        ).pack(pady=(4, 0))

        # Status label
        self.status_var = tk.StringVar(value="")
        tk.Label(
            card, textvariable=self.status_var, bg="#1A1D26", fg="#00D4AA",
            font=("Helvetica", 9), wraplength=400, justify="center"
        ).pack(pady=(16, 0))

        # Target path info
        target_text = f"→ {REAL_MAIN}"
        tk.Label(
            card, text=target_text, bg="#1A1D26", fg="#555577",
            font=("Courier", 8), wraplength=420, justify="center"
        ).pack(pady=(6, 16))

        # Button
        btn = tk.Button(
            card, text="🖥️  Create Desktop Shortcut",
            font=("Helvetica", 11, "bold"),
            bg="#6C63FF", fg="white",
            activebackground="#5A52E0", activeforeground="white",
            padx=20, pady=10, borderwidth=0, cursor="hand2",
            relief=tk.FLAT,
            command=self.do_create
        )
        btn.pack()

        # Auto-run on first launch
        self.after(600, self.do_create)

    def do_create(self):
        success, result = make_shortcut()
        if success:
            self.status_var.set(f"✅ Shortcut created!\n{result}")
            messagebox.showinfo(
                "Success ✅",
                f"Desktop shortcut created!\n\n"
                f"Double-click  '{APP_NAME}'  on your Desktop\n"
                f"to launch CareerPath AI."
            )
        else:
            self.status_var.set(f"❌ Failed: {result}")
            messagebox.showerror("Error ❌", result)


# ── Entry ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    create_icon()
    app = ShortcutMakerApp()
    app.mainloop()