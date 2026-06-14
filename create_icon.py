"""Generates assets/icon.ico — run once before building."""
import os
from PIL import Image, ImageDraw

def make_frame(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size / 64  # scale factor relative to 64px base

    cx = cy = size // 2
    pad = max(2, int(3 * s))

    # Dark background circle
    d.ellipse([pad, pad, size - pad, size - pad], fill=(13, 13, 26, 230))
    # Purple border
    bw = max(1, int(2.5 * s))
    d.ellipse([pad, pad, size - pad, size - pad], outline=(124, 58, 237), width=bw)

    # Cyan crosshair
    col = (0, 212, 255)
    g  = max(2, int(5 * s))   # center gap
    t  = max(1, int(2 * s))   # arm thickness
    m  = pad + bw + max(1, int(2 * s))  # arm start from edge

    d.rectangle([cx - t, m,      cx + t, cy - g], fill=col)  # top
    d.rectangle([cx - t, cy + g, cx + t, size - m], fill=col)  # bottom
    d.rectangle([m,      cy - t, cx - g, cy + t], fill=col)  # left
    d.rectangle([cx + g, cy - t, size - m, cy + t], fill=col)  # right

    # Center dot
    dot = max(1, int(2 * s))
    d.ellipse([cx - dot, cy - dot, cx + dot, cy + dot], fill=col)

    return img


def main():
    os.makedirs("assets", exist_ok=True)
    sizes = [16, 24, 32, 48, 64, 128, 256]
    frames = [make_frame(sz) for sz in sizes]
    frames[0].save(
        "assets/icon.ico",
        format="ICO",
        sizes=[(sz, sz) for sz in sizes],
        append_images=frames[1:],
    )
    print("Created assets/icon.ico")


if __name__ == "__main__":
    main()
