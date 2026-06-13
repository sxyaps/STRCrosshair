"""System tray icon — generated programmatically (no external icon file needed)."""
import pystray
from PIL import Image, ImageDraw, ImageFont


def _make_icon() -> Image.Image:
    SIZE = 64
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    cx = cy = SIZE // 2

    # Outer ring
    d.ellipse([4, 4, 60, 60], outline=(124, 58, 237), width=3)

    # Cross arms (cyan)
    col = (0, 212, 255)
    gap = 7
    arm = 18
    t = 2
    # top
    d.rectangle([cx - t, 8,      cx + t, cy - gap], fill=col)
    # bottom
    d.rectangle([cx - t, cy + gap, cx + t, SIZE - 8], fill=col)
    # left
    d.rectangle([8,      cy - t, cx - gap, cy + t], fill=col)
    # right
    d.rectangle([cx + gap, cy - t, SIZE - 8, cy + t], fill=col)
    # dot
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=col)

    return img


class TrayManager:
    def __init__(self, root, config_manager, overlay, show_settings, quit_app):
        self.root = root
        self._icon = None

        img = _make_icon()

        menu = pystray.Menu(
            pystray.MenuItem("⚙  Settings",  lambda icon, item: root.after(0, show_settings), default=True),
            pystray.MenuItem("👁  Toggle Crosshair", lambda icon, item: root.after(0, overlay.toggle_visibility)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("✕  Quit",      lambda icon, item: root.after(0, quit_app)),
        )

        self._icon = pystray.Icon("STRCrosshair", img, "STRCrosshair", menu)

    def run(self):
        if self._icon:
            self._icon.run()

    def stop(self):
        if self._icon:
            try:
                self._icon.stop()
            except Exception:
                pass
