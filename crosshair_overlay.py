"""
Transparent, click-through, always-on-top crosshair overlay.

Uses a near-black color (#010203) as the transparent key so that:
  - The canvas background becomes invisible (a "hole" in the window)
  - Crosshair lines and outlines are fully visible
  - Pure black (#000000) outlines remain opaque

Win32 flags applied:
  WS_EX_LAYERED    - required for transparentcolor and alpha
  WS_EX_TRANSPARENT - makes the window click-through
  WS_EX_TOOLWINDOW  - hides from Alt+Tab
  WS_EX_NOACTIVATE  - never steals keyboard focus
  HWND_TOPMOST      - stays above all non-topmost windows
"""
import ctypes
import tkinter as tk

_KEY = "#010203"  # transparent key color (imperceptibly dark)
_SWP = 0x0002 | 0x0001 | 0x0010  # SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE


class CrosshairOverlay:
    def __init__(self, root, config_manager):
        self.cm = config_manager
        self.root = root
        self.visible = True

        self.win = tk.Toplevel(root)
        self.win.title("STRCrosshair_OVL")
        self.win.overrideredirect(True)

        self.sw = self.win.winfo_screenwidth()
        self.sh = self.win.winfo_screenheight()
        self.win.geometry(f"{self.sw}x{self.sh}+0+0")

        self.win.configure(bg=_KEY)
        self.win.wm_attributes("-alpha", 1.0)
        self.win.wm_attributes("-transparentcolor", _KEY)
        self.win.wm_attributes("-topmost", True)
        self.win.wm_attributes("-toolwindow", True)

        self.canvas = tk.Canvas(self.win, bg=_KEY, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.win.after(200, self._setup_win32)
        self.draw()

    # ── Win32 ────────────────────────────────────────────────────────────────

    def _setup_win32(self):
        try:
            hwnd = self.win.winfo_id()
            GWL_EXSTYLE = -20
            FLAGS = 0x80000 | 0x20 | 0x80 | 0x8000000  # LAYERED|TRANSPARENT|TOOLWINDOW|NOACTIVATE
            cur = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, cur | FLAGS)
            self._topmost()
            self.win.after(4000, self._keep_topmost)
        except Exception as e:
            print(f"Win32 init failed: {e}")

    def _topmost(self):
        try:
            ctypes.windll.user32.SetWindowPos(
                self.win.winfo_id(), -1, 0, 0, 0, 0, _SWP  # HWND_TOPMOST = -1
            )
        except Exception:
            pass

    def _keep_topmost(self):
        """Re-enforce topmost every 4 s so games can't push us under."""
        if self.visible:
            self._topmost()
            self.win.after(4000, self._keep_topmost)

    # ── Drawing ──────────────────────────────────────────────────────────────

    def draw(self):
        self.canvas.delete("all")
        cfg = self.cm.config
        cx = self.sw // 2 + cfg.offset_x
        cy = self.sh // 2 + cfg.offset_y
        c   = cfg.color
        oc  = cfg.outline_color if cfg.outline_enabled else None
        ow  = cfg.outline_thickness
        t   = cfg.thickness
        s   = cfg.size
        g   = cfg.gap
        sty = cfg.style

        if sty in ("cross", "crossdot", "circlecross", "tcross"):
            self._cross(cx, cy, t, s, g, c, oc, ow, top=(sty != "tcross"))
        if sty in ("circle", "circlecross") or cfg.circle_enabled:
            self._circle(cx, cy, cfg.circle_radius, t, c, oc, ow)
        if sty in ("dot", "crossdot") or cfg.dot_enabled:
            self._dot(cx, cy, cfg.dot_size, c, oc, ow)

    def _r(self, x1, y1, x2, y2, fill):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="")

    def _cross(self, cx, cy, t, s, g, col, oc, ow, top=True):
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
                self._r(x1 - ow, y1 - ow, x2 + ow, y2 + ow, oc)
            self._r(x1, y1, x2, y2, col)

    def _circle(self, cx, cy, r, t, col, oc, ow):
        if oc and ow > 0:
            self.canvas.create_oval(
                cx - r - ow, cy - r - ow, cx + r + ow, cy + r + ow,
                outline=oc, width=t + ow * 2, fill=""
            )
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=col, width=t, fill="")

    def _dot(self, cx, cy, r, col, oc, ow):
        if oc and ow > 0:
            self.canvas.create_oval(cx - r - ow, cy - r - ow, cx + r + ow, cy + r + ow, fill=oc, outline="")
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=col, outline="")

    # ── Public API ───────────────────────────────────────────────────────────

    def toggle_visibility(self):
        self.visible = not self.visible
        if self.visible:
            self.win.deiconify()
            self._topmost()
        else:
            self.win.withdraw()

    def refresh(self):
        cfg = self.cm.config
        self.win.wm_attributes("-alpha", max(0.05, min(1.0, cfg.opacity)))
        self.draw()
