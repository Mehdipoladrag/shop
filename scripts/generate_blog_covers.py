#!/usr/bin/env python3
"""Draws the cover pictures of the demo blog posts (seed_demo_blog).

Each cover is composed from the catalog illustrations (see generate_demo_art.py) on a navy
background, so it needs no photographs and no network access. The drawing is deterministic.

Usage:
    python scripts/generate_demo_art.py        # once, creates the product pictures
    python scripts/generate_blog_covers.py     # writes shop/static/assets/img/blog/cover-*.jpg

A real photograph can replace any cover: keep the file name and the seed picks it up.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
PRODUCT_PICTURES = REPO_ROOT / "shop" / "static" / "assets" / "img" / "product_img" / "new"
OUTPUT = REPO_ROOT / "shop" / "static" / "assets" / "img" / "blog"

SIZE = (1200, 750)
SUPERSAMPLE = 3
JPEG_QUALITY = 86
NAVY_DARK = (11, 24, 56)
NAVY_MID = (31, 58, 110)
NAVY_GLOW = (63, 102, 176)
CORAL = (255, 107, 74)
INK = (10, 20, 41)
WHITE = (255, 255, 255)


@dataclass(frozen=True)
class Placement:
    """One product picture on the cover; positions and heights are fractions of the cover size."""

    picture: str
    x: float
    y: float
    height: float
    tilt: float = 0.0


@dataclass(frozen=True)
class Cover:
    name: str
    placements: list[Placement]
    badge: str = ""  # "versus" draws a VS disc, "shield" a shield with a check mark
    extras: dict = field(default_factory=dict)


COVERS = [
    Cover(
        "cover-choose-iphone",
        [
            Placement("iphone-air-sky-blue", 0.22, 0.56, 0.74, tilt=8),
            Placement("iphone-16-teal", 0.78, 0.56, 0.74, tilt=-8),
            Placement("iphone-17-pro-max-cosmic-orange", 0.50, 0.52, 0.94),
        ],
    ),
    Cover(
        "cover-iphone-16-vs-15",
        [
            Placement("iphone-16-pink", 0.27, 0.52, 0.86, tilt=5),
            Placement("iphone-15-blue", 0.73, 0.52, 0.86, tilt=-5),
        ],
        badge="versus",
    ),
    Cover(
        "cover-device-care",
        [
            Placement("ipad-air-11-blue", 0.27, 0.44, 0.56, tilt=4),
            Placement("iphone-17-black", 0.52, 0.50, 0.82, tilt=-3),
            Placement("airpods-pro-3", 0.80, 0.66, 0.46),
        ],
        badge="shield",
    ),
]


def background() -> Image.Image:
    """Dark navy with a soft light behind the devices and a few thin decorative rings."""
    width, height = SIZE
    base = Image.new("RGB", SIZE, NAVY_DARK)
    glow_mask = Image.radial_gradient("L").resize((int(width * 1.05), int(height * 1.5)))
    glow_mask = ImageChops.invert(glow_mask).point(lambda value: int(value * 0.85))
    glow = Image.new("RGB", SIZE, NAVY_GLOW)
    placed = Image.new("L", SIZE, 0)
    placed.paste(glow_mask, ((width - glow_mask.width) // 2, int(height * 0.5 - glow_mask.height / 2)))
    base = Image.composite(glow, base, placed.filter(ImageFilter.GaussianBlur(30)))
    mid = Image.composite(Image.new("RGB", SIZE, NAVY_MID), base, Image.linear_gradient("L").resize(SIZE).point(lambda v: int(v * 0.35)))
    rings = Image.new("RGBA", (width * SUPERSAMPLE, height * SUPERSAMPLE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(rings)
    for radius, opacity in ((330, 26), (470, 18), (620, 12)):
        center = (width * SUPERSAMPLE // 2, int(height * SUPERSAMPLE * 0.52))
        box = (center[0] - radius * SUPERSAMPLE, center[1] - radius * SUPERSAMPLE, center[0] + radius * SUPERSAMPLE, center[1] + radius * SUPERSAMPLE)
        draw.ellipse(box, outline=(255, 255, 255, opacity), width=2 * SUPERSAMPLE)
    dot = int(34 * SUPERSAMPLE)
    draw.ellipse((int(width * 0.92 * SUPERSAMPLE) - dot // 2, int(height * 0.14 * SUPERSAMPLE) - dot // 2, int(width * 0.92 * SUPERSAMPLE) + dot // 2, int(height * 0.14 * SUPERSAMPLE) + dot // 2), fill=CORAL + (255,))
    rings = rings.resize(SIZE, Image.Resampling.LANCZOS)
    return Image.alpha_composite(mid.convert("RGBA"), rings)


def place(canvas: Image.Image, placement: Placement) -> None:
    """Pastes one product picture scaled to the wanted height, centred on its position."""
    picture = Image.open(PRODUCT_PICTURES / f"{placement.picture}.png").convert("RGBA")
    bounds = picture.getbbox() or (0, 0, *picture.size)
    picture = picture.crop(bounds)
    target_height = int(SIZE[1] * placement.height)
    picture = picture.resize((round(picture.width * target_height / picture.height), target_height), Image.Resampling.LANCZOS)
    if placement.tilt:
        picture = picture.rotate(placement.tilt, resample=Image.Resampling.BICUBIC, expand=True)
    shadow = Image.new("RGBA", picture.size, (0, 0, 0, 0))
    shadow.putalpha(picture.getchannel("A").point(lambda value: int(value * 0.35)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    x = int(SIZE[0] * placement.x - picture.width / 2)
    y = int(SIZE[1] * placement.y - picture.height / 2)
    canvas.alpha_composite(shadow, (x, y + 22))
    canvas.alpha_composite(picture, (x, y))


def versus_disc(canvas: Image.Image) -> None:
    """A coral disc with "VS" between the two compared devices."""
    radius = 66
    layer = Image.new("RGBA", (radius * 2 * SUPERSAMPLE,) * 2, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse((0, 0, layer.width - 1, layer.height - 1), fill=CORAL + (255,))
    layer = layer.resize((radius * 2, radius * 2), Image.Resampling.LANCZOS)
    font = ImageFont.load_default(size=62)
    ImageDraw.Draw(layer).text((radius, radius + 2), "VS", font=font, fill=INK + (255,), anchor="mm")
    canvas.alpha_composite(layer, (SIZE[0] // 2 - radius, SIZE[1] // 2 - radius))


def shield(canvas: Image.Image) -> None:
    """A white shield with a navy check mark, the symbol of protection."""
    width, height = 190, 224
    layer = Image.new("RGBA", (width * SUPERSAMPLE, height * SUPERSAMPLE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    scale = SUPERSAMPLE
    outline = [(95, 0), (180, 30), (180, 108), (150, 170), (95, 224), (40, 170), (10, 108), (10, 30)]
    draw.polygon([(x * scale, y * scale) for x, y in outline], fill=WHITE + (255,))
    draw.line([(58 * scale, 112 * scale), (86 * scale, 142 * scale), (136 * scale, 84 * scale)], fill=NAVY_MID + (255,), width=18 * scale, joint="curve")
    for cap in ((58, 112), (136, 84)):
        draw.ellipse(((cap[0] - 9) * scale, (cap[1] - 9) * scale, (cap[0] + 9) * scale, (cap[1] + 9) * scale), fill=NAVY_MID + (255,))
    layer = layer.resize((width, height), Image.Resampling.LANCZOS)
    padding = 48  # room for the blur, otherwise its edge is cut off in a visible box
    padded = Image.new("RGBA", (width + 2 * padding, height + 2 * padding), (0, 0, 0, 0))
    padded.paste(layer, (padding, padding))
    glow = padded.filter(ImageFilter.GaussianBlur(16))
    x, y = int(SIZE[0] * 0.09), int(SIZE[1] * 0.60)
    canvas.alpha_composite(glow, (x - padding, y - padding))
    canvas.alpha_composite(layer, (x, y))


def render(cover: Cover) -> Image.Image:
    canvas = background()
    for placement in cover.placements:
        place(canvas, placement)
    if cover.badge == "versus":
        versus_disc(canvas)
    if cover.badge == "shield":
        shield(canvas)
    return canvas.convert("RGB")


def main() -> int:
    missing = [p.picture for cover in COVERS for p in cover.placements if not (PRODUCT_PICTURES / f"{p.picture}.png").is_file()]
    if missing:
        print(f"Run scripts/generate_demo_art.py first; missing: {', '.join(sorted(set(missing)))}", file=sys.stderr)
        return 2
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for cover in COVERS:
        target = OUTPUT / f"{cover.name}.jpg"
        render(cover).save(target, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        print(f"{target.name:34} {target.stat().st_size / 1024:6.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
