"""
ui/dashboard.py - High-End Animated Dashboard with Floating Entrance Transitions
"""
import customtkinter as ctk
import tkinter as tk
import random

COLORS = {
    "bg": "#0D0F14", "card": "#1A1D27", "accent": "#6C63FF",
    "accent_hover": "#7C73FF", "teal": "#00D4AA", "text": "#F0F0F5",
    "muted": "#7A7F9A", "error": "#FF6B6B", "sidebar": "#12151C", "border": "#2A2D3E",
    "card_glow": "#25293D"
}

MOTIVATION = [
    "Fuel your ambition. ⚡",
    "Master your craft. 💎",
    "Architect your future. 🏗️",
    "Code your destiny. 💻",
    "Stay ahead of the curve. 📈"
]

QUICK_TRACKS = [
    ("🌐", "Full Stack Dev",  "fullstack",     "intermediate", "Build complete web applications"),
    ("🤖", "AI / ML",         "aiml",          "advanced",     "Highest salary potential in tech"),
    ("🔐", "Cybersecurity",   "cybersecurity", "advanced",     "Fastest growing field globally"),
    ("📊", "Data Science",    "datascience",   "intermediate", "Data-driven analytical career"),
    ("☁️", "DevOps",          "devops",        "advanced",     "Cloud & infrastructure automation"),
    ("📱", "Android Dev",     "android",       "intermediate", "Build native mobile applications"),
]

class DashboardPanel(ctk.CTkFrame):
    def __init__(self, master, user: dict, on_navigate=None):
        super().__init__(master, fg_color=COLORS["bg"])
        self.user = user
        self.on_navigate = on_navigate
        self._anim_widgets = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._build()
        # Start the "Staggered Rise" animation sequence
        self.after(100, self._animate_entrance)

    def _build(self):
        # --- Header (Motivational Replacement) ---
        self.header_container = ctk.CTkFrame(self, fg_color="transparent")
        self.header_container.grid(row=0, column=0, sticky="ew", padx=45, pady=(40, 20))
        
        # Professional Heading
        ctk.CTkLabel(self.header_container, text=f"{self.user.get('username', 'Explorer')}'s Hub",
                     font=ctk.CTkFont(size=36, weight="bold"), text_color=COLORS["text"]).pack(anchor="w")
        
        # Dynamic Motivation Subtitle
        ctk.CTkLabel(self.header_container, text=random.choice(MOTIVATION),
                     font=ctk.CTkFont(size=16), text_color=COLORS["teal"]).pack(anchor="w", pady=(2, 0))
        
        self.header_container.grid_remove()
        self._anim_widgets.append(self.header_container)

        # --- Body ---
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", 
                                             scrollbar_button_color=COLORS["border"],
                                             scrollbar_button_hover_color=COLORS["accent"])
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=35)
        self.scroll.grid_columnconfigure((0, 1, 2), weight=1)

        # Stats section
        self.stats_row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.stats_row.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 25))
        self.stats_row.grid_columnconfigure((0, 1, 2), weight=1)

        stats_items = [
            ("🚀", "12", "Active Paths"), 
            ("🔥", "85%", "Completion"), 
            ("⭐", "Top 5%", "Global Rank")
        ]

        for i, (icon, val, label) in enumerate(stats_items):
            card = self._create_stat_card(self.stats_row, icon, val, label)
            card.grid(row=0, column=i, padx=10, sticky="ew")
            card.grid_remove()
            self._anim_queue_item(card)

        # Quick Start Grid Heading
        self.recom_lbl = ctk.CTkLabel(self.scroll, text="Strategic Roadmaps", 
                                     font=ctk.CTkFont(size=20, weight="bold"))
        self.recom_lbl.grid(row=1, column=0, columnspan=3, sticky="w", padx=12, pady=(20, 15))
        self.recom_lbl.grid_remove()
        self._anim_queue_item(self.recom_lbl)

        for j, track in enumerate(QUICK_TRACKS):
            col, row = j % 3, 2 + j // 3
            card = self._create_track_card(self.scroll, *track)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card.grid_remove()
            self._anim_queue_item(card)

    def _anim_queue_item(self, widget):
        """Adds widget to list and keeps track of its intended Y position offset."""
        self._anim_widgets.append(widget)

    def _create_stat_card(self, parent, icon, val, label):
        card = ctk.CTkFrame(parent, fg_color=COLORS["card"], corner_radius=16, border_width=1, border_color=COLORS["border"])
        ctk.CTkLabel(card, text=icon, font=("Arial", 28)).pack(pady=(15, 0))
        ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=24, weight="bold"), text_color=COLORS["accent"]).pack()
        ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=12), text_color=COLORS["muted"]).pack(pady=(0, 15))
        return card

    def _create_track_card(self, parent, icon, name, key, diff, desc):
        card = ctk.CTkFrame(parent, fg_color=COLORS["card"], corner_radius=20, border_width=1, border_color=COLORS["border"])
        card.grid_columnconfigure(0, weight=1)

        # Visual elements
        ctk.CTkLabel(card, text=icon, font=("Arial", 35)).grid(row=0, column=0, pady=(25, 10))
        ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=16, weight="bold")).grid(row=1, column=0, padx=20)
        
        # Skill Badge
        badge = ctk.CTkLabel(card, text=diff.upper(), font=ctk.CTkFont(size=9, weight="bold"), 
                             fg_color=COLORS["sidebar"], corner_radius=6, width=80)
        badge.grid(row=2, column=0, pady=8)

        # Explore Button
        btn = ctk.CTkButton(card, text="Start Roadmap", height=40, corner_radius=12,
                            fg_color="transparent", border_width=1, border_color=COLORS["border"],
                            hover_color=COLORS["accent"], command=lambda k=key: self._navigate(k))
        btn.grid(row=3, column=0, padx=25, pady=(15, 25), sticky="ew")

        # --- Enhanced Hover Effects ---
        def on_enter(e):
            card.configure(border_color=COLORS["accent"], fg_color=COLORS["card_glow"])
            btn.configure(border_width=0, fg_color=COLORS["accent"])

        def on_leave(e):
            card.configure(border_color=COLORS["border"], fg_color=COLORS["card"])
            btn.configure(border_width=1, fg_color="transparent")

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        return card

    def _animate_entrance(self, index=0):
        """Creates a cascading floating effect where items rise and glow into place."""
        if index < len(self._anim_widgets):
            w = self._anim_widgets[index]
            w.grid()
            
            # Physics rise simulation (modifying padding for a smooth 'float up' look)
            orig_pady = w.grid_info().get('pady', (0, 0))
            if isinstance(orig_pady, int): orig_pady = (orig_pady, orig_pady)
            
            # Start slightly lower and rise
            w.grid_configure(pady=(orig_pady[0] + 10, orig_pady[1]))
            
            def settle(widget=w, p=orig_pady):
                widget.grid_configure(pady=p)
                # Border glow flash on arrival
                if hasattr(widget, "configure") and "border_color" in widget.keys():
                    widget.configure(border_color=COLORS["teal"])
                    self.after(150, lambda: widget.configure(border_color=COLORS["border"]))

            self.after(50, settle)
            
            # Cascading timing logic
            self.after(80, lambda: self._animate_entrance(index + 1))

    def _navigate(self, key):
        if self.on_navigate:
            self.on_navigate(key)