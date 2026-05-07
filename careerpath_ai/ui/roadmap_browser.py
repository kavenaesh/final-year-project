"""
ui/roadmap_browser.py - Career track grid with staggered entrance animations
"""
import customtkinter as ctk
import tkinter as tk

COLORS = {
    "bg": "#0D0F14", "card": "#1A1D27", "accent": "#6C63FF",
    "accent_hover": "#7C73FF", "teal": "#00D4AA", "text": "#F0F0F5",
    "muted": "#7A7F9A", "error": "#FF6B6B", "sidebar": "#12151C", "border": "#2A2D3E",
    "glow": "#1E2235"
}

DIFF_COLORS = {
    "Beginner": "#00D4AA", "Intermediate": "#6C63FF", "Advanced": "#FF6B6B"
}

class RoadmapBrowser(ctk.CTkFrame):
    def __init__(self, master, user: dict, on_view_roadmap):
        super().__init__(master, fg_color=COLORS["bg"])
        self.user = user
        self.on_view_roadmap = on_view_roadmap
        self._saved_keys = set()
        self._anim_queue = [] # Queue for staggered animations
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._load_saved()
        self._build()
        
        # Initial ripple entrance
        self.after(100, self._run_entrance_animation)

    def _load_saved(self):
        try:
            from database.db import get_saved_roadmaps
            saved = get_saved_roadmaps(self.user["id"])
            self._saved_keys = {r["roadmap_key"] for r in saved}
        except Exception: pass

    def _build(self):
        # Header Section
        self.hdr = ctk.CTkFrame(self, fg_color="transparent")
        self.hdr.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 12))
        
        ctk.CTkLabel(self.hdr, text="🗺️  Career Roadmaps",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     text_color=COLORS["text"]).pack(side="left")

        # Search bar with focus glow
        self.search_frame = ctk.CTkFrame(self.hdr, fg_color=COLORS["card"], 
                                         corner_radius=10, border_width=1, border_color=COLORS["border"])
        self.search_frame.pack(side="right")
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        
        self.search_entry = ctk.CTkEntry(self.search_frame, textvariable=self.search_var, 
                                         placeholder_text="Search tracks...",
                                         width=220, height=38, fg_color="transparent", border_width=0)
        self.search_entry.pack(padx=5)
        
        self.search_entry.bind("<FocusIn>", lambda e: self.search_frame.configure(border_color=COLORS["accent"]))
        self.search_entry.bind("<FocusOut>", lambda e: self.search_frame.configure(border_color=COLORS["border"]))

        # Scrollable grid
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg"],
                                             scrollbar_button_color=COLORS["border"],
                                             scrollbar_button_hover_color=COLORS["accent"])
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 16))
        self.scroll.grid_columnconfigure((0, 1, 2), weight=1)

        self._render_cards()

    def _run_entrance_animation(self):
        """Sequential ripple reveal for cards."""
        if self._anim_queue:
            widget = self._anim_queue.pop(0)
            widget.grid()
            # Soft pop-in pulse
            if hasattr(widget, "configure"):
                widget.configure(border_color=COLORS["accent"])
                self.after(120, lambda: widget.configure(border_color=COLORS["border"]))
            self.after(60, self._run_entrance_animation)

    def _render_cards(self, filter_text: str = ""):
        # Stop current animation queue if any
        self._anim_queue.clear()
        
        for widget in self.scroll.winfo_children():
            widget.destroy()

        from core.roadmap_data2 import CAREER_TRACKS, ROADMAPS

        categories = {}
        for track in CAREER_TRACKS:
            key = track["key"]
            data = ROADMAPS.get(key, {})
            title = data.get("title", key)
            if filter_text and filter_text.lower() not in title.lower():
                continue
            cat = track["category"]
            categories.setdefault(cat, []).append((key, data))

        row_idx = 0
        for cat_name, tracks in categories.items():
            # Category label
            cat_lbl = ctk.CTkLabel(self.scroll, text=f"  {cat_name}",
                                   font=ctk.CTkFont(size=14, weight="bold"),
                                   text_color=COLORS["muted"])
            cat_lbl.grid(row=row_idx, column=0, columnspan=3, sticky="w", padx=8, pady=(16, 4))
            row_idx += 1

            for i, (key, data) in enumerate(tracks):
                card = self._make_card(key, data)
                card.grid(row=row_idx + i // 3, column=i % 3, padx=8, pady=6, sticky="nsew")
                card.grid_remove() # Hide for animation
                self._anim_queue.append(card)
            
            row_idx += (len(tracks) + 2) // 3
        
        self._run_entrance_animation()

    def _make_card(self, key: str, data: dict) -> ctk.CTkFrame:
        card = ctk.CTkFrame(self.scroll, fg_color=COLORS["card"], corner_radius=16,
                             border_width=1, border_color=COLORS["border"])
        card.grid_columnconfigure(0, weight=1)

        # Top Section
        top = ctk.CTkFrame(card, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(top, text=data.get("icon", "🔹"), font=("Arial", 24)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(top, text=data.get("title", key), font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=COLORS["text"], wraplength=160, justify="left").pack(side="left")

        # Bookmark toggle with color shift
        is_saved = key in self._saved_keys
        save_btn = ctk.CTkButton(top, text="💾" if is_saved else "🔖", width=32, height=32,
                                fg_color=COLORS["teal"] if is_saved else COLORS["sidebar"],
                                hover_color=COLORS["accent"], corner_radius=8)
        save_btn.configure(command=lambda k=key, b=save_btn: self._toggle_save(k, b))
        save_btn.pack(side="right")

        # Meta info
        ctk.CTkLabel(card, text=data.get("description", ""), font=ctk.CTkFont(size=11),
                     text_color=COLORS["muted"], wraplength=220, justify="left").grid(
                     row=1, column=0, sticky="w", padx=18, pady=(0, 10))

        # Difficulty & Time
        meta = ctk.CTkFrame(card, fg_color="transparent")
        meta.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 15))
        diff = data.get("difficulty", "Intermediate")
        ctk.CTkLabel(meta, text=diff, font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=DIFF_COLORS.get(diff), fg_color=COLORS["sidebar"], corner_radius=5).pack(side="left")
        ctk.CTkLabel(meta, text=f"  ⏱ {data.get('duration', '')}", 
                     font=ctk.CTkFont(size=10), text_color=COLORS["muted"]).pack(side="left")

        # Action Button
        view_btn = ctk.CTkButton(card, text="Explore Roadmap", height=38, corner_radius=10,
                                fg_color=COLORS["sidebar"], border_width=1, border_color=COLORS["border"],
                                hover_color=COLORS["accent"], command=lambda k=key: self.on_view_roadmap(k))
        view_btn.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 15))

        # --- Professional Interactions ---
        def on_enter(e):
            card.configure(border_color=COLORS["accent"], fg_color=COLORS["glow"])
            view_btn.configure(fg_color=COLORS["accent"], border_width=0)
            
        def on_leave(e):
            card.configure(border_color=COLORS["border"], fg_color=COLORS["card"])
            view_btn.configure(fg_color=COLORS["sidebar"], border_width=1)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        return card

    def _toggle_save(self, key: str, btn: ctk.CTkButton):
        from database.db import save_roadmap, remove_saved_roadmap
        if key in self._saved_keys:
            remove_saved_roadmap(self.user["id"], key)
            self._saved_keys.discard(key)
            btn.configure(text="🔖", fg_color=COLORS["sidebar"])
        else:
            save_roadmap(self.user["id"], key)
            self._saved_keys.add(key)
            btn.configure(text="💾", fg_color=COLORS["teal"])

    def _on_search(self, *_):
        self._render_cards(self.search_var.get())