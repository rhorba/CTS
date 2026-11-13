#!/usr/bin/env python3
"""Draw the CTS plugin icon: six phase segments around a three-person team.

The ring is the six gated phases, read clockwise from the top; the last one (SHIP)
is green. The three dots are the team. Run from the repo root:

    python3 scripts/build_icon.py
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path("claude-team-skills/.claude-plugin/icon.png")
SIZE = 1024
SCALE = 4  # supersample, then downscale for smooth edges

NAVY = (26, 26, 46)
GREEN = (48, 209, 88)
WHITE = (255, 255, 255)
# UNDERSTAND -> VERIFY, light to full brand purple; SHIP is green.
PHASES = [(196, 184, 255), (170, 152, 255), (144, 122, 255), (124, 98, 255), (107, 78, 255), GREEN]

RING_OUTER = 0.40   # radii as a fraction of the canvas
RING_INNER = 0.30
GAP_DEG = 10        # the gate between two phases
DOT_ORBIT = 0.115
DOT_RADIUS = 0.058


def draw(size=SIZE, scale=SCALE):
    n = size * scale
    c = n / 2
    img = Image.new("RGB", (n, n), NAVY)
    d = ImageDraw.Draw(img)

    outer, inner = RING_OUTER * n, RING_INNER * n
    width = outer - inner
    box = [c - outer, c - outer, c + outer, c + outer]
    step = 360 / len(PHASES)
    for i, colour in enumerate(PHASES):
        start = -90 + i * step + GAP_DEG / 2
        end = -90 + (i + 1) * step - GAP_DEG / 2
        d.arc(box, start, end, fill=colour, width=round(width))

    r = DOT_RADIUS * n
    for k in range(3):
        angle = math.radians(-90 + k * 120)
        x = c + DOT_ORBIT * n * math.cos(angle)
        y = c + DOT_ORBIT * n * math.sin(angle)
        d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)

    return img.resize((size, size), Image.LANCZOS)


def main():
    draw().save(OUT, optimize=True)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
