"""
ui/profile_panel.py - User profile and completion stats
"""
import customtkinter as ctk
import json
import tkinter as tk

COLORS = {
    "bg": "#0D0F14", "card": "#1A1D27", "accent": "#6C63FF",
    "teal": "#00D4AA", "text": "#F0F0F5", "muted": "#7A7F9A",
    "border": "#2A2D3E", "sidebar": "#12151C"
}

class ProfilePanel(ctk.CTkFrame):
    def __init__(self, master, user: dict):
        super().__init__(master, fg_color=COLORS["bg"])
        self.user = user
        self._is_editing = False
        self._anim_widgets = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build()

    def _build(self):
        # Header
        self.hdr_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.hdr_frame.grid(row=0, column=0, sticky="ew", padx=32, pady=(28, 12))
        
        ctk.CTkLabel(self.hdr_frame, text="👤  My Profile",
                     font=ctk.CTkFont(size=26, weight="bold"),
                     text_color=COLORS["text"]).pack(side="left")

        # Edit/Save Toggle Button
        self.edit_btn = ctk.CTkButton(self.hdr_frame, text="Edit Profile", width=100, height=32,
                                     fg_color=COLORS["sidebar"], border_width=1, border_color=COLORS["border"],
                                     hover_color=COLORS["card"], command=self._toggle_edit)
        self.edit_btn.pack(side="right")
        
        self.hdr_frame.grid_remove()
        self._anim_widgets.append(self.hdr_frame)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg"],
                                              scrollbar_button_color=COLORS["border"])
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 16))
        self.scroll.grid_columnconfigure(0, weight=1)

        self._render_content()
        self.after(100, self._run_entrance_animation)

    def _render_content(self):
        self._anim_widgets.clear()
        
        # Clear scroll content for re-rendering
        for w in self.scroll.winfo_children():
            w.destroy()

        # ── User info / Editor card ──────────────────────────────────────────
        self.info_card = self._card(self.scroll)
        self.info_card.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        
        self.info_card.grid_remove()
        self._anim_widgets.append(self.info_card)
        
        if not self._is_editing:
            self._render_view_mode()
        else:
            self._render_edit_mode()

        # ── Stats Section (Remains visible always) ───────────────────────────
        self._render_stats()

    def _render_view_mode(self):
        avatar = ctk.CTkLabel(self.info_card, text=self.user.get("avatar", "👤"), font=ctk.CTkFont(size=60))
        avatar.grid(row=0, column=0, rowspan=2, padx=24, pady=24)
        
        ctk.CTkLabel(self.info_card, text=self.user.get("username", "User"),
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=COLORS["text"]).grid(row=0, column=1, sticky="sw", pady=(24, 0))
        ctk.CTkLabel(self.info_card, text=self.user.get("email", ""),
                     font=ctk.CTkFont(size=14),
                     text_color=COLORS["muted"]).grid(row=1, column=1, sticky="nw")

    def _render_edit_mode(self):
        # Avatar Selector
        self.avatar_var = tk.StringVar(value=self.user.get("avatar", "👤"))
        ctk.CTkLabel(self.info_card, text="Avatar", font=ctk.CTkFont(size=12, weight="bold"), 
                     text_color=COLORS["muted"]).grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        
        avatar_menu = ctk.CTkOptionMenu(self.info_card, values=["👤", "👨‍💻", "👩‍💻", "🚀", "🎓", "🤖"],
                                       variable=self.avatar_var, width=80, fg_color=COLORS["sidebar"])
        avatar_menu.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Username Input
        ctk.CTkLabel(self.info_card, text="Username", font=ctk.CTkFont(size=12, weight="bold"), 
                     text_color=COLORS["muted"]).grid(row=0, column=1, padx=10, pady=(20, 0), sticky="w")
        self.username_entry = ctk.CTkEntry(self.info_card, width=200, placeholder_text="New Username")
        self.username_entry.insert(0, self.user.get("username", ""))
        self.username_entry.grid(row=1, column=1, padx=10, pady=(0, 20), sticky="w")

        # Email Input
        ctk.CTkLabel(self.info_card, text="Email", font=ctk.CTkFont(size=12, weight="bold"), 
                     text_color=COLORS["muted"]).grid(row=0, column=2, padx=10, pady=(20, 0), sticky="w")
        self.email_entry = ctk.CTkEntry(self.info_card, width=200, placeholder_text="New Email")
        self.email_entry.insert(0, self.user.get("email", ""))
        self.email_entry.grid(row=1, column=2, padx=10, pady=(0, 20), sticky="w")

    def _toggle_edit(self):
        if self._is_editing:
            self._save_profile()
        else:
            self._is_editing = True
            self.edit_btn.configure(text="Save Profile", fg_color=COLORS["teal"], text_color=COLORS["bg"])
            self._render_content()
            self._anim_widgets.append(self.hdr_frame) # Re-add header to animation as it's outside scroll
            self._run_entrance_animation()

    def _save_profile(self):
        new_username = self.username_entry.get().strip()
        new_email = self.email_entry.get().strip()
        new_avatar = self.avatar_var.get()

        if not new_username or not new_email:
            self._show_error("Username and email are required")
            return 

        # Update Database First
        try:
            from database.db import update_user_profile
            import sqlite3
            update_user_profile(self.user["id"], new_username, new_email, new_avatar)
            
            # If successful, Update local object
            self.user["username"] = new_username
            self.user["email"] = new_email
            self.user["avatar"] = new_avatar
            
            self._is_editing = False
            self.edit_btn.configure(text="Edit Profile", fg_color=COLORS["sidebar"], text_color=COLORS["text"])
            self._render_content()
            self._anim_widgets.append(self.hdr_frame)
            self._run_entrance_animation()
            
        except ImportError:
            pass
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                self._show_error("Username or email already taken.")
            else:
                self._show_error(f"Update failed: {e}")

    def _show_error(self, message):
        """Display an error message briefly."""
        err_lbl = ctk.CTkLabel(self.info_card, text=message, text_color="#FF6B6B", font=ctk.CTkFont(size=12))
        err_lbl.grid(row=2, column=0, columnspan=3, pady=(0, 10))
        self.after(3000, err_lbl.destroy)

    def _render_stats(self):
        from database.db import get_saved_roadmaps
        from core.roadmap_data2 import ROADMAPS
        
        saved = get_saved_roadmaps(self.user["id"])
        
        total_completed = 0
        total_topics = 0
        roadmap_stats = []

        for row in saved:
            r_key = row["roadmap_key"]
            try:
                progress = json.loads(row["progress_json"])
            except Exception:
                progress = {}
                
            r_completed = sum(1 for val in progress.values() if val)
            total_completed += r_completed
            
            # Find total topics in this roadmap
            r_total = 0
            r_data = ROADMAPS.get(r_key)
            if r_data:
                for phase in r_data.get("phases", []):
                    r_total += len(phase.get("topics", []))
            
            total_topics += r_total
            if r_total > 0:
                roadmap_stats.append((r_data.get("title", r_key), r_completed, r_total))

        # ── Overall Stats Row ───────────────────────────────────────
        stats_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        stats_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Stat 1: Total Completed Topics
        s1 = self._card(stats_frame)
        s1.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        s1.grid_remove()
        self._anim_widgets.append(s1)
        ctk.CTkLabel(s1, text="✅", font=ctk.CTkFont(size=24)).pack(pady=(16, 4))
        ctk.CTkLabel(s1, text=str(total_completed), font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=COLORS["teal"]).pack()
        ctk.CTkLabel(s1, text="Topics Completed", font=ctk.CTkFont(size=12),
                     text_color=COLORS["muted"]).pack(pady=(0, 16))

        # Stat 2: Completion Percentage (of saved roadmaps)
        s2 = self._card(stats_frame)
        s2.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        s2.grid_remove()
        self._anim_widgets.append(s2)
        pct = int((total_completed / total_topics * 100)) if total_topics > 0 else 0
        ctk.CTkLabel(s2, text="🏆", font=ctk.CTkFont(size=24)).pack(pady=(16, 4))
        ctk.CTkLabel(s2, text=f"{pct}%", font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=COLORS["accent"]).pack()
        ctk.CTkLabel(s2, text="Overall Score", font=ctk.CTkFont(size=12),
                     text_color=COLORS["muted"]).pack(pady=(0, 16))

        # ── Breakdown ───────────────────────────────────────────────
        if roadmap_stats:
            breakdown_card = self._card(self.scroll)
            breakdown_card.grid(row=2, column=0, sticky="ew")
            breakdown_card.grid_remove()
            self._anim_widgets.append(breakdown_card)
            ctk.CTkLabel(breakdown_card, text="Roadmap Progress",
                         font=ctk.CTkFont(size=15, weight="bold"),
                         text_color=COLORS["text"]).pack(anchor="w", padx=16, pady=(16, 8))
            
            for title, comp, tot in roadmap_stats:
                row_f = ctk.CTkFrame(breakdown_card, fg_color="transparent")
                row_f.pack(fill="x", padx=16, pady=6)
                ctk.CTkLabel(row_f, text=title, font=ctk.CTkFont(size=13),
                             text_color=COLORS["text"]).pack(side="left")
                ctk.CTkLabel(row_f, text=f"{comp} / {tot}", font=ctk.CTkFont(size=13, weight="bold"),
                             text_color=COLORS["teal"]).pack(side="right")
                
                # Progress bar
                prog = ctk.CTkProgressBar(breakdown_card, height=8, fg_color=COLORS["sidebar"],
                                          progress_color=COLORS["teal"])
                prog.pack(fill="x", padx=16, pady=(0, 10))
                prog.set(comp / tot if tot > 0 else 0)

    def _card(self, parent) -> ctk.CTkFrame:
        f = ctk.CTkFrame(parent, fg_color=COLORS["card"], corner_radius=12)
        return f

    def refresh(self):
        """Called when navigating to this panel to reload stats."""
        self._is_editing = False
        self._anim_widgets.append(self.hdr_frame) # Header gets re-animated
        self._render_content()
        self._run_entrance_animation()

    def _run_entrance_animation(self):
        """Staggered reveal animation for profile elements."""
        if self._anim_widgets:
            widget = self._anim_widgets.pop(0)
            try:
                widget.grid()
                # Fade-in flash effect
                if hasattr(widget, 'cget') and hasattr(widget, 'configure'):
                    orig_bg = widget.cget("fg_color")
                    if orig_bg != "transparent":
                        widget.configure(fg_color="#25293D")
                        self.after(100, lambda w=widget, bg=orig_bg: w.configure(fg_color=bg))
            except Exception:
                pass
            self.after(70, self._run_entrance_animation)
