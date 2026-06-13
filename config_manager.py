"""Persistent configuration for STRCrosshair."""
import json
import os
from dataclasses import dataclass, asdict


@dataclass
class CrosshairConfig:
    style: str = "cross"          # cross | dot | circle | crossdot | tcross | circlecross
    color: str = "#00ff41"        # primary color
    outline_enabled: bool = True
    outline_color: str = "#000000"
    outline_thickness: int = 1
    size: int = 8                 # arm half-length (px)
    thickness: int = 2
    gap: int = 3                  # center gap
    opacity: float = 1.0
    dot_enabled: bool = False
    dot_size: int = 2
    circle_enabled: bool = False
    circle_radius: int = 18
    offset_x: int = 0
    offset_y: int = 0
    hotkey: str = "ctrl+shift+h"
    start_minimized: bool = False


class ConfigManager:
    def __init__(self):
        self.dir = os.path.join(os.path.expanduser("~"), ".strcrosshair")
        self.path = os.path.join(self.dir, "config.json")
        os.makedirs(self.dir, exist_ok=True)
        self.config = CrosshairConfig()
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    data = json.load(f)
                for k, v in data.items():
                    if hasattr(self.config, k):
                        setattr(self.config, k, v)
            except Exception:
                pass

    def save(self):
        try:
            with open(self.path, "w") as f:
                json.dump(asdict(self.config), f, indent=2)
        except Exception as e:
            print(f"Save failed: {e}")
