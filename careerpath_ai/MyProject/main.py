import os
import sys
import platform
import tkinter as tk
from tkinter import messagebox

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    print("Pillow is not installed. Please install it from requirements.txt")
    sys.exit()

APP_NAME = "CareerPath Setup"
ICON_PNG = "app_icon.png"
ICON_ICO = "app_icon.ico"

def create_icon():
    """Generates a modern, colorful Windows 10X style custom app icon if missing."""
    if os.path.exists(ICON_PNG) and os.path.exists(ICON_ICO):
        return

    SIZE = 256
    MARGIN = 24
    RADIUS = 48

    # 1. Base transparent image
    base = Image.new('RGBA', (SIZE, SIZE), (255, 255, 255, 0))

    # 2. Draw strong drop shadow (like Windows 10X deep shadow)
    shadow = Image.new('RGBA', (SIZE, SIZE), (255, 255, 255, 0))
    s_draw = ImageDraw.Draw(shadow)
    shadow_box = [MARGIN, MARGIN + 12, SIZE - MARGIN, SIZE - MARGIN + 12]
    s_draw.rounded_rectangle(shadow_box, radius=RADIUS, fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    base.alpha_composite(shadow)

    # 3. Create vibrant Gradient Background (Blue to Cyan matching a career path theme)
    gradient = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    color_top = (108, 99, 255)   # #6C63FF (modern purple/blue)
    color_bottom = (0, 212, 170) # #00D4AA (vibrant teal)

    for y in range(SIZE):
        ratio = y / SIZE
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        draw_y = ImageDraw.Draw(gradient)
        draw_y.line([(0, y), (SIZE, y)], fill=(r, g, b, 255))

    # Mask gradient to rounded rect base
    mask = Image.new('L', (SIZE, SIZE), 0)
    m_draw = ImageDraw.Draw(mask)
    box = [MARGIN, MARGIN, SIZE - MARGIN, SIZE - MARGIN]
    m_draw.rounded_rectangle(box, radius=RADIUS, fill=255)

    app_bg = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    app_bg.paste(gradient, (0, 0), mask=mask)
    base.alpha_composite(app_bg)

    # 4. Draw Modern Overlapping Symbol 
    symbol = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    sym_draw = ImageDraw.Draw(symbol)
    
    # Career path stylized shape (overlapping triangles/paths)
    sym_draw.polygon([(100, 180), (100, 70), (160, 125)], fill=(255, 255, 255, 210))
    sym_draw.polygon([(100, 180), (160, 180), (200, 125), (140, 125)], fill=(255, 255, 255, 140))
    sym_shadow = symbol.filter(ImageFilter.GaussianBlur(3))

    base.alpha_composite(sym_shadow)
    base.alpha_composite(symbol)

    # Save PNG and ICO
    base.save(ICON_PNG, "PNG")
    base.save(ICON_ICO, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])


def get_desktop_path():
    if platform.system() == "Windows":
        return os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop")
    else:
        return os.path.join(os.path.expanduser("~"), "Desktop")

def create_windows_shortcut(target, desktop_dir, app_name):
    try:
        import win32com.client
    except ImportError:
        print("pywin32 is not installed!")
        return False
        
    shortcut_path = os.path.join(desktop_dir, f"{app_name}.lnk")
    if os.path.exists(shortcut_path):
        return False
        
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = os.path.dirname(target)
        
        icon_path = os.path.join(os.path.dirname(target), ICON_ICO)
        if os.path.exists(icon_path):
            shortcut.IconLocation = os.path.abspath(icon_path)
            
        shortcut.WindowStyle = 1
        shortcut.save()
        return True
    except Exception as e:
        print("Error creating Windows shortcut:", e)
        return False

def create_linux_shortcut(target, desktop_dir, app_name):
    shortcut_path = os.path.join(desktop_dir, f"{app_name}.desktop")
    if os.path.exists(shortcut_path):
        return False
        
    icon_path = os.path.join(os.path.dirname(target), ICON_PNG)
    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={app_name}
Exec="{sys.executable}" "{target}"
Icon={os.path.abspath(icon_path) if os.path.exists(icon_path) else 'utilities-terminal'}
Terminal=false
"""
    with open(shortcut_path, "w") as f:
        f.write(content)
    os.chmod(shortcut_path, 0o755)
    return True

def create_macos_shortcut(target, desktop_dir, app_name):
    shortcut_path = os.path.join(desktop_dir, f"{app_name}.command")
    if os.path.exists(shortcut_path):
        return False
    with open(shortcut_path, "w") as f:
        f.write(f'#!/bin/bash\n"{sys.executable}" "{target}"\n')
    os.chmod(shortcut_path, 0o755)
    return True

def auto_create_shortcut():
    desktop = get_desktop_path()
    target = os.path.abspath(__file__)
    
    system = platform.system()
    if system == "Windows":
        return create_windows_shortcut(target, desktop, APP_NAME)
    elif system == "Linux":
        return create_linux_shortcut(target, desktop, APP_NAME)
    elif system == "Darwin":
        return create_macos_shortcut(target, desktop, APP_NAME)
    return None

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("450x250")
        self.resizable(False, False)
        
        # Configure UI Theme
        self.configure(bg="#F2F3F5")
        
        # Ensure icon is ready
        create_icon()
        
        # Apply Icon
        icon_path_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), ICON_PNG)
        icon_path_ico = os.path.join(os.path.dirname(os.path.abspath(__file__)), ICON_ICO)
        
        try:
            if platform.system() == "Windows" and os.path.exists(icon_path_ico):
                self.iconbitmap(icon_path_ico)
            elif os.path.exists(icon_path_png):
                icon_img = tk.PhotoImage(file=icon_path_png)
                self.iconphoto(True, icon_img)
        except Exception as e:
            print("Failed to set window icon. (Pillow may need restart / cache)", e)

        # Build Main Frame
        main_frame = tk.Frame(self, bg="#FFFFFF", padx=20, pady=20, relief=tk.RAISED, bd=1)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        tk.Label(main_frame, text=APP_NAME, font=("Helvetica", 18, "bold"), bg="#FFFFFF", fg="#333333").pack(pady=(0, 10))
        tk.Label(main_frame, text="Desktop Shortcut Manager & Custom Icon Generator", font=("Helvetica", 10), bg="#FFFFFF", fg="#666666").pack(pady=(0, 20))
        
        self.btn = tk.Button(main_frame, text="📌 Re-create Desktop Shortcut", 
                             font=("Helvetica", 11, "bold"), bg="#5865F2", fg="white",
                             activebackground="#4752C4", activeforeground="white",
                             padx=15, pady=8, borderwidth=0, cursor="hand2",
                             command=self.manual_shortcut)
        self.btn.pack()
        
        # Auto-create shortcut schedule logic
        self.after(500, self.do_autorun)
        
    def do_autorun(self):
        created = auto_create_shortcut()
        if created is True:
            messagebox.showinfo("Success", f"Desktop shortcut created!")

    def manual_shortcut(self):
        target_path = os.path.join(get_desktop_path(), f"{APP_NAME}.lnk") if platform.system() == "Windows" else os.path.join(get_desktop_path(), f"{APP_NAME}.desktop")
        
        if os.path.exists(target_path):
            try:
                os.remove(target_path)  # Delete old to recreate immediately
            except OSError:
                pass
            
        created = auto_create_shortcut()
        if created is True:
            messagebox.showinfo("Success", "Desktop shortcut newly created!")
        else:
            messagebox.showerror("Error", "Could not create the shortcut.")

if __name__ == "__main__":
    generate_icon_if_missing = create_icon
    generate_icon_if_missing()
    
    app = App()
    app.mainloop()
