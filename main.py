"""STRCrosshair — entry point."""
import os
import sys
import threading
import tkinter as tk


def main():
    root = tk.Tk()
    root.withdraw()
    root.title("STRCrosshair")

    from config_manager import ConfigManager
    from crosshair_overlay import CrosshairOverlay
    from settings_window import SettingsWindow

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

    # System tray (background thread)
    try:
        from tray_manager import TrayManager
        t = TrayManager(root, cfg, overlay, show_settings, quit_app)
        _tray[0] = t
        threading.Thread(target=t.run, daemon=True).start()
    except Exception as e:
        print(f"Tray unavailable: {e}")

    # Global hotkey (requires `keyboard` package)
    try:
        import keyboard
        keyboard.add_hotkey(
            cfg.config.hotkey,
            lambda: root.after(0, overlay.toggle_visibility)
        )
    except Exception as e:
        print(f"Hotkey unavailable: {e}")

    if not cfg.config.start_minimized:
        root.after(400, show_settings)

    root.mainloop()


if __name__ == "__main__":
    main()
