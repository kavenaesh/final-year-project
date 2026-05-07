"""
ui/app_window.py - Main application window with collapsible sidebar (fixed)
"""
import customtkinter as ctk
import tkinter as tk

COLORS = {
    "bg": "#0D0F14",
    "card": "#1A1D27",
    "accent": "#6C63FF",
    "accent_hover": "#7C73FF",
    "teal": "#00D4AA",
    "text": "#F0F0F5",
    "muted": "#7A7F9A",
    "error": "#FF6B6B",
    "sidebar": "#12151C",
    "border": "#2A2D3E",
    "nav_active_bg": "#1E2035",
}

NAV_ITEMS = [
    ("🏠", "Dashboard"),
    ("🗺️", "Roadmaps"),
    ("🤖", "AI Advisor"),
    ("📚", "Resources"),
    ("💾", "Saved"),
    ("⚙️", "Settings"),
]


class AppWindow(ctk.CTkFrame):
    def __init__(self, master, user: dict, token: str, on_logout):
        super().__init__(master, fg_color=COLORS["bg"])
        self.master = master
        self.user = user
        self.token = token
        self.on_logout = on_logout
        self._sidebar_expanded = True
        self._active_nav = "Dashboard"
        self._nav_buttons = {}
        self._nav_indicators = {}
        self._content_frames = {}

        self._build()
        self._build_panels()
        self._show_panel("Dashboard")

    def _build(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ─── SIDEBAR ─────────────────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self, fg_color=COLORS["sidebar"], width=240,
                                     corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_columnconfigure(0, weight=1)

        # Logo
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, sticky="ew", padx=16, pady=(24, 12))
        self.logo_icon = ctk.CTkLabel(self.logo_frame, text="🎯",
                                       font=ctk.CTkFont(size=26))
        self.logo_icon.pack(side="left", padx=(0, 8))
        self.logo_text = ctk.CTkLabel(self.logo_frame, text="CareerPath AI",
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       text_color=COLORS["text"])
        self.logo_text.pack(side="left")

        # Divider
        ctk.CTkFrame(self.sidebar, height=1, fg_color=COLORS["border"]).grid(
            row=1, column=0, sticky="ew", padx=12, pady=(0, 6))

        # Nav items — row frame with left accent indicator + button
        for idx, (icon, label) in enumerate(NAV_ITEMS):
            row_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=46)
            row_frame.grid(row=idx + 2, column=0, sticky="ew", padx=4, pady=2)
            row_frame.grid_propagate(False)
            row_frame.grid_columnconfigure(1, weight=1)

            indicator = ctk.CTkFrame(row_frame, width=3, height=28,
                                      fg_color="transparent", corner_radius=2)
            indicator.grid(row=0, column=0, padx=(4, 0), pady=9)
            self._nav_indicators[label] = indicator

            btn = ctk.CTkButton(
                row_frame,
                text=f"{icon}   {label}",
                height=38, anchor="w",
                fg_color="transparent",
                hover_color=COLORS["nav_active_bg"],
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=13),
                corner_radius=8,
                command=lambda l=label: self._show_panel(l)
            )
            btn.grid(row=0, column=1, sticky="ew", padx=(2, 4))
            self._nav_buttons[label] = btn

        # Spacer pushes user card to bottom
        self.sidebar.grid_rowconfigure(len(NAV_ITEMS) + 2, weight=1)

        # User card - clickable for Profile pane
        self.user_frame = ctk.CTkFrame(self.sidebar, fg_color=COLORS["card"], corner_radius=10, cursor="hand2")
        self.user_frame.grid(row=len(NAV_ITEMS) + 3, column=0, sticky="ew", padx=10, pady=(0, 6))
        self.user_frame.grid_columnconfigure(1, weight=1)

        def _hover_user(e): self.user_frame.configure(fg_color=COLORS["border"])
        def _leave_user(e): self.user_frame.configure(fg_color=COLORS["card"])
        def _click_user(e): self._show_panel("Profile")

        self.user_frame.bind("<Enter>", _hover_user)
        self.user_frame.bind("<Leave>", _leave_user)
        self.user_frame.bind("<Button-1>", _click_user)

        self.user_avatar = ctk.CTkLabel(self.user_frame, text="👤", font=ctk.CTkFont(size=20), cursor="hand2")
        self.user_avatar.grid(row=0, column=0, padx=(10, 6), pady=10)
        self.user_avatar.bind("<Button-1>", _click_user)

        user_info = ctk.CTkFrame(self.user_frame, fg_color="transparent")
        user_info.grid(row=0, column=1, sticky="w", pady=10)
        self.user_name_lbl = ctk.CTkLabel(
            user_info, text=self.user.get("username", "User"),
            font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["text"], cursor="hand2")
        self.user_name_lbl.pack(anchor="w")
        self.user_name_lbl.bind("<Button-1>", _click_user)
        
        self.user_email_lbl = ctk.CTkLabel(
            user_info, text=self.user.get("email", ""),
            font=ctk.CTkFont(size=10), text_color=COLORS["muted"], cursor="hand2")
        self.user_email_lbl.pack(anchor="w")
        self.user_email_lbl.bind("<Button-1>", _click_user)

        # Collapse button
        self.collapse_btn = ctk.CTkButton(
            self.sidebar, text="◀  Collapse", height=34,
            fg_color="transparent", hover_color=COLORS["border"],
            text_color=COLORS["muted"], font=ctk.CTkFont(size=11),
            anchor="w", corner_radius=8,
            command=self._toggle_sidebar
        )
        self.collapse_btn.grid(row=len(NAV_ITEMS) + 4, column=0,
                                sticky="ew", padx=8, pady=(2, 14))

        # ─── CONTENT AREA ────────────────────────────────────────────
        self.content_area = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

    def _build_panels(self):
        from ui.dashboard import DashboardPanel
        from ui.roadmap_browser import RoadmapBrowser
        from ui.ai_advisor import AIAdvisorPanel
        from ui.resources import ResourcesPanel
        from ui.saved_roadmaps import SavedRoadmapsPanel
        from ui.settings import SettingsPanel
        from ui.profile_panel import ProfilePanel

        panel_classes = {
            "Dashboard": (DashboardPanel, {
                "user": self.user,
                "on_navigate": self._on_dashboard_navigate,
            }),
            "Roadmaps": (RoadmapBrowser, {
                "user": self.user,
                "on_view_roadmap": self._open_roadmap,
            }),
            "AI Advisor": (AIAdvisorPanel, {"user": self.user}),
            "Resources":  (ResourcesPanel, {}),
            "Saved":      (SavedRoadmapsPanel, {
                "user": self.user,
                "on_continue": self._open_roadmap,
            }),
            "Settings":   (SettingsPanel, {
                "user": self.user,
                "on_logout": self._handle_logout,
            }),
            "Profile":    (ProfilePanel, {
                "user": self.user
            }),
        }

        for name, (cls, kwargs) in panel_classes.items():
            try:
                frame = cls(self.content_area, **kwargs)
                frame.grid(row=0, column=0, sticky="nsew")
                self._content_frames[name] = frame
            except Exception as e:
                err_frame = ctk.CTkFrame(self.content_area, fg_color=COLORS["bg"])
                err_frame.grid(row=0, column=0, sticky="nsew")
                ctk.CTkLabel(err_frame, text=f"⚠️ Error loading {name}:\n{e}",
                             text_color=COLORS["error"],
                             font=ctk.CTkFont(size=13)).pack(expand=True)
                self._content_frames[name] = err_frame

    def _on_dashboard_navigate(self, roadmap_key: str):
        """Dashboard quick-start cards call this with the roadmap key directly."""
        self._open_roadmap(roadmap_key)

    def _open_roadmap(self, roadmap_key: str):
        from ui.roadmap_view import RoadmapViewPanel
        if "roadmap_view" in self._content_frames:
            self._content_frames["roadmap_view"].destroy()
            del self._content_frames["roadmap_view"]

        view = RoadmapViewPanel(
            self.content_area,
            roadmap_key=roadmap_key,
            user=self.user,
            on_back=lambda: self._show_panel("Roadmaps")
        )
        view.grid(row=0, column=0, sticky="nsew")
        self._content_frames["roadmap_view"] = view
        self._show_panel("roadmap_view")

    def _show_panel(self, name: str):
        for label, btn in self._nav_buttons.items():
            ind = self._nav_indicators[label]
            if label == name:
                btn.configure(fg_color=COLORS["nav_active_bg"],
                              text_color=COLORS["text"],
                              font=ctk.CTkFont(size=13, weight="bold"))
                ind.configure(fg_color=COLORS["accent"])
            else:
                btn.configure(fg_color="transparent",
                              text_color=COLORS["muted"],
                              font=ctk.CTkFont(size=13))
                ind.configure(fg_color="transparent")
        self._active_nav = name
        if name in self._content_frames:
            panel = self._content_frames[name]
            if hasattr(panel, "refresh"):
                panel.refresh()
            panel.tkraise()

    def _toggle_sidebar(self):
        if self._sidebar_expanded:
            self.sidebar.configure(width=60)
            self.logo_text.pack_forget()
            for (icon, _label), btn in zip(NAV_ITEMS, self._nav_buttons.values()):
                btn.configure(text=icon, anchor="center", width=44,
                              font=ctk.CTkFont(size=16))
            self.user_name_lbl.pack_forget()
            self.user_email_lbl.pack_forget()
            self.collapse_btn.configure(text="▶", anchor="center")
            self._sidebar_expanded = False
        else:
            self.sidebar.configure(width=240)
            self.logo_text.pack(side="left")
            for (icon, label), btn in zip(NAV_ITEMS, self._nav_buttons.values()):
                btn.configure(text=f"{icon}   {label}", anchor="w", width=200,
                              font=ctk.CTkFont(size=13))
            self.user_name_lbl.pack(anchor="w")
            self.user_email_lbl.pack(anchor="w")
            self.collapse_btn.configure(text="◀  Collapse", anchor="w")
            self._sidebar_expanded = True

    def _handle_logout(self):
        from auth.auth import logout_user
        logout_user(self.user["id"], self.token)
        self.on_logout()
