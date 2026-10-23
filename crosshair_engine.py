"""
STRCrosshair overlay engine — runs as a standalone subprocess.

Reads newline-delimited JSON commands from stdin:
  {"action": "config", "data": {...}}   update crosshair settings
  {"action": "toggle"}                  show / hide
  {"action": "quit"}                    clean exit

Fullscreen approach (Windows 10 / 11):
  WS_EX_LAYERED + WS_EX_TRANSPARENT + WS_EX_TOOLWINDOW + WS_EX_NOACTIVATE
  SetLayeredWindowAttributes(LWA_COLORKEY) — color-key transparency
  DwmExtendFrameIntoClientArea(-1,-1,-1,-1) — GPU-composite above game swap chain
  SetWindowPos(HWND_TOPMOST) re-enforced every 3 s
"""
import sys
import os
import json
import ctypes
import threading
import collections


_KR, _KG, _KB = 1, 2, 3
KEY = (_KR, _KG, _KB)
KEY_COLORREF = (_KB << 16) | (_KG << 8) | _KR

GWL_EXSTYLE   = -20
WS_EX_FLAGS   = 0x80000 | 0x20 | 0x80 | 0x8000000
LWA_COLORKEY  = 0x01
HWND_TOPMOST  = -1
SWP_FLAGS     = 0x0002 | 0x0001 | 0x0010


class MARGINS(ctypes.Structure):
    _fields_ = [("l", ctypes.c_int), ("r", ctypes.c_int),
                ("t", ctypes.c_int), ("b", ctypes.c_int)]


def _rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _cross(surf, cx, cy, t, s, g, col, oc, ow, top):
    import pygame
    h = max(1, t // 2)
    arms = [
        pygame.Rect(cx - h, cy + g,     t, s),
        pygame.Rect(cx - g - s, cy - h, s, t),
        pygame.Rect(cx + g, cy - h,     s, t),
    ]
    if top:
        arms.append(pygame.Rect(cx - h, cy - g - s, t, s))
    for r in arms:
        if oc and ow > 0:
            pygame.draw.rect(surf, oc, r.inflate(ow * 2, ow * 2))
        pygame.draw.rect(surf, col, r)


def _draw(surf, cfg: dict, cx: int, cy: int):
    import pygame
    col = _rgb(cfg.get("color", "#00ff41"))
    oe  = cfg.get("outline_enabled", True)
    oc  = _rgb(cfg.get("outline_color", "#000000")) if oe else None
    ow  = cfg.get("outline_thickness", 1)
    t   = cfg.get("thickness", 2)
    s   = cfg.get("size", 8)
    g   = cfg.get("gap", 3)
    sty = cfg.get("style", "cross")

    if sty in ("cross", "crossdot", "circlecross", "tcross"):
        _cross(surf, cx, cy, t, s, g, col, oc, ow, top=(sty != "tcross"))

    if sty in ("circle", "circlecross") or cfg.get("circle_enabled"):
        r = cfg.get("circle_radius", 18)
        if oc and ow > 0:
            pygame.draw.circle(surf, oc, (cx, cy), r + ow, t + ow * 2)
        pygame.draw.circle(surf, col, (cx, cy), r, t)

    if sty in ("dot", "crossdot") or cfg.get("dot_enabled"):
        r = cfg.get("dot_size", 2)
        if oc and ow > 0:
            pygame.draw.circle(surf, oc, (cx, cy), r + ow)
        pygame.draw.circle(surf, col, (cx, cy), r)


def main():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

    cmds: collections.deque = collections.deque()

    def _read_stdin():
        for raw in sys.stdin:
            raw = raw.strip()
            if raw:
                try:
                    cmds.append(json.loads(raw))
                except Exception:
                    pass

    threading.Thread(target=_read_stdin, daemon=True).start()

    import pygame

    pygame.init()

    u32 = ctypes.windll.user32
    dwm = ctypes.windll.dwmapi

    W = u32.GetSystemMetrics(0)
    H = u32.GetSystemMetrics(1)

    os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
    screen = pygame.display.set_mode((W, H), pygame.NOFRAME)
    pygame.display.set_caption("STRCrosshairOVL")

    hwnd = pygame.display.get_wm_info()["window"]

    old = u32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    u32.SetWindowLongW(hwnd, GWL_EXSTYLE, old | WS_EX_FLAGS)

    u32.SetLayeredWindowAttributes(hwnd, KEY_COLORREF, 0, LWA_COLORKEY)

    margins = MARGINS(-1, -1, -1, -1)
    dwm.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))

    u32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_FLAGS)

    cfg     = {}
    visible = True
    top_ms  = 0
    clock   = pygame.time.Clock()

    while True:
        dt = clock.tick(60)
        top_ms += dt

        while cmds:
            msg = cmds.popleft()
            act = msg.get("action")
            if act == "quit":
                pygame.quit()
                return
            elif act == "toggle":
                visible = not visible
            elif act == "config":
                cfg.update(msg.get("data", {}))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return

        if top_ms >= 3000:
            u32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_FLAGS)
            top_ms = 0

        screen.fill(KEY)
        if visible and cfg:
            ox = cfg.get("offset_x", 0)
            oy = cfg.get("offset_y", 0)
            _draw(screen, cfg, W // 2 + ox, H // 2 + oy)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
