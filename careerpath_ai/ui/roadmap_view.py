"""
ui/roadmap_view.py - Canvas roadmap flowchart with proper alignment, arrows, and detail panel
"""
import customtkinter as ctk
import tkinter as tk
import webbrowser

COLORS = {
    "bg": "#0D0F14", "card": "#1A1D27", "accent": "#6C63FF",
    "accent_hover": "#7C73FF", "teal": "#00D4AA", "text": "#F0F0F5",
    "muted": "#7A7F9A", "error": "#FF6B6B", "sidebar": "#12151C",
    "border": "#2A2D3E", "optional_node": "#252838", "done_node": "#007A60",
    "phase_text": "#FFFFFF", "connector": "#3A3D52", "nav_active_bg": "#1E2035",
}

NODE_W      = 280
NODE_H      = 54
NODE_R      = 10
PHASE_W     = 340
PHASE_H     = 40
V_NODE_GAP  = 24
V_PHASE_GAP = 56
CANVAS_PAD  = 60
ARROW_SIZE  = 8


class RoadmapViewPanel(ctk.CTkFrame):
    def __init__(self, master, roadmap_key: str, user: dict, on_back):
        super().__init__(master, fg_color=COLORS["bg"])
        self.roadmap_key = roadmap_key
        self.user = user
        self.on_back = on_back
        self._progress = {}
        self._nodes = []
        self._anim_idx = 0
        self._detail_visible = False
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._load_data()
        self._build_ui()
        self.after(120, self._draw_roadmap)

    def _load_data(self):
        from core.roadmap_data2 import ROADMAPS
        self.roadmap = ROADMAPS.get(self.roadmap_key, {})
        try:
            from database.db import get_roadmap_progress, save_roadmap
            save_roadmap(self.user["id"], self.roadmap_key)
            self._progress = get_roadmap_progress(self.user["id"], self.roadmap_key)
        except Exception:
            self._progress = {}

    def _build_ui(self):
        # Header
        hdr = ctk.CTkFrame(self, fg_color=COLORS["sidebar"], height=56, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_columnconfigure(2, weight=1)
        hdr.grid_propagate(False)

        ctk.CTkButton(hdr, text="←  Back", width=90, height=34,
                      fg_color="transparent", hover_color=COLORS["border"],
                      text_color=COLORS["muted"], font=ctk.CTkFont(size=12),
                      command=self.on_back).grid(row=0, column=0, padx=12, pady=11)

        ctk.CTkLabel(hdr,
                     text=f"{self.roadmap.get('icon','📋')}  {self.roadmap.get('title','')}",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=COLORS["text"]).grid(row=0, column=1, padx=8, sticky="w")

        btn_row = ctk.CTkFrame(hdr, fg_color="transparent")
        btn_row.grid(row=0, column=3, padx=12, pady=8, sticky="e")
        ctk.CTkButton(btn_row, text="💾  Save", width=90, height=34,
                      fg_color=COLORS["teal"], hover_color="#00E5BB",
                      corner_radius=8, font=ctk.CTkFont(size=12, weight="bold"),
                      command=self._save_roadmap).pack(side="left", padx=(0, 6))
        ctk.CTkButton(btn_row, text="📄  Export", width=90, height=34,
                      fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                      corner_radius=8, font=ctk.CTkFont(size=12, weight="bold"),
                      command=self._export_png).pack(side="left")

        # Main area: canvas | detail
        self._main = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        self._main.grid(row=1, column=0, sticky="nsew")
        self._main.grid_columnconfigure(0, weight=1)
        self._main.grid_rowconfigure(0, weight=1)

        cf = ctk.CTkFrame(self._main, fg_color=COLORS["bg"])
        cf.grid(row=0, column=0, sticky="nsew")
        cf.grid_columnconfigure(0, weight=1)
        cf.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(cf, bg=COLORS["bg"], highlightthickness=0)
        vs = ctk.CTkScrollbar(cf, orientation="vertical", command=self.canvas.yview,
                               button_color=COLORS["border"])
        hs = ctk.CTkScrollbar(cf, orientation="horizontal", command=self.canvas.xview,
                               button_color=COLORS["border"])
        self.canvas.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        vs.grid(row=0, column=1, sticky="ns")
        hs.grid(row=1, column=0, sticky="ew")

        self.canvas.bind("<MouseWheel>", self._on_scroll)
        self.canvas.bind("<Control-MouseWheel>", self._on_zoom)

        # Legend bar
        leg = ctk.CTkFrame(self, fg_color=COLORS["sidebar"], height=30, corner_radius=0)
        leg.grid(row=2, column=0, sticky="ew")
        for sym, color, lbl in [
            ("■", COLORS["accent"],         "Required"),
            ("■", COLORS["optional_node"],  "Optional"),
            ("■", COLORS["done_node"],       "Completed"),
        ]:
            f = ctk.CTkFrame(leg, fg_color="transparent")
            f.pack(side="left", padx=10)
            ctk.CTkLabel(f, text=sym, text_color=color, font=ctk.CTkFont(size=13)).pack(side="left")
            ctk.CTkLabel(f, text=f"  {lbl}", text_color=COLORS["muted"],
                         font=ctk.CTkFont(size=11)).pack(side="left")
        ctk.CTkLabel(leg, text="Click a node for details  •  Ctrl+Scroll to zoom",
                     text_color=COLORS["muted"], font=ctk.CTkFont(size=10)).pack(side="right", padx=14)

        # Side detail panel (initially hidden)
        self.detail_panel = ctk.CTkFrame(self._main, fg_color=COLORS["card"], width=360,
                                          corner_radius=0, border_width=1,
                                          border_color=COLORS["border"])

    def _draw_roadmap(self):
        self.canvas.delete("all")
        self._nodes.clear()
        self._anim_idx = 0

        phases = self.roadmap.get("phases", [])
        if not phases:
            self.canvas.create_text(200, 100, text="No roadmap data available.",
                                    fill=COLORS["muted"], font=("Segoe UI", 13))
            return

        cx      = CANVAS_PAD + PHASE_W // 2   # horizontal center for everything
        x_phase = CANVAS_PAD                   # left edge of phase banners
        x_node  = cx - NODE_W // 2             # left edge of nodes
        cy      = CANVAS_PAD
        prev_bottom = None                     # bottom-center y of the last item drawn

        for phase in phases:
            phase_color = phase.get("color", COLORS["accent"])
            topics = phase.get("topics", [])

            # Arrow from previous node into this phase banner
            if prev_bottom is not None:
                gap_mid = prev_bottom + (cy - prev_bottom) // 2
                self.canvas.create_line(cx, prev_bottom, cx, cy - ARROW_SIZE,
                                        fill=COLORS["connector"], width=2)
                self._arrowhead(cx, cy)

            # Phase banner
            self._rounded_rect(x_phase, cy, x_phase + PHASE_W, cy + PHASE_H,
                                r=8, fill=phase_color, outline="")
            self.canvas.create_text(cx, cy + PHASE_H // 2,
                                    text=phase.get("phase", ""),
                                    fill=COLORS["phase_text"],
                                    font=("Segoe UI", 11, "bold"),
                                    width=PHASE_W - 20)
            cy += PHASE_H

            for topic in topics:
                # Arrow from above into this node
                node_top = cy + V_NODE_GAP
                self.canvas.create_line(cx, cy, cx, node_top - ARROW_SIZE,
                                        fill=COLORS["connector"], width=2)
                self._arrowhead(cx, node_top)

                is_done = self._progress.get(topic["name"], False)
                is_req  = topic.get("required", True)
                fill    = COLORS["done_node"]    if is_done else (COLORS["accent"] if is_req else COLORS["optional_node"])
                outline = COLORS["teal"]          if is_done else (COLORS["accent_hover"] if is_req else COLORS["border"])

                ny = node_top
                nx = x_node

                node_id = self._rounded_rect(
                    nx, ny, nx + NODE_W, ny + NODE_H,
                    r=NODE_R, fill=fill, outline=outline, width=2,
                    tags=("node", topic["name"])
                )

                self.canvas.create_text(
                    cx, ny + NODE_H // 2,
                    text=topic["name"],
                    fill=COLORS["text"],
                    font=("Segoe UI", 10, "bold" if is_req else "normal"),
                    width=NODE_W - 24,
                    tags=("nodetxt", topic["name"])
                )

                if is_done:
                    self.canvas.create_text(nx + NODE_W - 16, ny + NODE_H // 2,
                                            text="✓", fill="#FFF",
                                            font=("Segoe UI", 12, "bold"),
                                            tags=("nodetick", topic["name"]))

                if not is_req:
                    self.canvas.create_text(nx + 40, ny + 10, text="optional",
                                            fill=COLORS["muted"],
                                            font=("Segoe UI", 8),
                                            tags=("nodepill", topic["name"]))

                t = topic
                self.canvas.tag_bind(topic["name"], "<Button-1>",
                                     lambda e, tp=t: self._show_detail(tp))
                self.canvas.tag_bind(topic["name"], "<Enter>",
                                     lambda e, nid=node_id: (
                                         self.canvas.itemconfig(nid, outline=COLORS["teal"], width=3),
                                         self.canvas.configure(cursor="hand2")))
                self.canvas.tag_bind(topic["name"], "<Leave>",
                                     lambda e, nid=node_id, oc=outline: (
                                         self.canvas.itemconfig(nid, outline=oc, width=2),
                                         self.canvas.configure(cursor="")))

                self._nodes.append((node_id, topic))
                cy = ny + NODE_H
                prev_bottom = cy

            cy += V_PHASE_GAP

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._animate_nodes()

    # ── Canvas helpers ─────────────────────────────────────────────────────────
    def _rounded_rect(self, x1, y1, x2, y2, r=8, **kw):
        pts = [
            x1+r, y1,   x2-r, y1,
            x2,   y1,   x2,   y1+r,
            x2,   y2-r, x2,   y2,
            x2-r, y2,   x1+r, y2,
            x1,   y2,   x1,   y2-r,
            x1,   y1+r, x1,   y1,
            x1+r, y1,
        ]
        tags    = kw.pop("tags", ())
        fill    = kw.pop("fill", COLORS["card"])
        outline = kw.pop("outline", "")
        width   = kw.pop("width", 1)
        return self.canvas.create_polygon(pts, smooth=True,
                                          fill=fill, outline=outline, width=width,
                                          tags=tags, **kw)

    def _arrowhead(self, x, tip_y):
        aw = ARROW_SIZE
        self.canvas.create_polygon(
            x,      tip_y,
            x - aw, tip_y - aw * 1.5,
            x + aw, tip_y - aw * 1.5,
            fill=COLORS["connector"], outline=""
        )

    # ── Animation ──────────────────────────────────────────────────────────────
    def _animate_nodes(self):
        if self._anim_idx < len(self._nodes):
            nid, _ = self._nodes[self._anim_idx]
            orig = self.canvas.itemcget(nid, "outline")
            self.canvas.itemconfig(nid, outline=COLORS["teal"], width=4)
            self.after(80, lambda: self.canvas.itemconfig(nid, outline=orig, width=2))
            self._anim_idx += 1
            self.after(100, self._animate_nodes)

    # ── Detail panel ────────────────────────────────────────────────────────────
    def _show_detail(self, topic: dict):
        for w in self.detail_panel.winfo_children():
            w.destroy()
        if not self._detail_visible:
            self.detail_panel.grid(row=0, column=1, sticky="nsew")
            self._detail_visible = True

        scroll = ctk.CTkScrollableFrame(self.detail_panel, fg_color=COLORS["card"])
        scroll.pack(fill="both", expand=True)
        scroll.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(scroll, text="✕", width=32, height=28,
                      fg_color="transparent", hover_color=COLORS["border"],
                      text_color=COLORS["muted"], font=ctk.CTkFont(size=13),
                      command=self._close_detail).grid(row=0, column=0, sticky="ne",
                                                       padx=12, pady=(10, 0))

        ctk.CTkLabel(scroll, text=topic["name"],
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=COLORS["accent"], wraplength=320, justify="left").grid(
            row=1, column=0, sticky="w", padx=16, pady=(4, 4))

        badge_row = ctk.CTkFrame(scroll, fg_color="transparent")
        badge_row.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 6))
        req_text  = "✅ Required" if topic.get("required", True) else "💡 Optional"
        req_color = COLORS["teal"] if topic.get("required", True) else COLORS["muted"]
        ctk.CTkLabel(badge_row, text=req_text, font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=req_color, fg_color=COLORS["sidebar"],
                     corner_radius=4).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(badge_row, text=f"⏱ {topic.get('time_estimate', 'N/A')}",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=COLORS["accent"], fg_color=COLORS["sidebar"],
                     corner_radius=4).pack(side="left")

        ctk.CTkLabel(scroll, text=topic.get("description", ""),
                     font=ctk.CTkFont(size=12), text_color=COLORS["text"],
                     wraplength=320, justify="left").grid(
            row=3, column=0, sticky="w", padx=16, pady=(4, 10))

        is_done  = self._progress.get(topic["name"], False)
        done_var = tk.BooleanVar(value=is_done)
        ctk.CTkCheckBox(scroll, text="Mark as Completed",
                        variable=done_var,
                        fg_color=COLORS["teal"], hover_color="#00E5BB",
                        checkmark_color="white", font=ctk.CTkFont(size=12),
                        command=lambda: self._toggle_progress(topic["name"], done_var)).grid(
            row=4, column=0, sticky="w", padx=16, pady=(0, 12))

        ctk.CTkFrame(scroll, height=1, fg_color=COLORS["border"]).grid(
            row=5, column=0, sticky="ew", padx=12, pady=(0, 8))

        resources = topic.get("resources", {})
        row_idx = 6
        type_icons = {"youtube": "▶ ", "website": "🌐 ", "udemy": "🎓 ",
                      "coursera": "🎓 ", "other": "📖 "}
        for section, sec_label in [("free", "🆓  Free Resources"), ("paid", "💳  Paid Resources")]:
            items = resources.get(section, [])
            if not items:
                continue
            ctk.CTkLabel(scroll, text=sec_label,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=COLORS["teal"] if section == "free" else COLORS["accent"]).grid(
                row=row_idx, column=0, sticky="w", padx=16, pady=(6, 4))
            row_idx += 1
            for res in items:
                pf = type_icons.get(res.get("type", ""), "🔗 ")
                ctk.CTkButton(
                    scroll, text=f"{pf}{res['name']}", height=34, anchor="w",
                    fg_color=COLORS["sidebar"], hover_color=COLORS["nav_active_bg"],
                    text_color=COLORS["text"], font=ctk.CTkFont(size=11),
                    corner_radius=6,
                    command=lambda url=res["url"]: webbrowser.open(url)
                ).grid(row=row_idx, column=0, sticky="ew", padx=16, pady=2)
                row_idx += 1

    def _close_detail(self):
        self.detail_panel.grid_remove()
        self._detail_visible = False

    def _toggle_progress(self, name: str, var: tk.BooleanVar):
        self._progress[name] = var.get()
        try:
            from database.db import update_roadmap_progress
            update_roadmap_progress(self.user["id"], self.roadmap_key, self._progress)
        except Exception:
            pass
        for nid, topic in self._nodes:
            if topic["name"] == name:
                done = var.get()
                fill = COLORS["done_node"] if done else (
                    COLORS["accent"] if topic.get("required", True) else COLORS["optional_node"])
                self.canvas.itemconfig(nid, fill=fill)
                break

    def _save_roadmap(self):
        try:
            from database.db import save_roadmap
            save_roadmap(self.user["id"], self.roadmap_key)
        except Exception:
            pass
        lbl = ctk.CTkLabel(self, text="✅  Roadmap saved!",
                           font=ctk.CTkFont(size=12), text_color=COLORS["teal"])
        lbl.place(relx=0.5, rely=0.96, anchor="center")
        self.after(2500, lbl.destroy)

    def _export_png(self):
        try:
            from PIL import ImageGrab
            import tkinter.filedialog as fd
            path = fd.asksaveasfilename(defaultextension=".png",
                                        filetypes=[("PNG Image", "*.png")],
                                        title="Export Roadmap as PNG")
            if path:
                x, y = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
                img = ImageGrab.grab(bbox=(x, y,
                                           x + self.canvas.winfo_width(),
                                           y + self.canvas.winfo_height()))
                img.save(path)
                lbl = ctk.CTkLabel(self, text="✅  Exported!",
                                   font=ctk.CTkFont(size=12), text_color=COLORS["teal"])
                lbl.place(relx=0.5, rely=0.96, anchor="center")
                self.after(3000, lbl.destroy)
        except Exception:
            pass

    def _on_scroll(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.canvas.scale("all", 0, 0, factor, factor)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
