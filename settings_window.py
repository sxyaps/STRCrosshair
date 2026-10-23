import tkinter as tk
from tkinter import ttk, colorchooser
from dataclasses import asdict

BG       = "#0d0d1a"
BG2      = "#13132a"
BG3      = "#1a1a2e"
FG       = "#e2e8f0"
FG2      = "#94a3b8"
PRIMARY  = "#7c3aed"
ACCENT   = "#00d4ff"
BORDER   = "#2d2d4e"

STYLES = ["cross", "dot", "circle", "crossdot", "tcross", "circlecross"]
STYLE_LABELS = {
    "cross": "Cross",
    "dot": "Dot",
    "circle": "Circle",
    "crossdot": "Cross + Dot",
    "tcross": "T-Cross",
    "circlecross": "Circle + Cross",
}


class SettingsWindow:
    def __init__(self, root, config_manager, overlay):
        self.root = root
        self.cm = config_manager
        self.overlay = overlay
        self._build()

    def _build(self):
        self.root.title("STRCrosshair")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # Title bar
        title = tk.Frame(self.root, bg=BG, pady=12)
        title.pack(fill="x", padx=20)
        tk.Label(title, text="STR", font=("Segoe UI", 18, "bold"),
                 bg=BG, fg=PRIMARY).pack(side="left")
        tk.Label(title, text="Crosshair", font=("Segoe UI", 18),
                 bg=BG, fg=FG).pack(side="left")

        # Preview canvas
        self._canvas = tk.Canvas(self.root, width=200, height=200,
                                  bg=BG3, highlightthickness=1,
                                  highlightbackground=BORDER)
        self._canvas.pack(pady=(0, 8))

        # Controls panel
        panel = tk.Frame(self.root, bg=BG, padx=20)
        panel.pack(fill="x")

        self._vars = {}
        cfg = self.cm.config

        # Style dropdown
        self._add_label(panel, "Style")
        sv = tk.StringVar(value=STYLE_LABELS.get(cfg.style, "Cross"))
        self._vars["style"] = sv
        cb = ttk.Combobox(panel, textvariable=sv,
                          values=list(STYLE_LABELS.values()),
                          state="readonly", width=22)
        cb.pack(fill="x", pady=(0, 8))
        sv.trace_add("write", lambda *_: self._on_change())

        # Color buttons
        self._add_label(panel, "Color")
        row = tk.Frame(panel, bg=BG)
        row.pack(fill="x", pady=(0, 8))
        self._color_btn = self._color_swatch(row, cfg.color, lambda: self._pick_color("color"))
        self._color_btn.pack(side="left", padx=(0, 8))
        tk.Label(row, text="Outline", bg=BG, fg=FG2,
                 font=("Segoe UI", 9)).pack(side="left", padx=(0, 4))
        self._outline_btn = self._color_swatch(row, cfg.outline_color,
                                                lambda: self._pick_color("outline_color"))
        self._outline_btn.pack(side="left")

        # Sliders
        sliders = [
            ("Arm Length", "size", 1, 40),
            ("Thickness", "thickness", 1, 10),
            ("Center Gap", "gap", 0, 20),
            ("Opacity", "opacity", 0.1, 1.0),
            ("Offset X", "offset_x", -200, 200),
            ("Offset Y", "offset_y", -200, 200),
        ]
        for label, key, lo, hi in sliders:
            self._add_slider(panel, label, key, lo, hi,
                             float if key == "opacity" else int)

        # Checkboxes
        checks = [
            ("Center Dot", "dot_enabled"),
            ("Outer Circle", "circle_enabled"),
            ("Outline", "outline_enabled"),
            ("Start Minimized", "start_minimized"),
        ]
        cframe = tk.Frame(panel, bg=BG)
        cframe.pack(fill="x", pady=(4, 0))
        for i, (label, key) in enumerate(checks):
            v = tk.BooleanVar(value=getattr(cfg, key))
            self._vars[key] = v
            cb2 = tk.Checkbutton(cframe, text=label, variable=v,
                                  bg=BG, fg=FG, selectcolor=BG2,
                                  activebackground=BG, activeforeground=FG,
                                  font=("Segoe UI", 9),
                                  command=self._on_change)
            cb2.grid(row=i // 2, column=i % 2, sticky="w", padx=(0, 12), pady=2)

        # Hotkey
        self._add_label(panel, "Hotkey")
        hv = tk.StringVar(value=cfg.hotkey)
        self._vars["hotkey"] = hv
        tk.Entry(panel, textvariable=hv, bg=BG2, fg=FG,
                 insertbackground=FG, relief="flat",
                 font=("Segoe UI", 9)).pack(fill="x", pady=(0, 8))
        hv.trace_add("write", lambda *_: self._on_change())

        # Save button
        tk.Button(panel, text="Save", bg=PRIMARY, fg="white",
                  relief="flat", font=("Segoe UI", 10, "bold"),
                  pady=8, cursor="hand2",
                  command=self._save).pack(fill="x", pady=(8, 16))

        self._update_preview()

    def _add_label(self, parent, text):
        tk.Label(parent, text=text, bg=BG, fg=FG2,
                 font=("Segoe UI", 9)).pack(anchor="w")

    def _color_swatch(self, parent, color, cmd):
        btn = tk.Button(parent, bg=color, width=3, relief="flat",
                        cursor="hand2", command=cmd)
        return btn

    def _add_slider(self, parent, label, key, lo, hi, typ):
        self._add_label(parent, label)
        val = getattr(self.cm.config, key)
        v = tk.DoubleVar(value=val)
        self._vars[key] = v
        res = 0.05 if typ == float else 1
        s = ttk.Scale(parent, from_=lo, to=hi, variable=v,
                      orient="horizontal",
                      command=lambda _: self._on_change())
        s.pack(fill="x", pady=(0, 8))

    def _pick_color(self, key):
        current = getattr(self.cm.config, key)
        _, hex_color = colorchooser.askcolor(color=current, parent=self.root)
        if hex_color:
            setattr(self.cm.config, key, hex_color)
            if key == "color":
                self._color_btn.configure(bg=hex_color)
            else:
                self._outline_btn.configure(bg=hex_color)
            self._on_change()

    def _on_change(self):
        cfg = self.cm.config
        label_to_key = {v: k for k, v in STYLE_LABELS.items()}
        cfg.style = label_to_key.get(self._vars["style"].get(), "cross")

        for key, var in self._vars.items():
            if key == "style":
                continue
            val = var.get()
            if key == "opacity":
                val = round(float(val), 2)
            elif key in ("offset_x", "offset_y"):
                val = int(float(val))
            elif key not in ("dot_enabled", "circle_enabled",
                             "outline_enabled", "start_minimized", "hotkey"):
                val = max(1, int(float(val)))
            setattr(cfg, key, val)

        self.overlay.refresh()
        self._update_preview()

    def _save(self):
        self._on_change()
        self.cm.save()

    def _update_preview(self):
        c = self._canvas
        c.delete("all")
        cfg = self.cm.config
        W, H = 200, 200
        cx, cy = W // 2, H // 2

        col = cfg.color
        oc  = cfg.outline_color if cfg.outline_enabled else None
        ow  = cfg.outline_thickness
        t   = cfg.thickness
        s   = cfg.size
        g   = cfg.gap
        sty = cfg.style

        def rect(x, y, w, h, color):
            c.create_rectangle(x, y, x + w, y + h, fill=color, outline="")

        def outline_rect(x, y, w, h):
            if oc and ow > 0:
                rect(x - ow, y - ow, w + ow * 2, h + ow * 2, oc)

        h2 = max(1, t // 2)

        if sty in ("cross", "crossdot", "circlecross", "tcross"):
            arms = [
                (cx - h2, cy + g, t, s),
                (cx - g - s, cy - h2, s, t),
                (cx + g, cy - h2, s, t),
            ]
            if sty != "tcross":
                arms.append((cx - h2, cy - g - s, t, s))
            for (x, y, w, hh) in arms:
                outline_rect(x, y, w, hh)
                rect(x, y, w, hh, col)

        if sty in ("circle", "circlecross") or cfg.circle_enabled:
            r = cfg.circle_radius
            if oc and ow > 0:
                c.create_oval(cx - r - ow, cy - r - ow,
                              cx + r + ow, cy + r + ow,
                              outline=oc, width=t + ow * 2)
            c.create_oval(cx - r, cy - r, cx + r, cy + r,
                          outline=col, width=t)

        if sty in ("dot", "crossdot") or cfg.dot_enabled:
            r = cfg.dot_size
            if oc and ow > 0:
                c.create_oval(cx - r - ow, cy - r - ow,
                              cx + r + ow, cy + r + ow,
                              fill=oc, outline="")
            c.create_oval(cx - r, cy - r, cx + r, cy + r,
                          fill=col, outline="")

    def show(self):
        self.root.deiconify()
        self.root.lift()

    def hide(self):
        self.root.withdraw()
