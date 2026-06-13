"""
CrosshairOverlay — thin proxy that manages crosshair_engine.py as a subprocess.

The engine runs in its own process so pygame (SDL2) has the main thread to itself,
while tkinter's settings window keeps the main thread in this process.
IPC is newline-delimited JSON over stdin.
"""
import sys
import os
import json
import subprocess
from dataclasses import asdict


class CrosshairOverlay:
    def __init__(self, root, config_manager):
        """root is accepted for API compatibility; not used."""
        self.cm = config_manager
        self._proc = None
        self._visible = True
        self._start()

    # ── Subprocess management ─────────────────────────────────────────────────

    def _engine_path(self) -> str:
        if getattr(sys, "frozen", False):
            # PyInstaller bundle: engine script is extracted alongside the exe
            return os.path.join(sys._MEIPASS, "crosshair_engine.py")
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "crosshair_engine.py")

    def _start(self):
        path = self._engine_path()
        self._proc = subprocess.Popen(
            [sys.executable, path],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        self.refresh()  # push initial config

    def _send(self, msg: dict):
        try:
            if self._proc and self._proc.poll() is None:
                self._proc.stdin.write(json.dumps(msg) + "\n")
                self._proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass

    # ── Public API (called by settings_window and tray_manager) ──────────────

    def toggle_visibility(self):
        self._visible = not self._visible
        self._send({"action": "toggle"})

    def refresh(self):
        """Push current config to the overlay engine."""
        self._send({"action": "config", "data": asdict(self.cm.config)})

    def stop(self):
        self._send({"action": "quit"})
        if self._proc:
            try:
                self._proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._proc.terminate()
