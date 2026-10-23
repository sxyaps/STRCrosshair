import sys
import tkinter as tk
import keyboard

from config_manager import ConfigManager
from crosshair_overlay import CrosshairOverlay
from settings_window import SettingsWindow
from tray_manager import TrayManager


def _run_settings():
    cm = ConfigManager()

    root = tk.Tk()
    root.configure(bg="#0d0d1a")

    overlay = CrosshairOverlay(root, cm)
    sw = SettingsWindow(root, cm, overlay)

    def toggle():
        overlay.toggle_visibility()

    def show_settings():
        root.after(0, sw.show)

    def quit_app():
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        overlay.stop()
        tray.stop()
        root.after(0, root.destroy)

    tray = TrayManager(toggle, show_settings, quit_app)
    tray.start()

    try:
        keyboard.add_hotkey(cm.config.hotkey, toggle)
    except Exception:
        pass

    if cm.config.start_minimized:
        root.withdraw()
    else:
        root.protocol("WM_DELETE_WINDOW", sw.hide)

    root.mainloop()
    overlay.stop()


if __name__ == "__main__":
    if "--engine" in sys.argv:
        from crosshair_engine import main as run_engine
        run_engine()
    else:
        _run_settings()
