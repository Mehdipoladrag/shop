"""Tablet illustrations: the front of an iPad in front of its back panel, with an Apple Pencil."""

from __future__ import annotations

import math
from dataclasses import dataclass

from PIL import Image

from .parts import (
    DIAGONAL,
    GLASS_BLACK,
    WALLPAPERS,
    Finish,
    draw_dot,
    draw_flash,
    draw_ground_shadow,
    draw_lens,
    draw_wallpaper,
    finish,
    sheen,
)
from .toolkit import (
    WHITE,
    Layer,
    Linear,
    Radial,
    Shape,
    capsule,
    circle,
    color,
    darken,
    lighten,
    polygon,
    rounded_rect,
)

CANVAS = 900
SPRITE_MARGIN = 46
LANDSCAPE_PX_PER_MM = 2.62
PORTRAIT_PX_PER_MM = 3.5  # the mini is drawn larger so that it does not look lost on the canvas
BACK_OFFSET_X = 0.07  # how far the back panel is shifted left of the front, as a fraction of the width
BACK_OFFSET_Y = 0.11  # ... and up, as a fraction of the height
SEAM = 0.9

PENCIL_LENGTH_MM = 166.0
PENCIL_WIDTH_MM = 8.9
PENCIL_LEAN = 13.0  # degrees the pencil leans towards the screen
PENCIL_INSET = 0.07  # distance of the pencil tip from the right edge, as a fraction of the width


@dataclass(frozen=True)
class TabletModel:
    """Proportions of one iPad (landscape size in mm; `portrait` turns it upright)."""

    width_mm: float
    height_mm: float
    portrait: bool = False
    corner: float = 0.075  # corner radius as a fraction of the short side
    bezel: float = 0.034  # screen bezel as a fraction of the short side
    pencil: bool = False
    back_camera: str = "plate"  # "plate" (raised square) or "ring" (flush lens)


MODELS = {
    "ipad-pro-13": TabletModel(281.6, 215.5, bezel=0.03, pencil=True),
    "ipad-pro-11": TabletModel(249.7, 177.5, bezel=0.034, pencil=True),
    "ipad-air-11": TabletModel(247.6, 178.5, bezel=0.05, pencil=True, back_camera="ring"),
    "ipad-mini": TabletModel(195.4, 134.8, portrait=True, bezel=0.062, back_camera="ring", corner=0.085),
    "ipad": TabletModel(248.6, 179.5, bezel=0.062, back_camera="ring"),
}

FINISHES = {
    "silver": finish("#e8eaee", "#c2c6cd", "#f3f4f7", "#a9adb6"),
    "space-black": finish("#41434a", "#25262b", "#5c5f67", "#18191c"),
    "blue": finish("#a9c2e0", "#7f9dc4", "#c4d6ec", "#6f8db5"),
    "purple": finish("#c6b9dc", "#9b8cba", "#d9cfe9", "#8a7aab"),
    "starlight": finish("#eee9de", "#cfc8b8", "#f7f4ec", "#b9b1a0"),
    "yellow": finish("#f4df93", "#d9bd5c", "#f8ebb6", "#c4a74c"),
    "pink": finish("#f5c2d2", "#dc96ae", "#f9d6e2", "#c9839c"),
}


def _size(model: TabletModel) -> tuple[float, float]:
    scale = PORTRAIT_PX_PER_MM if model.portrait else LANDSCAPE_PX_PER_MM
    width, height = model.width_mm * scale, model.height_mm * scale
    return (height, width) if model.portrait else (width, height)


def _radius(model: TabletModel, size: tuple[float, float]) -> float:
    return model.corner * min(size)


def _sprite(size: tuple[float, float]) -> tuple[Layer, tuple]:
    layer = Layer(size[0] + 2 * SPRITE_MARGIN, size[1] + 2 * SPRITE_MARGIN)
    return layer, (SPRITE_MARGIN, SPRITE_MARGIN, SPRITE_MARGIN + size[0], SPRITE_MARGIN + size[1])


def _outline(layer: Layer, box: tuple, radius: float, fin: Finish, rail: float) -> Shape:
    """Draws the aluminium rail and returns the shape of the face inside it."""
    outer = rounded_rect(box, radius, 3.0)
    layer.fill(outer, Linear.of(fin.frame[0], fin.frame[1], angle=DIAGONAL))
    stops = ((0.0, color("#ffffff", 210)), (0.3, color("#ffffff", 0)), (0.72, color("#000000", 0)), (1.0, color("#000000", 80)))
    layer.fill(outer, Linear(stops, angle=DIAGONAL))
    gap = rounded_rect((box[0] + rail - SEAM, box[1] + rail - SEAM, box[2] - rail + SEAM, box[3] - rail + SEAM), radius - rail + SEAM, 3.0)
    layer.fill(gap, color("#000000", 70))
    return rounded_rect((box[0] + rail, box[1] + rail, box[2] - rail, box[3] - rail), radius - rail, 3.0)


def draw_front(model: TabletModel, fin: Finish, wallpaper_key: str) -> Layer:
    """The screen side: aluminium rail, black bezel, wallpaper and the front camera."""
    size = _size(model)
    layer, box = _sprite(size)
    radius = _radius(model, size)
    rail = 2.4
    glass = _outline(layer, box, radius, fin, rail)
    layer.fill(glass, Linear.of(color("#10131c"), GLASS_BLACK, angle=DIAGONAL))
    bezel = model.bezel * min(size)
    screen_box = (box[0] + rail + bezel, box[1] + rail + bezel, box[2] - rail - bezel, box[3] - rail - bezel)
    screen = rounded_rect(screen_box, max(radius - rail - bezel * 0.8, 4), 3.0)
    draw_wallpaper(layer, screen, screen_box, WALLPAPERS[wallpaper_key])
    center_x = (box[0] + box[2]) / 2
    draw_dot(layer, center_x, box[1] + rail + bezel / 2, max(bezel * 0.17, 1.6), "#1a2040")
    return layer


def draw_back(model: TabletModel, fin: Finish) -> Layer:
    """The back panel with its single camera in the top left corner."""
    size = _size(model)
    layer, box = _sprite(size)
    radius = _radius(model, size)
    rail = 2.4
    face = _outline(layer, box, radius, fin, rail)
    layer.fill(face, Linear.of(fin.back[0], fin.back[1], angle=DIAGONAL + 12))
    sheen(layer, face, 0.16)
    short = min(size)
    lens_x, lens_y = box[0] + 0.09 * short, box[1] + 0.09 * short
    if model.back_camera == "plate":
        plate = rounded_rect((lens_x - 0.065 * short, lens_y - 0.065 * short, lens_x + 0.15 * short, lens_y + 0.21 * short), 0.05 * short, 3.0)
        layer.shadow(plate, blur=4, offset=(2, 4), opacity=0.3)
        layer.fill(plate, Linear.of(lighten(fin.module[0], 0.45), darken(fin.module[1], 0.25), angle=DIAGONAL))
        inner = rounded_rect((lens_x - 0.065 * short + 2, lens_y - 0.065 * short + 2, lens_x + 0.15 * short - 2, lens_y + 0.21 * short - 2), 0.05 * short - 2, 3.0)
        layer.fill(inner, Linear.of(fin.module[0], fin.module[1], angle=DIAGONAL + 10))
        draw_flash(layer, lens_x + 0.04 * short, lens_y + 0.155 * short, 0.02 * short, fin.ring)
    draw_lens(layer, lens_x + (0.04 * short if model.back_camera == "plate" else 0), lens_y, 0.045 * short, fin.ring)
    return layer


def draw_pencil(scale: float = 1.0) -> Layer:
    """A white Apple Pencil standing on its tip (rotated later), lit from the left."""
    length = PENCIL_LENGTH_MM * LANDSCAPE_PX_PER_MM * scale
    width = PENCIL_WIDTH_MM * LANDSCAPE_PX_PER_MM * scale
    layer = Layer(width + 2 * SPRITE_MARGIN, length + 2 * SPRITE_MARGIN)
    cx, top = layer.width / 2, SPRITE_MARGIN
    tip_length = length * 0.13
    body_bottom = top + length - tip_length
    body = capsule((cx, top + width / 2), (cx, body_bottom), width / 2)
    barrel = Linear(((0.0, color("#ffffff")), (0.35, color("#f4f6f9")), (0.8, color("#d5dae2")), (1.0, color("#b9c0cb"))), angle=0)
    cone = polygon([(cx - width / 2, body_bottom), (cx + width / 2, body_bottom), (cx + width * 0.06, top + length), (cx - width * 0.06, top + length)])
    layer.fill(cone, Linear(((0.0, color("#ffffff")), (0.5, color("#eceff3")), (1.0, color("#b3bac6"))), angle=0))
    layer.fill(body, barrel)
    flat = capsule((cx + width * 0.3, top + width * 0.9), (cx + width * 0.3, body_bottom), width * 0.04)
    layer.fill(flat, color("#9aa3b2"), 0.35)
    layer.fill(circle(cx, top + length - width * 0.02, width * 0.07), color("#59616f"))
    return layer


def compose(model: TabletModel, fin: Finish, wallpaper_key: str) -> Image.Image:
    """The hero picture: back panel peeking out behind the screen, Pencil leaning on the front."""
    front = draw_front(model, fin, wallpaper_key)
    back = draw_back(model, fin)
    width, height = front.width - 2 * SPRITE_MARGIN, front.height - 2 * SPRITE_MARGIN
    shift_x, shift_y = BACK_OFFSET_X * width, BACK_OFFSET_Y * height
    total_w, total_h = width + shift_x, height + shift_y
    left = (CANVAS - total_w) / 2
    top = (CANVAS - total_h) / 2 - 10
    scene = Layer(CANVAS, CANVAS)
    floor = top + total_h + 16
    draw_ground_shadow(scene, left + shift_x + width / 2, floor, width * 1.05, 38, 0.26)
    scene.paste(back, left - SPRITE_MARGIN, top - SPRITE_MARGIN)
    front_x, front_y = left + shift_x, top + shift_y
    outline = rounded_rect((front_x, front_y, front_x + width, front_y + height), _radius(model, (width, height)), 3.0)
    scene.shadow(outline, blur=14, offset=(-6, 14), opacity=0.34)
    scene.paste(front, front_x - SPRITE_MARGIN, front_y - SPRITE_MARGIN)
    if model.pencil:
        _lean_pencil(scene, front_x + width * (1 - PENCIL_INSET), floor - 4)
    return scene.output((CANVAS, CANVAS))


def _lean_pencil(scene: Layer, tip_x: float, tip_y: float) -> None:
    """Places a rotated Pencil so that its tip rests on the floor at (tip_x, tip_y)."""
    pencil = draw_pencil()
    length = pencil.height - 2 * SPRITE_MARGIN
    turned = pencil.rotated(PENCIL_LEAN)
    angle = math.radians(PENCIL_LEAN)
    center_x = tip_x - (length / 2) * math.sin(angle)
    center_y = tip_y - (length / 2) * math.cos(angle)
    # The sprite margin is symmetric, so the sprite center is the center of the pencil.
    shadow = Layer(turned.width, turned.height)
    scene.shadow(_pencil_footprint(tip_x, tip_y, length, angle), blur=6, offset=(8, 4), opacity=0.25)
    scene.paste_centered(turned, center_x, center_y)


def _pencil_footprint(tip_x: float, tip_y: float, length: float, angle: float) -> Shape:
    """A slim silhouette of the leaning pencil, used for its soft shadow."""
    top = (tip_x - length * math.sin(angle), tip_y - length * math.cos(angle))
    return capsule(top, (tip_x, tip_y), PENCIL_WIDTH_MM * LANDSCAPE_PX_PER_MM / 2)
