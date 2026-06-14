"""
STRCrosshair — entry point.

When frozen with PyInstaller the single .exe serves two roles:
  - Normal launch  → settings UI + tray (tkinter, main process)
  - --engine flag  → crosshair overlay (pygame, spawned as subprocess)
"""
import os
import sys


def _run_settings():
    import threading
    import tkinter as tk
    from config_manager import ConfigManager
    from crosshair_overlay import CrosshairOverlay
    from settings_window import SettingsWindow

    root = tk.Tk()
    root.withdraw()
    root.title("STRCrosshair")

    cfg     = ConfigManager()
    overlay = CrosshairOverlay(root, cfg)

    _settings = [None]

    def show_settings():
        if _settings[0] is None or not _settings[0].window.winfo_exists():
            _settings[0] = SettingsWindow(root, cfg, overlay)
        else:
            _settings[0].window.lift()
            _settings[0].window.focus_force()

    _tray = [None]

    def quit_app():
        overlay.stop()
        if _tray[0]:
            _tray[0].stop()
        root.after(0, lambda: os._exit(0))

    try:
        from tray_manager import TrayManager
        t = TrayManager(root, cfg, overlay, show_settings, quit_app)
        _tray[0] = t
        threading.Thread(target=t.run, daemon=True).start()
    except Exception as e:
        print(f"Tray unavailable: {e}")

    try:
        import keyboard
        keyboard.add_hotkey(
            cfg.config.hotkey,
            lambda: root.after(0, overlay.toggle_visibility),
        )
    except Exception as e:
        print(f"Hotkey unavailable: {e}")

    if not cfg.config.start_minimized:
        root.after(400, show_settings)

    root.mainloop()


if __name__ == "__main__":
    if "--engine" in sys.argv:
        # Subprocess role: run the pygame crosshair engine
        from crosshair_engine import main as run_engine
        run_engine()
    else:
        _run_settings()
