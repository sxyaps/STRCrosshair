# STRCrosshair

Custom always-on-top crosshair overlay for Windows — built for gaming.

## Features

- **Always on top** — uses Win32 `HWND_TOPMOST` + re-enforced every 4 s
- **Click-through** — `WS_EX_TRANSPARENT` so the overlay never steals clicks
- **No taskbar / Alt-Tab entry** — `WS_EX_TOOLWINDOW` keeps it invisible
- **6 crosshair styles** — Cross, Dot, Circle, Cross+Dot, T-Cross, Circle+Cross
- **Full customization** — color, outline, size, thickness, gap, opacity, position offset
- **Live preview** in the settings panel
- **System tray** — right-click to toggle / open settings / quit
- **Global hotkey** (`Ctrl+Shift+H` by default) to show/hide the crosshair
- **Config auto-saved** to `~/.strcrosshair/config.json`

## Quickstart

```bat
pip install -r requirements.txt
python main.py
```

## Build standalone .exe

```bat
build.bat
```

Produces `dist\STRCrosshair.exe` — no Python install required on target machine.

## Fullscreen notes

| Game mode | Works? |
|-----------|--------|
| Borderless Windowed | ✅ Works perfectly |
| Windowed | ✅ Works perfectly |
| Exclusive Fullscreen (DX9) | ⚠️ May not appear — use Borderless Windowed instead |
| Exclusive Fullscreen (DX11/12 flip model) | ✅ Usually works |

Set your game to **Borderless Windowed** for guaranteed overlay support. Most competitive games (Valorant, CS2, Apex, Fortnite) already default to this.

## Hotkey

Default: `Ctrl+Shift+H` — toggles crosshair on/off instantly.  
Change it in Settings → Hotkey (requires app restart to re-register).

## Settings

Open from the system tray icon or on launch.

| Setting | Description |
|---------|-------------|
| Style | Cross / Dot / Circle / Cross+Dot / T-Cross / Circle+Cross |
| Color | Primary crosshair color |
| Outline | Black (or custom) border for contrast on any background |
| Arm Length | How long each arm extends from center gap |
| Thickness | Line width in pixels |
| Center Gap | Empty space around the exact center point |
| Opacity | Overall transparency of the crosshair |
| Center Dot | Small filled circle at center |
| Outer Circle | Dynamic circle overlay (e.g. for spread indication) |
| Offset X/Y | Move crosshair off true center if needed |
