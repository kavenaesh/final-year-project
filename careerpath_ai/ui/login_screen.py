"""
ui/login_screen.py - Professional Animated Login & Register screen
"""
import customtkinter as ctk
import tkinter as tk
import math

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
}

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master, fg_color=COLORS["bg"])
        self.master = master
        self.on_login_success = on_login_success
        self._alpha = 0.0
        self._mode = "login"
        self._anim_widgets = []
        
        self._build()
        self._fade_in()
        # Start content reveal after a short delay
        self.after(200, self._run_entrance_animation)

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main Card with "Pop-in" preparation
        self.card = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=24,
                                  border_width=1, border_color=COLORS["border"])
        self.card.grid(row=0, column=0, padx=20, pady=20)
        self.card.grid_columnconfigure(0, weight=1)
        
        # --- 1. Logo & Title ---
        logo_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        logo_frame.grid(row=0, column=0, pady=(30, 5), padx=40)

        self.logo_lbl = ctk.CTkLabel(logo_frame, text="🎯", font=ctk.CTkFont(size=58))
        self.logo_lbl.pack()
        
        self.title_lbl = ctk.CTkLabel(logo_frame, text="CareerPath AI",
                                     font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
                                     text_color=COLORS["accent"])
        self.title_lbl.pack(pady=(4, 0))
        
        self.sub_lbl = ctk.CTkLabel(logo_frame, text="Your Intelligent Career Navigator",
                                   font=ctk.CTkFont(size=13), text_color=COLORS["muted"])
        self.sub_lbl.pack()
        
        # Add to anim queue
        self._anim_widgets.append(logo_frame)

        # --- 2. Toggle Tabs ---
        self.toggle_frame = ctk.CTkFrame(self.card, fg_color=COLORS["sidebar"], corner_radius=12)
        self.toggle_frame.grid(row=1, column=0, pady=(20, 0), padx=40)
        self._anim_widgets.append(self.toggle_frame)

        self.btn_login_tab = ctk.CTkButton(
            self.toggle_frame, text="Login", width=140, height=40,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"),
            command=self._show_login
        )
        self.btn_login_tab.grid(row=0, column=0, padx=5, pady=5)

        self.btn_register_tab = ctk.CTkButton(
            self.toggle_frame, text="Register", width=140, height=40,
            fg_color="transparent", text_color=COLORS["muted"],
            hover_color=COLORS["border"], corner_radius=10, font=ctk.CTkFont(size=13),
            command=self._show_register
        )
        self.btn_register_tab.grid(row=0, column=1, padx=5, pady=5)

        # --- 3. Form Container ---
        self.form_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.form_frame.grid(row=2, column=0, pady=(15, 0), padx=40)
        self.form_frame.grid_columnconfigure(0, weight=1)
        self._anim_widgets.append(self.form_frame)

        # Username
        self.username_label = ctk.CTkLabel(self.form_frame, text="Username", anchor="w",
                                           font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["muted"])
        self.username_entry = ctk.CTkEntry(self.form_frame, width=340, height=45,
                                           placeholder_text="Choose a username",
                                           fg_color=COLORS["sidebar"], border_color=COLORS["border"],
                                           corner_radius=12)
        self.username_err = self._make_err_label()

        # Email
        self.email_label = ctk.CTkLabel(self.form_frame, text="Email Address", anchor="w",
                                        font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["muted"])
        self.email_label.grid(row=3, column=0, sticky="w", pady=(12, 2))
        self.email_entry = ctk.CTkEntry(self.form_frame, width=340, height=45,
                                        placeholder_text="you@example.com",
                                        fg_color=COLORS["sidebar"], border_color=COLORS["border"],
                                        corner_radius=12)
        self.email_entry.grid(row=4, column=0)
        self.email_err = self._make_err_label()
        self.email_err.grid(row=5, column=0, sticky="w")

        # Password
        self.pass_label = ctk.CTkLabel(self.form_frame, text="Password", anchor="w",
                                       font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["muted"])
        self.pass_label.grid(row=6, column=0, sticky="w", pady=(12, 2))
        self.pass_entry = ctk.CTkEntry(self.form_frame, width=340, height=45,
                                       placeholder_text="Enter password", show="•",
                                       fg_color=COLORS["sidebar"], border_color=COLORS["border"],
                                       corner_radius=12)
        self.pass_entry.grid(row=7, column=0)
        self.pass_err = self._make_err_label()
        self.pass_err.grid(row=8, column=0, sticky="w")

        # Confirm Password
        self.confirm_label = ctk.CTkLabel(self.form_frame, text="Confirm Password", anchor="w",
                                          font=ctk.CTkFont(size=12, weight="bold"), text_color=COLORS["muted"])
        self.confirm_entry = ctk.CTkEntry(self.form_frame, width=340, height=45,
                                          placeholder_text="Repeat your password", show="•",
                                          fg_color=COLORS["sidebar"], border_color=COLORS["border"],
                                          corner_radius=12)
        self.confirm_err = self._make_err_label()

        # Remember Me
        self.remember_var = tk.BooleanVar(value=False)
        self.remember_check = ctk.CTkCheckBox(
            self.form_frame, text="Stay signed in", variable=self.remember_var,
            font=ctk.CTkFont(size=12), text_color=COLORS["muted"],
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"]
        )
        self.remember_check.grid(row=12, column=0, pady=(15, 0), sticky="w")

        self.global_err = ctk.CTkLabel(self.form_frame, text="", font=ctk.CTkFont(size=12),
                                       text_color=COLORS["error"], wraplength=340)
        self.global_err.grid(row=13, column=0, pady=(8, 0))

        # --- 4. Submit & Footer ---
        self.submit_btn = ctk.CTkButton(
            self.card, text="Sign In", width=340, height=50,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            corner_radius=12, font=ctk.CTkFont(size=15, weight="bold"),
            command=self._submit
        )
        self.submit_btn.grid(row=3, column=0, pady=(20, 0), padx=40)
        self._anim_widgets.append(self.submit_btn)

        self.bottom_label = ctk.CTkLabel(
            self.card, text="New here? Create an account above.",
            font=ctk.CTkFont(size=12), text_color=COLORS["muted"]
        )
        self.bottom_label.grid(row=4, column=0, pady=(10, 30))
        self._anim_widgets.append(self.bottom_label)

        # Prepare for animation: hide initially
        for w in self._anim_widgets:
            w.grid_remove()

        self.master.bind("<Return>", lambda e: self._submit())

    # --- Animations ---

    def _run_entrance_animation(self):
        """Staggered reveal of form elements with a vertical slide."""
        if self._anim_widgets:
            widget = self._anim_widgets.pop(0)
            widget.grid()
            # Micro-interaction: momentary glow on appearance
            if hasattr(widget, 'configure') and 'border_color' in widget.keys():
                widget.configure(border_color=COLORS["accent"])
                self.after(150, lambda w=widget: w.configure(border_color=COLORS["border"]))
            self.after(80, self._run_entrance_animation)

    def _fade_in(self):
        try:
            self.master.wm_attributes("-alpha", self._alpha)
            if self._alpha < 1.0:
                self._alpha += 0.05
                self.after(15, self._fade_in)
            else:
                self.master.wm_attributes("-alpha", 1.0)
        except: pass

    # --- Logic & State Handling ---

    def _show_login(self):
        if self._mode == "login": return
        self._mode = "login"
        self.btn_login_tab.configure(fg_color=COLORS["accent"], text_color=COLORS["text"], font=ctk.CTkFont(size=13, weight="bold"))
        self.btn_register_tab.configure(fg_color="transparent", text_color=COLORS["muted"], font=ctk.CTkFont(size=13))
        
        self.username_label.grid_remove()
        self.username_entry.grid_remove()
        self.username_err.grid_remove()
        self.confirm_label.grid_remove()
        self.confirm_entry.grid_remove()
        self.confirm_err.grid_remove()
        self.remember_check.grid()
        
        self.submit_btn.configure(text="Sign In")
        self.bottom_label.configure(text="New here? Create an account above.")
        self._clear_errors()

    def _show_register(self):
        if self._mode == "register": return
        self._mode = "register"
        self.btn_register_tab.configure(fg_color=COLORS["accent"], text_color=COLORS["text"], font=ctk.CTkFont(size=13, weight="bold"))
        self.btn_login_tab.configure(fg_color="transparent", text_color=COLORS["muted"], font=ctk.CTkFont(size=13))
        
        self.username_label.grid(row=0, column=0, sticky="w", pady=(5, 2))
        self.username_entry.grid(row=1, column=0)
        self.username_err.grid(row=2, column=0, sticky="w")
        self.confirm_label.grid(row=9, column=0, sticky="w", pady=(12, 2))
        self.confirm_entry.grid(row=10, column=0)
        self.confirm_err.grid(row=11, column=0, sticky="w")
        self.remember_check.grid_remove()
        
        self.submit_btn.configure(text="Create Account")
        self.bottom_label.configure(text="Already have an account? Sign in above.")
        self._clear_errors()

    def _submit(self):
        self._clear_errors()
        email = self.email_entry.get().strip()
        password = self.pass_entry.get()

        if self._mode == "login":
            if not email:
                self._show_field_error(self.email_entry, self.email_err, "Email is required.")
                return
            if not password:
                self._show_field_error(self.pass_entry, self.pass_err, "Password is required.")
                return
            self._do_login(email, password)
        else:
            username = self.username_entry.get().strip()
            confirm = self.confirm_entry.get()
            ok = True
            if not username:
                self._show_field_error(self.username_entry, self.username_err, "Username is required.")
                ok = False
            if not email:
                self._show_field_error(self.email_entry, self.email_err, "Email is required.")
                ok = False
            if not password:
                self._show_field_error(self.pass_entry, self.pass_err, "Password is required.")
                ok = False
            elif confirm != password:
                self._show_field_error(self.confirm_entry, self.confirm_err, "Passwords do not match.")
                ok = False
            
            if ok:
                self._do_register(username, email, password)

    def _do_login(self, email, password):
        from auth.auth import login_user
        self.submit_btn.configure(text="Authenticating...", state="disabled")
        result = login_user(email, password, self.remember_var.get())
        if result["success"]:
            self.on_login_success(result["user"], result["token"])
        else:
            self.submit_btn.configure(text="Sign In", state="normal")
            self.global_err.configure(text=result["error"])

    def _do_register(self, username, email, password):
        from auth.auth import register_user, login_user
        self.submit_btn.configure(text="Preparing Profile...", state="disabled")
        result = register_user(username, email, password)
        if result["success"]:
            login_result = login_user(email, password, False)
            if login_result["success"]:
                self.on_login_success(login_result["user"], login_result["token"])
        else:
            self.submit_btn.configure(text="Create Account", state="normal")
            self.global_err.configure(text=result["error"])

    def _clear_errors(self):
        for lbl in [self.username_err, self.email_err, self.pass_err, self.confirm_err, self.global_err]:
            lbl.configure(text="")
        for entry in [self.username_entry, self.email_entry, self.pass_entry, self.confirm_entry]:
            entry.configure(border_color=COLORS["border"])

    def _show_field_error(self, entry, label, msg):
        entry.configure(border_color=COLORS["error"])
        label.configure(text=msg)

    def _make_err_label(self):
        return ctk.CTkLabel(self.form_frame, text="", font=ctk.CTkFont(size=11), text_color=COLORS["error"])