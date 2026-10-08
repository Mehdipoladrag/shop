"""Reusable device parts: color finishes, camera lenses, wallpapers and screens.

The light always comes from the top left, so in every pair of colors the first one is the lit
side and the second one the shaded side.
"""

from __future__ import annotations

from dataclasses import dataclass

from .toolkit import (
    WHITE,
    Color,
    Layer,
    Linear,
    Radial,
    Shape,
    arc_band,
    circle,
    color,
    darken,
    ellipse,
    lighten,
    mix,
    polygon,
    rotated_ellipse,
    rounded_rect,
    with_alpha,
)

DIAGONAL = 45.0  # gradient angle from the lit corner (top left) to the shaded corner
GLASS_BLACK = color("#07090f")
SHEEN_ANGLE = 38.0
SHEEN_SHADE_RATIO = 0.8  # how strong the shaded corner is compared with the highlight


# --------------------------------------------------------------------------- finishes


@dataclass(frozen=True)
class Finish:
    """The colors of one device variant."""

    back: tuple[Color, Color]  # back glass or body
    frame: tuple[Color, Color]  # side rail
    module: tuple[Color, Color]  # camera plateau
    ring: tuple[Color, Color]  # metal ring around every lens


def finish(back_lit: str, back_shaded: str, frame_lit: str | None = None, frame_shaded: str | None = None,
           module_lit: str | None = None, module_shaded: str | None = None) -> Finish:
    """Builds a Finish from hex colors; frame, module and lens ring are derived when omitted."""
    lit, shaded = color(back_lit), color(back_shaded)
    frame = (color(frame_lit) if frame_lit else lighten(lit, 0.38),
             color(frame_shaded) if frame_shaded else darken(shaded, 0.16))
    module = (color(module_lit) if module_lit else lighten(lit, 0.16),
              color(module_shaded) if module_shaded else mix(shaded, lit, 0.35))
    ring = (lighten(frame[0], 0.15), darken(frame[1], 0.32))
    return Finish((lit, shaded), frame, module, ring)


# --------------------------------------------------------------------------- wallpapers


@dataclass(frozen=True)
class Wallpaper:
    """An abstract navy and blue screen background: a base gradient plus soft color blooms."""

    top: str
    bottom: str
    blooms: tuple  # ((hex color, (x, y) as fractions of the screen, radius as a fraction of its height), ...)


WALLPAPERS = {
    "ocean": Wallpaper("#07173f", "#0b3480", (("#2f7bff", (0.15, 0.9), 0.62), ("#3f66ff", (0.92, 0.14), 0.5), ("#12c5e8", (0.88, 0.94), 0.4))),
    "midnight": Wallpaper("#060d2b", "#112c74", (("#3b6dff", (0.8, 0.85), 0.58), ("#0fb4d8", (0.08, 0.45), 0.42), ("#5a7bff", (0.3, 0.06), 0.38))),
    "aurora": Wallpaper("#08173a", "#0a4380", (("#10c9d0", (0.2, 0.92), 0.55), ("#3a66ff", (0.88, 0.35), 0.55), ("#6a86ff", (0.55, 0.04), 0.38))),
    "dusk": Wallpaper("#0a1442", "#16307e", (("#4f78ff", (0.5, 0.96), 0.6), ("#7388ff", (0.92, 0.1), 0.42), ("#22b8ff", (0.05, 0.28), 0.4))),
}
WALLPAPER_ORDER = tuple(WALLPAPERS)
BLOOM_OPACITY = 0.92
ARC_OPACITY = 0.14
ARC_WIDTH_FRACTION = 0.006  # arc stroke width as a fraction of the screen height
GLARE_OPACITY = 0.11


def draw_wallpaper(layer: Layer, screen: Shape, box: tuple, wallpaper: Wallpaper) -> None:
    """Paints the wallpaper inside the `screen` shape; `box` is the screen rectangle."""
    left, top, right, bottom = box
    width, height = right - left, bottom - top
    layer.fill(screen, Linear.of(color(wallpaper.top), color(wallpaper.bottom), angle=75), clip=None)
    for hex_color, (fx, fy), radius in wallpaper.blooms:
        reach = radius * height
        bloom = circle(left + fx * width, top + fy * height, reach)
        layer.fill(bloom, Radial.of(color(hex_color), color(hex_color, 0)), BLOOM_OPACITY, clip=screen)
    stroke = ARC_WIDTH_FRACTION * height
    for index, scale in enumerate((0.9, 1.25, 1.65)):
        rx, ry = width * scale, height * scale * 0.62
        ring = (left - rx * 0.25, top + height * 0.55 - ry + index * height * 0.05, left - rx * 0.25 + 2 * rx, top + height * 0.55 + ry + index * height * 0.05)
        layer.fill(arc_band(ring, 200, 340, stroke), WHITE, ARC_OPACITY, clip=screen)
    glare = polygon([(left, top), (left + width * 0.72, top), (left, top + height * 0.42)])
    layer.fill(glare, Linear.of(with_alpha(WHITE, 1.0), color("#ffffff", 0), angle=DIAGONAL), GLARE_OPACITY, clip=screen)


# --------------------------------------------------------------------------- lenses


LENS_GLASS = (color("#232d5c"), color("#0b1024"), color("#03040a"))
LENS_CORE = (color("#4a3fb0", 235), color("#1a1d5c", 200), color("#06071a", 0))


def draw_lens(layer: Layer, cx: float, cy: float, radius: float, ring: tuple[Color, Color], thickness: float = 0.22) -> None:
    """A camera lens: metal ring, dark barrel, coated glass and two small reflections.

    `thickness` is the width of the metal ring as a fraction of the radius.
    """
    outer = circle(cx, cy, radius)
    layer.shadow(outer, blur=radius * 0.12, offset=(radius * 0.06, radius * 0.12), opacity=0.5)
    metal = ((0.0, lighten(ring[0], 0.4)), (0.42, ring[0]), (0.52, ring[1]), (1.0, darken(ring[1], 0.3)))
    layer.fill(outer, Linear(metal, angle=DIAGONAL))
    layer.fill(arc_band((cx - radius * 0.93, cy - radius * 0.93, cx + radius * 0.93, cy + radius * 0.93), 190, 265, radius * 0.07), WHITE, 0.55)
    barrel = radius * (1 - thickness)
    layer.fill(circle(cx, cy, barrel), Linear.of(darken(ring[1], 0.55), lighten(ring[1], 0.1), angle=DIAGONAL))
    glass = barrel * 0.9
    layer.fill(circle(cx, cy, glass), Radial.of(*LENS_GLASS, center=(0.42, 0.4), radius=0.62))
    layer.fill(circle(cx + glass * 0.12, cy + glass * 0.14, glass * 0.62), Radial.of(*LENS_CORE))
    layer.fill(circle(cx, cy, glass * 0.3), Radial.of(color("#05060f"), color("#101540"), center=(0.4, 0.4)))
    layer.fill(rotated_ellipse(cx - glass * 0.38, cy - glass * 0.42, glass * 0.2, glass * 0.1, -38), WHITE, 0.62)
    layer.fill(rotated_ellipse(cx + glass * 0.36, cy + glass * 0.4, glass * 0.16, glass * 0.06, -38), color("#7fd3ff"), 0.35)


def draw_glass_lens(layer: Layer, cx: float, cy: float, radius: float, ring: tuple[Color, Color]) -> None:
    """A flat Android style lens: thin metal rim around a black glass disc."""
    outer = circle(cx, cy, radius)
    layer.shadow(outer, blur=radius * 0.1, offset=(radius * 0.05, radius * 0.1), opacity=0.4)
    layer.fill(outer, Linear.of(ring[0], ring[1], angle=DIAGONAL))
    layer.fill(circle(cx, cy, radius * 0.86), Radial.of(color("#10142c"), color("#030409"), center=(0.4, 0.38), radius=0.6))
    layer.fill(circle(cx + radius * 0.06, cy + radius * 0.08, radius * 0.5), Radial.of(color("#2b2f86", 220), color("#10123a", 0)))
    layer.fill(rotated_ellipse(cx - radius * 0.34, cy - radius * 0.38, radius * 0.18, radius * 0.09, -38), WHITE, 0.55)


def draw_flash(layer: Layer, cx: float, cy: float, radius: float, ring: tuple[Color, Color]) -> None:
    """The True Tone flash: a small ring with a warm light."""
    layer.fill(circle(cx, cy, radius), Linear.of(ring[0], ring[1], angle=DIAGONAL))
    layer.fill(circle(cx, cy, radius * 0.74), Radial.of(color("#fff6d8"), color("#e8cf8f"), color("#9c8650"), radius=0.55))


def draw_dot(layer: Layer, cx: float, cy: float, radius: float, tint: str = "#10131c") -> None:
    """A tiny sensor or microphone opening."""
    layer.fill(circle(cx, cy, radius), Radial.of(lighten(color(tint), 0.25), color(tint), radius=0.6))


def draw_lidar(layer: Layer, cx: float, cy: float, radius: float, ring: tuple[Color, Color]) -> None:
    layer.fill(circle(cx, cy, radius), Linear.of(ring[0], ring[1], angle=DIAGONAL))
    layer.fill(circle(cx, cy, radius * 0.78), Radial.of(color("#1b2140"), color("#05060c"), center=(0.4, 0.4), radius=0.6))
    layer.fill(rotated_ellipse(cx - radius * 0.28, cy - radius * 0.3, radius * 0.22, radius * 0.1, -38), WHITE, 0.4)


# --------------------------------------------------------------------------- screens


def draw_island(layer: Layer, cx: float, top: float, width: float, height: float) -> None:
    """The Dynamic Island pill with a faint camera lens on its right end."""
    layer.fill(rounded_rect((cx - width / 2, top, cx + width / 2, top + height), height / 2), GLASS_BLACK)
    lens_x = cx + width / 2 - height * 0.72
    layer.fill(circle(lens_x, top + height / 2, height * 0.3), Radial.of(color("#2c3470"), color("#0a0d1c"), radius=0.6))
    layer.fill(circle(lens_x - height * 0.07, top + height * 0.4, height * 0.07), WHITE, 0.5)


def draw_notch(layer: Layer, cx: float, top: float, width: float, height: float, screen: Shape) -> None:
    """The classic notch: a black tab hanging from the top edge, clipped to the screen."""
    radius = height * 0.5
    tab = rounded_rect((cx - width / 2, top - radius, cx + width / 2, top + height), radius, 2.4)
    layer.fill(tab, GLASS_BLACK, clip=screen)
    speaker = rounded_rect((cx - width * 0.15, top + height * 0.3, cx + width * 0.15, top + height * 0.46), height * 0.08)
    layer.fill(speaker, color("#1c2030"))
    layer.fill(circle(cx + width * 0.27, top + height * 0.4, height * 0.13), Radial.of(color("#2c3470"), color("#0a0d1c"), radius=0.6))


def draw_punch_hole(layer: Layer, cx: float, cy: float, radius: float) -> None:
    layer.fill(circle(cx, cy, radius), GLASS_BLACK)
    layer.fill(circle(cx, cy, radius * 0.5), Radial.of(color("#1d2358"), color("#05060f"), radius=0.6))


def draw_ground_shadow(layer: Layer, cx: float, y: float, width: float, depth: float, opacity: float = 0.3) -> None:
    """A soft contact shadow under a device standing on an imaginary floor at height `y`."""
    layer.shadow(ellipse((cx - width / 2, y - depth / 2, cx + width / 2, y + depth / 2)), blur=depth * 0.45, opacity=opacity)
    layer.shadow(ellipse((cx - width * 0.4, y - depth * 0.18, cx + width * 0.4, y + depth * 0.18)), blur=depth * 0.14, opacity=opacity * 1.2)


def sheen(layer: Layer, shape: Shape, strength: float) -> None:
    """A soft diagonal reflection across a glass surface: bright near the top left, shaded at the bottom right."""
    light = round(255 * strength)
    shade = round(255 * strength * SHEEN_SHADE_RATIO)
    clear = color("#ffffff", 0)
    stops = ((0.0, clear), (0.2, (255, 255, 255, light)), (0.45, clear), (0.7, color("#000000", 0)), (1.0, (0, 0, 0, shade)))
    layer.fill(shape, Linear(stops, angle=SHEEN_ANGLE))
