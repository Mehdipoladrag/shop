"""Category tile pictures: a navy disc with a small hero illustration of the category."""

from __future__ import annotations

from PIL import Image

from .parts import DIAGONAL
from .toolkit import (
    WHITE,
    Layer,
    Linear,
    Radial,
    arc_band,
    circle,
    color,
)

SIZE = 600
DISC_RADIUS = 284
ART_FRACTION = 0.74  # the illustration fills this share of the disc diameter
ART_SHIFT_Y = 6  # lifts the illustration a little above the disc center


def _disc() -> Layer:
    """The background: a navy disc with a soft light from the top left and two faint rings."""
    layer = Layer(SIZE, SIZE)
    center = SIZE / 2
    disc = circle(center, center, DISC_RADIUS)
    layer.shadow(disc, blur=9, offset=(0, 8), opacity=0.25)
    layer.fill(disc, Linear.of(color("#2f5aa8"), color("#10275a"), angle=DIAGONAL + 20))
    layer.fill(circle(center * 0.72, center * 0.6, DISC_RADIUS * 0.95), Radial.of(color("#6f9bff", 120), color("#6f9bff", 0)), clip=disc)
    for radius, opacity in ((DISC_RADIUS - 22, 0.16), (DISC_RADIUS - 52, 0.09)):
        ring = (center - radius, center - radius, center + radius, center + radius)
        layer.fill(arc_band(ring, 0, 360, 2.2), WHITE, opacity, clip=disc)
    return layer


def _fit(art: Image.Image) -> Image.Image:
    """Crops the illustration to its content and scales it to the disc."""
    content = art.crop(art.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox())
    limit = DISC_RADIUS * 2 * ART_FRACTION
    scale = min(limit / content.width, limit / content.height)
    return content.resize((round(content.width * scale), round(content.height * scale)), Image.Resampling.LANCZOS)


def category_picture(art: Image.Image) -> Image.Image:
    """The finished 600 x 600 picture for a category, built from a product style illustration."""
    disc = _disc().output((SIZE, SIZE))
    art = _fit(art)
    disc.alpha_composite(art, ((SIZE - art.width) // 2, (SIZE - art.height) // 2 - ART_SHIFT_Y))
    return disc
