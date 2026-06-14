"""
CrosshairOverlay — subprocess proxy for crosshair_engine.py.

Development: spawns  python crosshair_engine.py
Frozen .exe: spawns  STRCrosshair.exe --engine   (same binary, second role)

IPC: newline-delimited JSON over stdin.
"""
import sys
import os
import json
import subprocess
from dataclasses import asdict


class CrosshairOverlay:
    def __init__(self, root, config_manager):
        """root accepted for API compatibility; not used."""
        self.cm = config_manager
        self._proc = None
        self._visible = True
        self._start()

    def _start(self):
        if getattr(sys, "frozen", False):
            # PyInstaller bundle: re-launch this .exe in engine mode
            cmd = [sys.executable, "--engine"]
        else:
            engine = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "crosshair_engine.py"
            )
            cmd = [sys.executable, engine]

        self._proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        self.refresh()

    def _send(self, msg: dict):
        try:
            if self._proc and self._proc.poll() is None:
                self._proc.stdin.write(json.dumps(msg) + "\n")
                self._proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass

    def toggle_visibility(self):
        self._visible = not self._visible
        self._send({"action": "toggle"})

    def refresh(self):
        self._send({"action": "config", "data": asdict(self.cm.config)})

    def stop(self):
        self._send({"action": "quit"})
        if self._proc:
            try:
                self._proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._proc.terminate()
