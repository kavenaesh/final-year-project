"""
ui/ai_advisor.py - Professional AI Advisor with Markdown, Elastic Animations & Typewriter
"""
import customtkinter as ctk
import tkinter as tk
import queue
import threading
import re
import math

COLORS = {
    "bg": "#0D0F14", "card": "#1A1D27", "accent": "#6C63FF",
    "accent_hover": "#7C73FF", "teal": "#00D4AA", "text": "#F0F0F5",
    "muted": "#7A7F9A", "error": "#FF6B6B", "sidebar": "#12151C", "border": "#2A2D3E",
    "user_bubble": "#3D3580", "ai_bubble": "#1A1D27", "code_bg": "#12151C"
}

class AnimatedBubble(ctk.CTkFrame):
    """A floating chat bubble that parses markdown with an elastic rise animation."""
    def __init__(self, master, role: str, text: str = "", width: int = 560):
        bg_col = COLORS["user_bubble"] if role == "user" else COLORS["ai_bubble"]
        super().__init__(master, fg_color=bg_col, corner_radius=18, 
                         border_width=1 if role == "ai" else 0, border_color=COLORS["border"])
        
        self.role = role
        self.full_width = width
        self.raw_text = text
        self.grid_columnconfigure(0, weight=1)
        
        self.textbox = ctk.CTkTextbox(
            self, width=self.full_width, height=10, 
            fg_color="transparent", text_color=COLORS["text"],
            font=ctk.CTkFont("Segoe UI", size=13),
            wrap="word", border_width=0, border_spacing=0
        )
        self.textbox.grid(row=0, column=0, sticky="nsew", padx=16, pady=12)
        
        # Markdown Configuration
        t = self.textbox._textbox
        t.tag_config("bold", font=("Segoe UI", 13, "bold"))
        t.tag_config("italic", font=("Segoe UI", 13, "italic"))
        t.tag_config("code", font=("Consolas", 12), background=COLORS["code_bg"], foreground=COLORS["teal"])
        t.tag_config("h1", font=("Segoe UI", 18, "bold"), foreground=COLORS["accent"])
        t.tag_config("bullet", font=("Segoe UI", 13), foreground=COLORS["teal"])

        self._set_text(text)
        
    def add_chunk(self, chunk: str):
        self.raw_text += chunk
        self._set_text(self.raw_text)
        
    def _set_text(self, text: str):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        
        lines = text.split("\n")
        in_code_block = False
        
        for i, line in enumerate(lines):
            if line.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                self.textbox.insert("end", line + "\n", "code")
                continue
            if line.startswith("# "):
                self.textbox.insert("end", line[2:] + "\n", "h1")
                continue
            if line.strip().startswith(("- ", "* ")):
                self.textbox.insert("end", " • ", "bullet")
                line = line.strip()[2:]
            
            # Inline Bold/Code parsing
            tokens = re.split(r'(\*\*.*?\*\*|`.*?`)', line)
            for token in tokens:
                if token.startswith("**") and token.endswith("**"):
                    self.textbox.insert("end", token[2:-2], "bold")
                elif token.startswith("`") and token.endswith("`"):
                    self.textbox.insert("end", token[1:-1], "code")
                else:
                    self.textbox.insert("end", token)
            
            if i < len(lines) - 1: self.textbox.insert("end", "\n")
                
        # Dynamic height adjustment
        lines_count = sum(1 + len(line) // 65 for line in text.split("\n"))
        self.textbox.configure(height=max(35, min(600, lines_count * 22)))
        self.textbox.configure(state="disabled")

class AIAdvisorPanel(ctk.CTkFrame):
    def __init__(self, master, user: dict):
        super().__init__(master, fg_color=COLORS["bg"])
        self.user = user
        self._history = []
        self._result_queue = queue.Queue()
        self._ai_thinking = False
        self._dot_count = 0
        self._current_ai_bubble = None
        self._anim_queue = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._load_history()
        self._build()
        self._add_welcome()
        self._poll_queue()
        
        # Trigger entrance animation
        self.after(100, self._run_panel_animation)

    def _load_history(self):
        try:
            from database.db import get_chat_history
            rows = get_chat_history(self.user["id"], limit=30)
            self._history = [{"role": r["role"], "content": r["content"]} for r in rows]
        except Exception: pass

    def _build(self):
        # --- Header with Status Animation ---
        self.hdr = ctk.CTkFrame(self, fg_color=COLORS["sidebar"], height=65, corner_radius=0)
        self.hdr.grid(row=0, column=0, sticky="ew")
        self.hdr.grid_propagate(False)
        self.hdr.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.hdr, text="🤖", font=ctk.CTkFont(size=28)).grid(row=0, column=0, padx=20)
        
        t_frame = ctk.CTkFrame(self.hdr, fg_color="transparent")
        t_frame.grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(t_frame, text="PathAI Advisor", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
        self.status_lbl = ctk.CTkLabel(t_frame, text="● Online", font=ctk.CTkFont(size=10), text_color=COLORS["teal"])
        self.status_lbl.pack(anchor="w")

        self.clear_btn = ctk.CTkButton(self.hdr, text="🗑 Clear", width=80, height=32, 
                                      fg_color="transparent", border_width=1, border_color=COLORS["border"],
                                      hover_color=COLORS["card"], command=self._clear_chat)
        self.clear_btn.grid(row=0, column=2, padx=20)

        # --- Chat Display ---
        self.chat_scroll = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg"], scrollbar_button_color=COLORS["border"])
        self.chat_scroll.grid(row=1, column=0, sticky="nsew")
        self.chat_scroll.grid_columnconfigure(0, weight=1)
        self._chat_row = 0

        # --- Input Bar Container ---
        self.input_container = ctk.CTkFrame(self, fg_color=COLORS["bg"], height=100)
        self.input_container.grid(row=2, column=0, sticky="ew")
        self.input_container.grid_propagate(False)
        self.input_container.grid_columnconfigure(0, weight=1)

        self.input_frame = ctk.CTkFrame(self.input_container, fg_color=COLORS["card"], corner_radius=15, 
                                       border_width=1, border_color=COLORS["border"])
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkTextbox(self.input_frame, height=45, fg_color="transparent", 
                                         text_color=COLORS["text"], wrap="word")
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=15, pady=5)
        self.input_entry.bind("<Return>", self._on_enter)
        
        # Glow focus interaction
        self.input_entry.bind("<FocusIn>", lambda e: self.input_frame.configure(border_color=COLORS["accent"]))
        self.input_entry.bind("<FocusOut>", lambda e: self.input_frame.configure(border_color=COLORS["border"]))

        self.send_btn = ctk.CTkButton(self.input_frame, text="➤", width=50, height=38, corner_radius=10,
                                     fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                                     command=self._send_message)
        self.send_btn.grid(row=0, column=1, padx=10)

        # Prepare for stagger animation
        self.hdr.grid_remove()
        self.chat_scroll.grid_remove()
        self.input_container.grid_remove()
        
        self._anim_queue.extend([self.hdr, self.chat_scroll, self.input_container])

    def _run_panel_animation(self):
        """Staggered reveal animation for main advisor panel elements."""
        if self._anim_queue:
            widget = self._anim_queue.pop(0)
            widget.grid()
            # Fade-in flash effect if possible
            if hasattr(widget, 'configure') and 'border_color' in widget.keys():
                orig = widget.cget('border_color')
                widget.configure(border_color=COLORS['accent'])
                self.after(150, lambda: widget.configure(border_color=orig))
            self.after(90, self._run_panel_animation)

    def _animate_bubble_entrance(self, widget, target_y=10):
        """Elastic physics: Bubble rises and settles."""
        widget.grid_configure(pady=(target_y + 20, 4))
        def step(curr=20):
            if curr > 0:
                widget.grid_configure(pady=(target_y + curr, 4))
                self.after(10, lambda: step(curr - 2))
        step()

    def _add_user_bubble(self, text: str):
        row = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        row.grid(row=self._chat_row, column=0, sticky="ew", padx=20, pady=5)
        row.grid_columnconfigure(0, weight=1)
        
        bubble = AnimatedBubble(row, role="user", text=text, width=420)
        bubble.grid(row=0, column=1, sticky="e")
        self._animate_bubble_entrance(row)
        
        self._chat_row += 1
        self._scroll_to_bottom()

    def _add_ai_bubble(self, text: str) -> AnimatedBubble:
        row = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        row.grid(row=self._chat_row, column=0, sticky="ew", padx=20, pady=5)
        row.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(row, text="🤖", font=("Arial", 22)).grid(row=0, column=0, padx=(0, 10), sticky="n")
        
        bubble = AnimatedBubble(row, role="ai", text=text, width=540)
        bubble.grid(row=0, column=1, sticky="w")
        self._animate_bubble_entrance(row)
        
        self._chat_row += 1
        self._scroll_to_bottom()
        return bubble

    def _poll_queue(self):
        try:
            while True:
                kind, data = self._result_queue.get_nowait()
                if kind == "chunk":
                    if self._current_ai_bubble:
                        if self._current_ai_bubble.raw_text.startswith("●"):
                            self._current_ai_bubble.raw_text = ""
                        self._current_ai_bubble.add_chunk(data)
                    self._scroll_to_bottom()
                elif kind == "done":
                    self._ai_thinking = False
                    self.send_btn.configure(state="normal", text="➤")
                    self.status_lbl.configure(text="● Online", text_color=COLORS["teal"])
                    if data:
                        self._history.append({"role": "assistant", "content": data})
                        try:
                            from database.db import save_chat_message
                            save_chat_message(self.user["id"], "assistant", data)
                        except: pass
                elif kind == "error":
                    self._ai_thinking = False
                    self.send_btn.configure(state="normal", text="➤")
                    self.status_lbl.configure(text="⚠ API Error", text_color=COLORS["error"])
                    if self._current_ai_bubble:
                        self._current_ai_bubble.add_chunk(f"\n\n⚠️ **Error:** {data}")
        except queue.Empty: pass
        self.after(50, self._poll_queue)

    def _send_message(self):
        text = self.input_entry.get("1.0", "end").strip()
        if not text or self._ai_thinking: return
        self.input_entry.delete("1.0", "end")

        self._add_user_bubble(text)
        self._history.append({"role": "user", "content": text})
        
        try:
            from database.db import save_chat_message
            save_chat_message(self.user["id"], "user", text)
        except: pass

        self._ai_thinking = True
        self.send_btn.configure(state="disabled", text="⚡")
        self.status_lbl.configure(text="● Thinking...", text_color=COLORS["accent"])
        self._current_ai_bubble = self._add_ai_bubble("● ● ●")
        self._animate_dots()

        from core.ai_engine import stream_response_to_queue
        threading.Thread(target=lambda: stream_response_to_queue(list(self._history), self._result_queue), daemon=True).start()

    def _animate_dots(self):
        if self._ai_thinking and self._current_ai_bubble and self._current_ai_bubble.raw_text.startswith("●"):
            dots = "● " * (self._dot_count % 3 + 1)
            self._current_ai_bubble.raw_text = dots
            self._current_ai_bubble._set_text(dots)
            self._dot_count += 1
            self.after(400, self._animate_dots)

    def _add_welcome(self):
        if not self._history:
            self._add_ai_bubble("# Welcome to PathAI!\nI'm your career guidance co-pilot. How can I help you today?")
        else:
            for msg in self._history[-10:]:
                if msg["role"] == "user": self._add_user_bubble(msg["content"])
                else: self._add_ai_bubble(msg["content"])

    def _clear_chat(self):
        for w in self.chat_scroll.winfo_children(): w.destroy()
        self._chat_row = 0
        self._history.clear()
        try:
            from database.db import clear_chat_history
            clear_chat_history(self.user["id"])
        except: pass
        self._add_welcome()

    def _on_enter(self, e):
        if not e.state & 0x1:
            self._send_message()
            return "break"

    def _scroll_to_bottom(self):
        self.after(50, lambda: self.chat_scroll._parent_canvas.yview_moveto(1.0))