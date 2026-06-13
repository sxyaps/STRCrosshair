"""Settings window — dark gaming theme with live preview."""
import tkinter as tk
from tkinter import colorchooser

# ── Palette ──────────────────────────────────────────────────────────────────
BG      = "#0d0d1a"
SURFACE = "#1a1a2e"
CARD    = "#16213e"
PRIMARY = "#7c3aed"
PHOVER  = "#9d5cf0"
ACCENT  = "#00d4ff"
TEXT    = "#e2e8f0"
DIM     = "#94a3b8"
BORDER  = "#2d2d4e"
GREEN   = "#22c55e"

STYLES = [
    ("＋  Cross",       "cross"),
    ("•   Dot",         "dot"),
    ("○   Circle",      "circle"),
    ("⊕  Cross+Dot",   "crossdot"),
    ("T   T-Cross",     "tcross"),
    ("⊙  Cir+Cross",   "circlecross"),
]


def _lbl(parent, text, size=9, color=TEXT, bold=False):
    return tk.Label(
        parent, text=text, bg=parent["bg"],
        fg=color, font=("Segoe UI", size, "bold" if bold else "normal")
    )


class SettingsWindow:
    def __init__(self, root, config_manager, overlay):
        self.root = root
        self.cm = config_manager
        self.overlay = overlay
        self._style_btns = {}
        self._build_vars()
        self._build_window()
        self._build_ui()
        self._load()

    # ── Variables ─────────────────────────────────────────────────────────────

    def _build_vars(self):
        self.v_style   = tk.StringVar()
        self.v_color   = tk.StringVar()
        self.v_outline = tk.BooleanVar()
        self.v_ocol    = tk.StringVar()
        self.v_othick  = tk.IntVar()
        self.v_size    = tk.IntVar()
        self.v_thick   = tk.IntVar()
        self.v_gap     = tk.IntVar()
        self.v_opacity = tk.DoubleVar()
        self.v_dot     = tk.BooleanVar()
        self.v_dotsize = tk.IntVar()
        self.v_circ    = tk.BooleanVar()
        self.v_crad    = tk.IntVar()
        self.v_ox      = tk.IntVar()
        self.v_oy      = tk.IntVar()
        self.v_hotkey  = tk.StringVar()
        self.v_minst   = tk.BooleanVar()

    # ── Window shell ──────────────────────────────────────────────────────────

    def _build_window(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("STRCrosshair — Settings")
        self.window.configure(bg=BG)
        self.window.resizable(False, False)
        W, H = 620, 740
        sx = (self.window.winfo_screenwidth()  - W) // 2
        sy = (self.window.winfo_screenheight() - H) // 2
        self.window.geometry(f"{W}x{H}+{sx}+{sy}")
        self.window.lift()
        self.window.focus_force()

    # ── Full UI ───────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Scrollable canvas
        outer = tk.Frame(self.window, bg=BG)
        outer.pack(fill="both", expand=True)

        vbar = tk.Scrollbar(outer, orient="vertical")
        vbar.pack(side="right", fill="y")
        mc = tk.Canvas(outer, bg=BG, highlightthickness=0, yscrollcommand=vbar.set)
        mc.pack(side="left", fill="both", expand=True)
        vbar.config(command=mc.yview)

        self._sf = tk.Frame(mc, bg=BG)
        win_id = mc.create_window(0, 0, window=self._sf, anchor="nw", width=600)
        self._sf.bind("<Configure>", lambda e: mc.configure(scrollregion=mc.bbox("all")))
        mc.bind("<MouseWheel>", lambda e: mc.yview_scroll(int(-e.delta / 120), "units"))
        # Keep inner frame width matched
        mc.bind("<Configure>", lambda e: mc.itemconfig(win_id, width=e.width))

        p = self._sf  # shorthand

        # ── Header ────────────────────────────────────────────────────────────
        hdr = tk.Frame(p, bg=SURFACE, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="STR", bg=SURFACE, fg=PRIMARY, font=("Segoe UI", 22, "bold")).pack(side="left", padx=(20, 0))
        tk.Label(hdr, text="CROSSHAIR", bg=SURFACE, fg=TEXT, font=("Segoe UI", 22, "bold")).pack(side="left")
        sf = tk.Frame(hdr, bg=SURFACE)
        sf.pack(side="right", padx=20)
        tk.Label(sf, text="●", bg=SURFACE, fg=GREEN, font=("Segoe UI", 11)).pack(side="left")
        tk.Label(sf, text=" ACTIVE", bg=SURFACE, fg=DIM, font=("Segoe UI", 8)).pack(side="left")

        # ── Style picker ──────────────────────────────────────────────────────
        self._section(p, "CROSSHAIR STYLE")
        sg = tk.Frame(p, bg=BG)
        sg.pack(fill="x", padx=16, pady=(0, 8))
        for i, (lbl, key) in enumerate(STYLES):
            b = tk.Button(
                sg, text=lbl,
                bg=PRIMARY if self.v_style.get() == key else SURFACE,
                fg=TEXT, font=("Segoe UI", 9), relief="flat",
                padx=6, pady=7, cursor="hand2", width=12,
                command=lambda k=key: self._select_style(k)
            )
            b.grid(row=i // 3, column=i % 3, padx=4, pady=4, sticky="ew")
            self._style_btns[key] = b
        for c in range(3):
            sg.columnconfigure(c, weight=1)

        # ── Two-column: settings (left) + preview (right) ─────────────────────
        body = tk.Frame(p, bg=BG)
        body.pack(fill="x", padx=16, pady=(4, 0))

        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(body, bg=CARD, width=170)
        right.pack(side="right", fill="y", padx=(16, 0))
        right.pack_propagate(False)

        # ── Preview pane ──────────────────────────────────────────────────────
        _lbl(right, "PREVIEW", size=8, color=DIM, bold=True).pack(pady=(14, 4))
        self.prev = tk.Canvas(right, bg="#111122", width=148, height=148,
                               highlightthickness=1, highlightbackground=BORDER)
        self.prev.pack(padx=11)

        _lbl(right, "Hotkey", size=8, color=DIM).pack(pady=(16, 2))
        self._hotkey_disp = _lbl(right, self.v_hotkey.get() or "ctrl+shift+h", size=9, color=ACCENT)
        self._hotkey_disp.pack()

        tk.Button(right, text="▶  APPLY", bg=PRIMARY, fg=TEXT, font=("Segoe UI", 9, "bold"),
                  relief="flat", pady=7, cursor="hand2", command=self._apply
                  ).pack(pady=(20, 4), padx=11, fill="x")
        tk.Button(right, text="💾  SAVE", bg=CARD, fg=TEXT, font=("Segoe UI", 9),
                  relief="flat", pady=7, cursor="hand2",
                  highlightthickness=1, highlightbackground=PRIMARY,
                  command=self._save
                  ).pack(pady=4, padx=11, fill="x")
        tk.Button(right, text="👁  TOGGLE\nCROSSHAIR", bg=SURFACE, fg=DIM,
                  font=("Segoe UI", 8), relief="flat", pady=6, cursor="hand2",
                  command=self.overlay.toggle_visibility
                  ).pack(pady=(14, 4), padx=11, fill="x")
        tk.Button(right, text="↺  RESET\nDEFAULTS", bg=SURFACE, fg=DIM,
                  font=("Segoe UI", 8), relief="flat", pady=6, cursor="hand2",
                  command=self._reset_defaults
                  ).pack(pady=4, padx=11, fill="x")

        # ── Color ─────────────────────────────────────────────────────────────
        self._section(left, "COLOR")
        self._color_row(left, "Crosshair Color", self.v_color, self._pick_color)
        self._color_row(left, "Outline Color",   self.v_ocol,  self._pick_outline)
        self._toggle_row(left, "Outline Enabled", self.v_outline)
        self._slider(left, "Outline Thickness", 1, 4, self.v_othick)

        # ── Size ──────────────────────────────────────────────────────────────
        self._section(left, "SIZE & SHAPE")
        self._slider(left, "Arm Length",   1, 30, self.v_size)
        self._slider(left, "Thickness",    1, 8,  self.v_thick)
        self._slider(left, "Center Gap",   0, 20, self.v_gap)
        self._fslider(left, "Opacity",    0.05, 1.0, self.v_opacity)

        # ── Extras ────────────────────────────────────────────────────────────
        self._section(left, "EXTRAS")
        self._toggle_row(left, "Center Dot", self.v_dot)
        self._slider(left, "Dot Size", 1, 8, self.v_dotsize)
        self._toggle_row(left, "Outer Circle", self.v_circ)
        self._slider(left, "Circle Radius", 4, 60, self.v_crad)

        # ── Offset ────────────────────────────────────────────────────────────
        self._section(left, "POSITION OFFSET")
        self._slider(left, "Horizontal (X)", -200, 200, self.v_ox)
        self._slider(left, "Vertical (Y)",   -200, 200, self.v_oy)
        tk.Button(left, text="Reset to Screen Center",
                  bg=SURFACE, fg=DIM, font=("Segoe UI", 8), relief="flat",
                  padx=8, pady=3, cursor="hand2",
                  command=self._reset_pos).pack(anchor="w", padx=16, pady=(4, 0))

        # ── Hotkey ────────────────────────────────────────────────────────────
        self._section(left, "HOTKEY & STARTUP")
        hkr = tk.Frame(left, bg=BG)
        hkr.pack(fill="x", padx=16, pady=4)
        _lbl(hkr, "Toggle Hotkey:", color=DIM).pack(side="left")
        e = tk.Entry(hkr, textvariable=self.v_hotkey, bg=SURFACE, fg=ACCENT,
                     font=("Segoe UI", 9), relief="flat", width=20, insertbackground=ACCENT)
        e.pack(side="right", ipady=4)
        e.bind("<FocusOut>", lambda ev: self._hotkey_disp.config(text=self.v_hotkey.get()))

        self._toggle_row(left, "Start Minimized (no settings on launch)", self.v_minst)

        # ── Footer ────────────────────────────────────────────────────────────
        ft = tk.Frame(p, bg=SURFACE, pady=10)
        ft.pack(fill="x", pady=(16, 0))
        _lbl(ft, "STRCrosshair  •  Always-on-top click-through overlay", size=8, color=DIM).pack()
        _lbl(ft, "Works best with Borderless Windowed mode in-game", size=7, color=BORDER).pack()

    # ── Widget helpers ────────────────────────────────────────────────────────

    def _section(self, parent, title):
        f = tk.Frame(parent, bg=BG)
        f.pack(fill="x", padx=16, pady=(12, 0))
        _lbl(f, title, size=9, color=DIM, bold=True).pack(anchor="w")
        tk.Frame(f, bg=PRIMARY, height=2).pack(fill="x", pady=(2, 6))

    def _slider(self, parent, label, lo, hi, var):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", padx=16, pady=2)
        top = tk.Frame(row, bg=BG)
        top.pack(fill="x")
        _lbl(top, label, color=DIM, size=9).pack(side="left")
        vl = _lbl(top, str(var.get()), color=ACCENT, size=9)
        vl.pack(side="right")
        tk.Scale(row, variable=var, from_=lo, to=hi, orient="horizontal",
                 showvalue=False, bg=BG, fg=TEXT, troughcolor=SURFACE,
                 activebackground=PRIMARY, highlightthickness=0,
                 sliderlength=14, sliderrelief="flat",
                 command=lambda v: [vl.config(text=str(int(float(v)))), self._preview()]
                 ).pack(fill="x")

    def _fslider(self, parent, label, lo, hi, var):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", padx=16, pady=2)
        top = tk.Frame(row, bg=BG)
        top.pack(fill="x")
        _lbl(top, label, color=DIM, size=9).pack(side="left")
        vl = _lbl(top, f"{var.get():.2f}", color=ACCENT, size=9)
        vl.pack(side="right")
        tk.Scale(row, variable=var, from_=lo, to=hi, resolution=0.05,
                 orient="horizontal", showvalue=False, bg=BG, fg=TEXT,
                 troughcolor=SURFACE, activebackground=PRIMARY, highlightthickness=0,
                 sliderlength=14, sliderrelief="flat",
                 command=lambda v: [vl.config(text=f"{float(v):.2f}"), self._preview()]
                 ).pack(fill="x")

    def _toggle_row(self, parent, label, var):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", padx=16, pady=3)
        _lbl(row, label, color=DIM, size=9).pack(side="left")
        btn = tk.Button(row, text="", bg=BG, fg=TEXT, relief="flat",
                        font=("Segoe UI", 7, "bold"), padx=8, pady=1, cursor="hand2")

        def _refresh():
            btn.config(bg=PRIMARY if var.get() else SURFACE,
                       text="ON" if var.get() else "OFF")

        _refresh()

        def _toggle():
            var.set(not var.get())
            _refresh()
            self._preview()

        btn.config(command=_toggle)
        btn.pack(side="right")

    def _color_row(self, parent, label, var, pick_fn):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", padx=16, pady=3)
        _lbl(row, label, color=DIM, size=9).pack(side="left")
        sw = tk.Canvas(row, width=34, height=20, bg=BG, highlightthickness=0, cursor="hand2")
        sw.pack(side="right")
        sw.bind("<Button-1>", lambda e: pick_fn())
        tk.Button(row, text="Pick", bg=SURFACE, fg=TEXT, font=("Segoe UI", 8),
                  relief="flat", padx=6, pady=1, cursor="hand2", command=pick_fn
                  ).pack(side="right", padx=(0, 6))

        # Store swatch reference on the var for later updates
        var._swatch = sw
        self._refresh_swatch(var)

    def _refresh_swatch(self, var):
        sw = getattr(var, "_swatch", None)
        if sw:
            sw.delete("all")
            try:
                sw.create_rectangle(0, 0, 38, 24, fill=var.get(), outline=DIM)
            except Exception:
                pass

    # ── Color pickers ─────────────────────────────────────────────────────────

    def _pick_color(self):
        c = colorchooser.askcolor(color=self.v_color.get(), title="Crosshair Color", parent=self.window)
        if c[1]:
            self.v_color.set(c[1])
            self._refresh_swatch(self.v_color)
            self._preview()

    def _pick_outline(self):
        c = colorchooser.askcolor(color=self.v_ocol.get(), title="Outline Color", parent=self.window)
        if c[1]:
            self.v_ocol.set(c[1])
            self._refresh_swatch(self.v_ocol)
            self._preview()

    # ── Style buttons ─────────────────────────────────────────────────────────

    def _select_style(self, key):
        self.v_style.set(key)
        for k, b in self._style_btns.items():
            b.config(bg=PRIMARY if k == key else SURFACE)
        self._preview()

    # ── Live preview ──────────────────────────────────────────────────────────

    def _preview(self, *_):
        self._sync()
        self._draw_preview()

    def _draw_preview(self):
        self.prev.delete("all")
        cfg = self.cm.config
        cx = cy = 74
        c   = cfg.color
        oc  = cfg.outline_color if cfg.outline_enabled else None
        ow  = cfg.outline_thickness
        t   = cfg.thickness
        s   = cfg.size
        g   = cfg.gap
        sty = cfg.style

        if sty in ("cross", "crossdot", "circlecross", "tcross"):
            self._prev_cross(cx, cy, t, s, g, c, oc, ow, top=(sty != "tcross"))
        if sty in ("circle", "circlecross") or cfg.circle_enabled:
            self._prev_circle(cx, cy, cfg.circle_radius, t, c, oc, ow)
        if sty in ("dot", "crossdot") or cfg.dot_enabled:
            self._prev_dot(cx, cy, cfg.dot_size, c, oc, ow)

    def _pr(self, x1, y1, x2, y2, fill):
        self.prev.create_rectangle(x1, y1, x2, y2, fill=fill, outline="")

    def _prev_cross(self, cx, cy, t, s, g, col, oc, ow, top=True):
        h = t / 2
        arms = [
            (cx - h, cy + g,     cx + h, cy + g + s),
            (cx - g - s, cy - h, cx - g, cy + h),
            (cx + g, cy - h,     cx + g + s, cy + h),
        ]
        if top:
            arms.append((cx - h, cy - g - s, cx + h, cy - g))
        for x1, y1, x2, y2 in arms:
            if oc and ow > 0:
                self._pr(x1 - ow, y1 - ow, x2 + ow, y2 + ow, oc)
            self._pr(x1, y1, x2, y2, col)

    def _prev_circle(self, cx, cy, r, t, col, oc, ow):
        if oc and ow > 0:
            self.prev.create_oval(cx - r - ow, cy - r - ow, cx + r + ow, cy + r + ow,
                                   outline=oc, width=t + ow * 2, fill="")
        self.prev.create_oval(cx - r, cy - r, cx + r, cy + r, outline=col, width=t, fill="")

    def _prev_dot(self, cx, cy, r, col, oc, ow):
        if oc and ow > 0:
            self.prev.create_oval(cx - r - ow, cy - r - ow, cx + r + ow, cy + r + ow, fill=oc, outline="")
        self.prev.create_oval(cx - r, cy - r, cx + r, cy + r, fill=col, outline="")

    # ── Config sync ───────────────────────────────────────────────────────────

    def _sync(self):
        cfg = self.cm.config
        cfg.style            = self.v_style.get()
        cfg.color            = self.v_color.get()
        cfg.outline_enabled  = self.v_outline.get()
        cfg.outline_color    = self.v_ocol.get()
        cfg.outline_thickness= self.v_othick.get()
        cfg.size             = self.v_size.get()
        cfg.thickness        = self.v_thick.get()
        cfg.gap              = self.v_gap.get()
        cfg.opacity          = float(self.v_opacity.get())
        cfg.dot_enabled      = self.v_dot.get()
        cfg.dot_size         = self.v_dotsize.get()
        cfg.circle_enabled   = self.v_circ.get()
        cfg.circle_radius    = self.v_crad.get()
        cfg.offset_x         = self.v_ox.get()
        cfg.offset_y         = self.v_oy.get()
        cfg.hotkey           = self.v_hotkey.get()
        cfg.start_minimized  = self.v_minst.get()

    def _load(self):
        cfg = self.cm.config
        self.v_style.set(cfg.style)
        self.v_color.set(cfg.color)
        self.v_outline.set(cfg.outline_enabled)
        self.v_ocol.set(cfg.outline_color)
        self.v_othick.set(cfg.outline_thickness)
        self.v_size.set(cfg.size)
        self.v_thick.set(cfg.thickness)
        self.v_gap.set(cfg.gap)
        self.v_opacity.set(cfg.opacity)
        self.v_dot.set(cfg.dot_enabled)
        self.v_dotsize.set(cfg.dot_size)
        self.v_circ.set(cfg.circle_enabled)
        self.v_crad.set(cfg.circle_radius)
        self.v_ox.set(cfg.offset_x)
        self.v_oy.set(cfg.offset_y)
        self.v_hotkey.set(cfg.hotkey)
        self.v_minst.set(cfg.start_minimized)
        # Refresh style button highlights
        for k, b in self._style_btns.items():
            b.config(bg=PRIMARY if k == cfg.style else SURFACE)
        self._refresh_swatch(self.v_color)
        self._refresh_swatch(self.v_ocol)
        self._draw_preview()

    # ── Actions ───────────────────────────────────────────────────────────────

    def _apply(self):
        self._sync()
        self.overlay.refresh()

    def _save(self):
        self._sync()
        self.cm.save()
        self.overlay.refresh()

    def _reset_pos(self):
        self.v_ox.set(0)
        self.v_oy.set(0)
        self._preview()

    def _reset_defaults(self):
        from config_manager import CrosshairConfig
        self.cm.config = CrosshairConfig()
        self._load()
        self.overlay.refresh()
