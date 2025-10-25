import os
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tmpdata"

CLASSES = {
    "Healthy": (50, 160, 60),  # green
    "Disease": (140, 90, 50),  # brown
}

OUT.mkdir(parents=True, exist_ok=True)

for cls, color in CLASSES.items():
    d = OUT / cls
    d.mkdir(parents=True, exist_ok=True)
    for i in range(12):
        img = Image.new("RGB", (128, 128), color)
        draw = ImageDraw.Draw(img)
        if cls == "Disease":
            # draw a few random-ish spots
            for j in range(6):
                x = (i * 17 + j * 13) % 100 + 10
                y = (i * 11 + j * 19) % 100 + 10
                r = 6 + (i + j) % 10
                draw.ellipse((x, y, x + r, y + r), fill=(220, 220, 220))
        img.save(d / f"{cls}_{i}.png")

print(f"Wrote synthetic dataset to {OUT}")
