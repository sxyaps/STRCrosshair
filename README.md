# STRCrosshair

Custom always-on-top crosshair overlay for Windows 10 / 11.  
Works with DirectX 9, 10, 11, 12, OpenGL, and Vulkan games — fullscreen included.

## How it works

The overlay engine (`crosshair_engine.py`) runs as a separate process using **pygame (SDL2)** for rendering. Three Win32 techniques are stacked to guarantee the crosshair appears above games:

| Technique | Effect |
|-----------|--------|
| `WS_EX_LAYERED` + `SetLayeredWindowAttributes(LWA_COLORKEY)` | Background color becomes a transparent "hole" — only the crosshair pixels are visible |
| `WS_EX_TRANSPARENT` | Fully click-through — all mouse events fall through to the game |
| `DwmExtendFrameIntoClientArea(-1,-1,-1,-1)` | Forces DWM GPU-composition of this window, rendering it **above the game's DXGI swap chain** — the same technique used by HudSight and similar tools |
| `SetWindowPos(HWND_TOPMOST)` re-enforced every 3 s | Survives game launcher / anti-cheat window grabs |

Windows 10 1703+ (Creators Update) and Windows 11 route even "exclusive fullscreen" games through DWM's compositor, so `DwmExtendFrameIntoClientArea` is enough to overlay them without injecting DLLs into the game process.

## Quickstart

```bat
pip install -r requirements.txt
python main.py
```

The settings window opens automatically. Your crosshair appears instantly over the desktop and any running game.

## Build standalone .exe

```bat
build.bat
```

Produces `dist\STRCrosshair\STRCrosshair.exe` — copy the entire `dist\STRCrosshair\` folder to any Windows 10/11 machine, no Python needed.

## Fullscreen compatibility

| Game mode | DX version | Works? |
|-----------|-----------|--------|
| Borderless Windowed | any | ✅ |
| Exclusive Fullscreen | DX11 / DX12 | ✅ (DWM flip model) |
| Exclusive Fullscreen | DX10 | ✅ |
| Exclusive Fullscreen | DX9 (D3D9Ex) | ✅ (Win10 1703+) |
| Exclusive Fullscreen | DX9 legacy (pre-Win10 drivers) | ⚠️ rare edge case |
| OpenGL / Vulkan | — | ✅ |

## Features

| | |
|---|---|
| **6 crosshair styles** | Cross, Dot, Circle, Cross+Dot, T-Cross, Circle+Cross |
| **Full color picker** | Primary + outline color |
| **Live preview** | Instant preview in settings panel |
| **System tray** | Right-click → Toggle / Settings / Quit |
| **Hotkey** | `Ctrl+Shift+H` toggles on/off (customisable) |
| **Config saved** | `~/.strcrosshair/config.json` — persists across launches |
| **DPI-aware** | Correct position on 4K / high-DPI displays |
| **No DLL injection** | Anti-cheat safe — uses Windows' own DWM compositor |

## Settings

Open from system tray or on launch.

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
| Outer Circle | Outer ring (useful for spread visualisation) |
| Offset X / Y | Move crosshair off true screen center |
| Hotkey | Global keyboard shortcut to toggle visibility |
| Start Minimized | Don't open settings on launch |

## Architecture

```
main.py  ──── tkinter settings window + system tray (main process)
          └── spawns crosshair_engine.py as subprocess
                  │  pygame SDL2 render loop (60 fps)
                  │  Win32: WS_EX_LAYERED | WS_EX_TRANSPARENT | HWND_TOPMOST
                  └── DwmExtendFrameIntoClientArea → DWM GPU overlay
         IPC: newline-delimited JSON over stdin
```
