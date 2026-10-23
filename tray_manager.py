import threading
import pystray
from PIL import Image, ImageDraw


def _make_icon():
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = cy = size // 2
    t = 3
    arm = 20
    gap = 5
    col = (124, 58, 237, 255)
    # cross
    d.rectangle([cx - t // 2, cy + gap, cx + t // 2, cy + gap + arm], fill=col)
    d.rectangle([cx - t // 2, cy - gap - arm, cx + t // 2, cy - gap], fill=col)
    d.rectangle([cx + gap, cy - t // 2, cx + gap + arm, cy + t // 2], fill=col)
    d.rectangle([cx - gap - arm, cy - t // 2, cx - gap, cy + t // 2], fill=col)
    return img


class TrayManager:
    def __init__(self, on_toggle, on_settings, on_quit):
        self._on_toggle   = on_toggle
        self._on_settings = on_settings
        self._on_quit     = on_quit
        self._icon = None

    def start(self):
        menu = pystray.Menu(
            pystray.MenuItem("Toggle Crosshair", lambda: self._on_toggle()),
            pystray.MenuItem("Settings",         lambda: self._on_settings()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit",             lambda: self._on_quit()),
        )
        self._icon = pystray.Icon("STRCrosshair", _make_icon(),
                                   "STRCrosshair", menu)
        threading.Thread(target=self._icon.run, daemon=True).start()

    def stop(self):
        if self._icon:
            self._icon.stop()
