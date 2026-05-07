"""
ui/settings.py - Animated Settings Panel with Fixed Theme & Font Logic
"""
import customtkinter as ctk
import tkinter as tk

COLORS = {
    "bg": "#0D0F14", "card": "#1A1D27", "accent": "#6C63FF",
    "accent_hover": "#7C73FF", "teal": "#00D4AA", "text": "#F0F0F5",
    "muted": "#7A7F9A", "error": "#FF6B6B", "sidebar": "#12151C", "border": "#2A2D3E",
}

class SettingsPanel(ctk.CTkFrame):
    def __init__(self, master, user: dict, on_logout):
        super().__init__(master, fg_color=COLORS["bg"])
        self.user = user
        self.on_logout = on_logout
        self._anim_queue = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build()
        
        # Trigger entrance animation
        self.after(100, self._run_entrance_animation)

    def _build(self):
        # Title
        self.title_lbl = ctk.CTkLabel(self, text="⚙️  Settings",
                                     font=ctk.CTkFont(size=26, weight="bold"),
                                     text_color=COLORS["text"])
        self.title_lbl.grid(row=0, column=0, sticky="w", padx=32, pady=(28, 12))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg"],
                                             scrollbar_button_color=COLORS["border"])
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 16))
        self.scroll.grid_columnconfigure(0, weight=1)
        r = 0



        # --- Account ---
        r = self._hdr(self.scroll, r, "👤  Account")
        acc = self._card(self.scroll, r); r += 1
        acc.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(acc, text=self.user.get("username", "User"),
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=COLORS["text"]).grid(row=0, column=0, padx=16, pady=(14, 2), sticky="w")
        
        ctk.CTkLabel(acc, text=self.user.get("email", "user@example.com"),
                     font=ctk.CTkFont(size=11), text_color=COLORS["muted"]).grid(
                     row=1, column=0, padx=16, pady=(0, 14), sticky="w")
        
        self.logout_btn = ctk.CTkButton(acc, text="🚪  Logout", width=100, height=36,
                                       fg_color="transparent", border_width=1, border_color=COLORS["error"],
                                       text_color=COLORS["error"], hover_color="#331A1D",
                                       corner_radius=8, font=ctk.CTkFont(size=12, weight="bold"),
                                       command=self.on_logout)
        self.logout_btn.grid(row=0, column=2, rowspan=2, padx=16, pady=14)
        
        acc.grid_remove()
        self._anim_queue.append(acc)

    # --- Logic Functions ---

    def _change_theme(self, new_theme):
        """Fixed theme switching logic."""
        ctk.set_appearance_mode(new_theme)

    def _update_font_scale(self, value):
        """Simulates font scaling and updates label."""
        self._font_lbl.configure(text=f"{value:.1f}×")
        # In a real app, you would update a global scaling variable here.

    def _run_entrance_animation(self):
        """Staggered reveal animation for settings cards."""
        if self._anim_queue:
            widget = self._anim_queue.pop(0)
            widget.grid()
            # Fade-in flash effect
            orig_bg = widget.cget("fg_color")
            widget.configure(fg_color="#25293D")
            self.after(100, lambda: widget.configure(fg_color=orig_bg))
            self.after(70, self._run_entrance_animation)

    # --- UI Helpers ---

    def _hdr(self, parent, row: int, text: str) -> int:
        lbl = ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=13, weight="bold"),
                           text_color=COLORS["muted"])
        lbl.grid(row=row, column=0, sticky="w", padx=8, pady=(18, 4))
        return row + 1

    def _card(self, parent, row: int) -> ctk.CTkFrame:
        f = ctk.CTkFrame(parent, fg_color=COLORS["card"], corner_radius=12,
                         border_width=1, border_color=COLORS["border"])
        f.grid(row=row, column=0, sticky="ew", padx=8, pady=4)
        f.grid_columnconfigure(1, weight=1)
        
        # Hover effect
        f.bind("<Enter>", lambda e: f.configure(border_color=COLORS["accent"]))
        f.bind("<Leave>", lambda e: f.configure(border_color=COLORS["border"]))
        return f