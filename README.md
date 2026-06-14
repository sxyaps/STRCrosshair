# STRCrosshair

Custom always-on-top crosshair overlay for Windows 10 / 11.  
Works with DirectX 9, 10, 11, 12, OpenGL, and Vulkan — fullscreen included.

## Download

**[⬇ Download STRCrosshair.exe](../../actions) → click the latest build → download `STRCrosshair-Windows-x64`**

No installation required. No Python needed. Just download and run.

> **Windows SmartScreen:** If Windows shows a blue "Unknown publisher" warning,  
> click **More info → Run anyway**. This happens because the exe isn't code-signed.  
> The app is open source — you can inspect every line of code in this repo.

---

## How it works

The overlay engine runs as a child process using **pygame (SDL2)** for GPU rendering.  
Three Win32 techniques stack together so the crosshair appears above your game:

| Technique | Effect |
|-----------|--------|
| `WS_EX_LAYERED` + color-key | Background pixels become invisible holes |
| `WS_EX_TRANSPARENT` | Fully click-through — zero input lag |
| **`DwmExtendFrameIntoClientArea(-1,-1,-1,-1)`** | Forces DWM to GPU-composite this window **above the game's DXGI swap chain** — same method used by HudSight |
| `HWND_TOPMOST` re-enforced every 3 s | Survives game launcher / anti-cheat window grabs |

No DLL injection. Anti-cheat safe.

## Fullscreen compatibility

| Game mode | API | Works? |
|-----------|-----|--------|
| Borderless Windowed | any | ✅ |
| Exclusive Fullscreen | DX12 | ✅ |
| Exclusive Fullscreen | DX11 | ✅ |
| Exclusive Fullscreen | DX10 | ✅ |
| Exclusive Fullscreen | DX9 (Win10+) | ✅ |
| Exclusive Fullscreen | OpenGL | ✅ |
| Exclusive Fullscreen | Vulkan | ✅ |

If a game still covers the crosshair, switch it to **Borderless Windowed** in display settings — this is guaranteed to work and gives faster Alt-Tab anyway.

## Features

| | |
|---|---|
| **6 crosshair styles** | Cross, Dot, Circle, Cross+Dot, T-Cross, Circle+Cross |
| **Color picker** | Primary color + outline color |
| **Live preview** | Changes appear instantly in the settings panel |
| **System tray** | Right-click → Toggle / Settings / Quit |
| **Global hotkey** | `Ctrl+Shift+H` toggles the crosshair on/off |
| **Opacity control** | Full transparency slider |
| **Position offset** | Move off true center if needed |
| **Config saved** | `~/.strcrosshair/config.json` — persists across launches |
| **High-DPI aware** | Correct position on 4K displays |

## Settings

Open from the system tray icon or on launch.

| Setting | Description |
|---------|-------------|
| Style | Cross / Dot / Circle / Cross+Dot / T-Cross / Circle+Cross |
| Color | Primary crosshair color |
| Outline | Border for contrast on any background |
| Arm Length | How long each arm extends from the center gap |
| Thickness | Line width in pixels |
| Center Gap | Empty space around the exact center point |
| Opacity | Overall transparency |
| Center Dot | Small filled circle at center |
| Outer Circle | Outer ring |
| Offset X / Y | Move crosshair off true screen center |
| Hotkey | Global keyboard shortcut to toggle |
| Start Minimized | Don't open settings on launch |

## Build from source

```bat
pip install -r requirements.txt
python main.py
```

To build your own `.exe`:
```bat
pip install -r requirements.txt
pip install pyinstaller
python create_icon.py
pyinstaller --onefile --windowed --name STRCrosshair --icon assets/icon.ico --hidden-import pygame --hidden-import pystray._win32 main.py
```

## Architecture

```
STRCrosshair.exe
├── Normal launch  →  tkinter settings window + system tray
└── --engine flag  →  pygame SDL2 overlay (spawned as subprocess)
        │  Win32: WS_EX_LAYERED | WS_EX_TRANSPARENT | HWND_TOPMOST
        └─ DwmExtendFrameIntoClientArea → GPU overlay above game frames
   IPC: newline-delimited JSON over stdin
```
