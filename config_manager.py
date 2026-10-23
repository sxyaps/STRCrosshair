import json
import os
from dataclasses import dataclass, field, asdict


CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".strcrosshair", "config.json")


@dataclass
class CrosshairConfig:
    style: str = "cross"
    color: str = "#00ff41"
    outline_enabled: bool = True
    outline_color: str = "#000000"
    outline_thickness: int = 1
    thickness: int = 2
    size: int = 8
    gap: int = 3
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
        self.config = CrosshairConfig()
        self._load()

    def _load(self):
        try:
            with open(CONFIG_PATH) as f:
                data = json.load(f)
            for k, v in data.items():
                if hasattr(self.config, k):
                    setattr(self.config, k, v)
        except Exception:
            pass

    def save(self):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(asdict(self.config), f, indent=2)
