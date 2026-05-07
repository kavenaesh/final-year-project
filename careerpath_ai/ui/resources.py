"""
ui/resources.py - Professional Animated Resources Browser
"""
import customtkinter as ctk
import tkinter as tk
import webbrowser

COLORS = {
    "bg": "#0D0F14", "card": "#1A1D27", "accent": "#6C63FF",
    "accent_hover": "#7C73FF", "teal": "#00D4AA", "text": "#F0F0F5",
    "muted": "#7A7F9A", "error": "#FF6B6B", "sidebar": "#12151C", "border": "#2A2D3E",
}

TYPE_ICONS = {"youtube": "▶", "website": "🌐", "udemy": "🎓", "coursera": "🎓", "other": "📖"}
TYPE_COLORS = {"youtube": "#FF4B4B", "website": COLORS["teal"], "udemy": "#A435F0",
               "coursera": "#0056D2", "other": COLORS["muted"]}

def _build_all_resources():
    try:
        from core.roadmap_data2 import ROADMAPS
    except Exception:
        return []

    items = []
    for key, rm in ROADMAPS.items():
        for phase in rm.get("phases", []):
            for topic in phase.get("topics", []):
                ress = topic.get("resources", {})
                for section in ("free", "paid"):
                    for r in ress.get(section, []):
                        items.append({
                            "name": r["name"],
                            "url": r["url"],
                            "type": r.get("type", "website"),
                            "track": rm.get("title", key),
                            "topic": topic["name"],
                            "free": section == "free",
                        })
    return items

class ResourcesPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLORS["bg"])
        self._all = _build_all_resources()
        self._filter_type = "All"
        self._filter_free = "All"
        self._anim_queue = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._build()

    def _build(self):
        # --- Header ---
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=40, pady=(35, 15))
        
        ctk.CTkLabel(hdr, text="Learning Library",
                     font=ctk.CTkFont(size=30, weight="bold"),
                     text_color=COLORS["text"]).pack(side="left")
        
        count_badge = ctk.CTkLabel(hdr, text=f"{len(self._all)} Resources",
                                   font=ctk.CTkFont(size=12, weight="bold"),
                                   text_color=COLORS["accent"], fg_color=COLORS["sidebar"],
                                   corner_radius=8, width=100, height=26)
        count_badge.pack(side="left", padx=20)

        # --- Filters Bar ---
        filters = ctk.CTkFrame(self, fg_color=COLORS["sidebar"], height=70, corner_radius=15)
        filters.grid(row=1, column=0, sticky="ew", padx=40, pady=(0, 20))
        filters.pack_propagate(False)

        # Search with focus animation
        search_frame = ctk.CTkFrame(filters, fg_color=COLORS["card"], corner_radius=10, 
                                    border_width=1, border_color=COLORS["border"])
        search_frame.pack(side="left", padx=15, pady=15)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._render())
        
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, 
                                    placeholder_text="Search topics, skills, or titles...",
                                    width=300, height=36, fg_color="transparent", border_width=0)
        search_entry.pack(side="left", padx=5)
        
        search_entry.bind("<FocusIn>", lambda e: search_frame.configure(border_color=COLORS["accent"]))
        search_entry.bind("<FocusOut>", lambda e: search_frame.configure(border_color=COLORS["border"]))

        # Dropdowns
        self._create_dropdown(filters, ["All", "YouTube", "Website", "Udemy", "Coursera"], 
                             "Category", self._set_type).pack(side="left", padx=5)
        
        self._create_dropdown(filters, ["All", "Free", "Paid"], 
                             "Price", self._set_free).pack(side="left", padx=5)

        # --- Scrollable Area ---
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                             scrollbar_button_color=COLORS["border"],
                                             scrollbar_button_hover_color=COLORS["accent"])
        self.scroll.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.scroll.grid_columnconfigure((0, 1, 2), weight=1)
        
        self._render()

    def _create_dropdown(self, parent, values, label, command):
        var = tk.StringVar(value=values[0])
        menu = ctk.CTkOptionMenu(parent, values=values, variable=var, 
                                 width=120, height=38, corner_radius=10,
                                 fg_color=COLORS["card"], button_color=COLORS["card"],
                                 button_hover_color=COLORS["border"],
                                 text_color=COLORS["muted"],
                                 command=command)
        return menu

    def _set_type(self, v):
        self._filter_type = v
        self._render()

    def _set_free(self, v):
        self._filter_free = v
        self._render()

    def _render(self):
        # Clear existing
        for w in self.scroll.winfo_children():
            w.destroy()
        
        self._anim_queue = []
        query = self.search_var.get().lower()
        
        filtered = [
            r for r in self._all 
            if (not query or query in r["name"].lower() or query in r["topic"].lower() or query in r["track"].lower())
            and (self._filter_type == "All" or r["type"].lower() == self._filter_type.lower())
            and (self._filter_free == "All" or (self._filter_free == "Free" and r["free"]) or (self._filter_free == "Paid" and not r["free"]))
        ]

        # Deduplicate
        seen = set()
        unique = []
        for r in filtered:
            if r["url"] not in seen:
                seen.add(r["url"])
                unique.append(r)

        if not unique:
            err = ctk.CTkLabel(self.scroll, text="No matching resources found. Try a different search! ✨",
                               font=ctk.CTkFont(size=14), text_color=COLORS["muted"])
            err.grid(row=0, column=0, columnspan=3, pady=100)
            return

        # Create cards and queue them for animation
        for i, r in enumerate(unique[:60]): # Limit to 60 for performance
            col, row = i % 3, i // 3
            card = self._make_card(r)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
            card.grid_remove() # Hide initially
            self._anim_queue.append(card)
        
        self._animate_cards()

    def _animate_cards(self, index=0):
        if index < len(self._anim_queue):
            card = self._anim_queue[index]
            card.grid()
            # Professional pop-in effect
            card.configure(border_color=COLORS["accent"])
            self.after(80, lambda: card.configure(border_color=COLORS["border"]))
            
            # Cascading speed
            self.after(40, lambda: self._animate_cards(index + 1))

    def _make_card(self, r: dict) -> ctk.CTkFrame:
        card = ctk.CTkFrame(self.scroll, fg_color=COLORS["card"], corner_radius=18, 
                            border_width=1, border_color=COLORS["border"])
        card.grid_columnconfigure(0, weight=1)

        # Header: Type & Status
        rtype = r.get("type", "website")
        icon = TYPE_ICONS.get(rtype, "🔗")
        icolor = TYPE_COLORS.get(rtype, COLORS["muted"])

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 10))
        
        ctk.CTkLabel(top, text=f"{icon}  {rtype.upper()}", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=icolor).pack(side="left")
        
        price_tag = "FREE" if r["free"] else "PAID"
        price_color = COLORS["teal"] if r["free"] else COLORS["accent"]
        ctk.CTkLabel(top, text=price_tag, font=ctk.CTkFont(size=9, weight="bold"),
                     text_color=price_color, fg_color=COLORS["bg"], 
                     corner_radius=5, width=45).pack(side="right")

        # Title
        ctk.CTkLabel(card, text=r["name"], font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=COLORS["text"], wraplength=220, justify="left").grid(
                     row=1, column=0, sticky="w", padx=18, pady=(0, 5))

        # Context path
        path_text = f"{r['track']}  •  {r['topic']}"
        ctk.CTkLabel(card, text=path_text, font=ctk.CTkFont(size=11), 
                     text_color=COLORS["muted"], wraplength=220, justify="left").grid(
                     row=2, column=0, sticky="w", padx=18, pady=(0, 15))

        # Professional Button
        btn = ctk.CTkButton(card, text="Access Resource  ↗", height=38, 
                            fg_color=COLORS["sidebar"], hover_color=COLORS["accent"],
                            border_width=1, border_color=COLORS["border"],
                            corner_radius=12, font=ctk.CTkFont(size=12, weight="bold"),
                            command=lambda url=r["url"]: webbrowser.open(url))
        btn.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 18))

        # Hover FX
        def on_enter(e):
            card.configure(border_color=COLORS["accent"], fg_color="#1E2230")
            btn.configure(fg_color=COLORS["accent"], border_width=0)
        def on_leave(e):
            card.configure(border_color=COLORS["border"], fg_color=COLORS["card"])
            btn.configure(fg_color=COLORS["sidebar"], border_width=1)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        return card