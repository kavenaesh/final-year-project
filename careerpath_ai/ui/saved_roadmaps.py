"""
ui/saved_roadmaps.py - User's saved roadmaps with staggered animations and fixed removal
"""
import customtkinter as ctk
import tkinter as tk
import json

COLORS = {
    "bg": "#0D0F14", "card": "#1A1D27", "accent": "#6C63FF",
    "accent_hover": "#7C73FF", "teal": "#00D4AA", "text": "#F0F0F5",
    "muted": "#7A7F9A", "error": "#FF6B6B", "sidebar": "#12151C", "border": "#2A2D3E",
    "card_glow": "#1E2235"
}

class SavedRoadmapsPanel(ctk.CTkFrame):
    def __init__(self, master, user: dict, on_continue):
        super().__init__(master, fg_color=COLORS["bg"])
        self.user = user
        self.on_continue = on_continue
        self._anim_queue = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build()

    def _build(self):
        # Header Section
        self.hdr = ctk.CTkFrame(self, fg_color="transparent")
        self.hdr.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 8))
        self.hdr.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.hdr, text="💾  My Saved Roadmaps",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     text_color=COLORS["text"]).grid(row=0, column=0, sticky="w")

        # Sort Dropdown
        self.sort_var = tk.StringVar(value="Recently Saved")
        self.sort_menu = ctk.CTkOptionMenu(self.hdr, values=["Recently Saved", "Alphabetical"],
                                          variable=self.sort_var, width=160, height=34,
                                          fg_color=COLORS["card"], button_color=COLORS["accent"],
                                          command=lambda v: self._render(v))
        self.sort_menu.grid(row=0, column=2, sticky="e")

        # Main Scrollable Area
        self.scroll = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg"],
                                             scrollbar_button_color=COLORS["border"],
                                             scrollbar_button_hover_color=COLORS["accent"])
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 16))
        self.scroll.grid_columnconfigure(0, weight=1)
        
        self._render("Recently Saved")

    def _run_entrance_animation(self):
        """Sequentially reveals each roadmap card with a 'fade-up' effect."""
        if self._anim_queue:
            card = self._anim_queue.pop(0)
            card.grid() # Make visible
            
            # Smoothly fill the progress bar to show life
            if hasattr(card, 'prog_bar'):
                target_val = card.target_pct / 100
                self._animate_progress(card.prog_bar, 0, target_val)
                
            self.after(70, self._run_entrance_animation)

    def _animate_progress(self, pbar, current, target):
        """Smoothly fills the progress bar from 0 to target."""
        if current < target:
            next_val = min(current + 0.05, target)
            pbar.set(next_val)
            self.after(20, lambda: self._animate_progress(pbar, next_val, target))

    def _render(self, sort_val: str = "Recently Saved"):
        # Clear current view
        for w in self.scroll.winfo_children():
            w.destroy()
        self._anim_queue.clear()

        sort_key = "recent" if sort_val == "Recently Saved" else "alpha"
        try:
            from database.db import get_saved_roadmaps
            rows = get_saved_roadmaps(self.user["id"], sort_by=sort_key)
        except Exception:
            rows = []

        if not rows:
            ctk.CTkLabel(self.scroll, text="No saved roadmaps yet. Go explore! ✨",
                         font=ctk.CTkFont(size=14), text_color=COLORS["muted"]).grid(row=0, column=0, pady=80)
            return

        from core.roadmap_data2 import ROADMAPS
        for i, row in enumerate(rows):
            key = row["roadmap_key"]
            rm = ROADMAPS.get(key, {})
            try:
                prog = json.loads(row.get("progress_json", "{}")) if row.get("progress_json") else {}
            except:
                prog = {}

            # Progress Calculation
            topics = [t for ph in rm.get("phases", []) for t in ph.get("topics", [])]
            total = len(topics)
            done = sum(1 for t in topics if prog.get(t["name"], False))
            pct = (done / total * 100) if total else 0

            card = self._make_card(row, rm, key, done, total, pct)
            card.grid(row=i, column=0, sticky="ew", padx=8, pady=8)
            card.grid_remove() # Hide initially for animation
            self._anim_queue.append(card)

        # Start animation sequence
        self.after(100, self._run_entrance_animation)

    def _make_card(self, row, rm, key, done, total, pct) -> ctk.CTkFrame:
        card = ctk.CTkFrame(self.scroll, fg_color=COLORS["card"], corner_radius=16,
                             border_width=1, border_color=COLORS["border"])
        card.grid_columnconfigure(1, weight=1)
        card.target_pct = pct # Store for animation

        # Left: Large Icon
        ctk.CTkLabel(card, text=rm.get("icon", "📋"),
                     font=ctk.CTkFont(size=40)).grid(row=0, column=0, rowspan=3, padx=20, pady=20)

        # Middle: Info
        ctk.CTkLabel(card, text=rm.get("title", key),
                     font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=1, sticky="sw", pady=(18, 2))

        ctk.CTkLabel(card, text=f"{done}/{total} topics completed",
                     font=ctk.CTkFont(size=12), text_color=COLORS["muted"]).grid(row=1, column=1, sticky="nw")

        # Progress Bar
        card.prog_bar = ctk.CTkProgressBar(card, height=10, width=350,
                                           progress_color=COLORS["teal"] if pct > 0 else COLORS["border"],
                                           fg_color=COLORS["sidebar"])
        card.prog_bar.set(0) # Start at 0 for animation
        card.prog_bar.grid(row=2, column=1, sticky="nw", pady=(10, 20))

        ctk.CTkLabel(card, text=f"{pct:.0f}%", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=COLORS["teal"]).grid(row=2, column=2, padx=15, pady=(0, 10))

        # Right: Action Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.grid(row=0, column=3, rowspan=3, padx=20)

        cont_btn = ctk.CTkButton(btn_frame, text="Continue →", width=120, height=36,
                                fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                                corner_radius=10, font=ctk.CTkFont(size=12, weight="bold"),
                                command=lambda k=key: self.on_continue(k))
        cont_btn.pack(pady=5)

        rem_btn = ctk.CTkButton(btn_frame, text="Remove", width=120, height=32,
                               fg_color="transparent", text_color=COLORS["error"],
                               hover_color="#331A1D", border_width=1, border_color="#331A1D",
                               command=lambda k=key: self._remove_roadmap(k))
        rem_btn.pack(pady=5)

        # Interaction: Hover Glow
        def on_enter(e):
            card.configure(border_color=COLORS["accent"], fg_color=COLORS["card_glow"])
        def on_leave(e):
            card.configure(border_color=COLORS["border"], fg_color=COLORS["card"])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        return card

    def _remove_roadmap(self, key: str):
        """Directly removes the roadmap and refreshes the UI."""
        try:
            from database.db import remove_saved_roadmap
            # Perform deletion
            remove_saved_roadmap(self.user["id"], key)
            
            # Show a temporary success toast
            toast = ctk.CTkLabel(self, text="Roadmap Removed", 
                                 text_color=COLORS["error"], font=ctk.CTkFont(size=12, weight="bold"))
            toast.place(relx=0.5, rely=0.05, anchor="n")
            self.after(2000, toast.destroy)
            
            # Immediate Re-render
            self._render(self.sort_var.get())
            
        except Exception as e:
            print(f"Error removing roadmap: {e}")