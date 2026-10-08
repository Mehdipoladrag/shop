"""Smartphone illustrations: the back of one phone overlapped by the front of a second one."""

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
    draw_glass_lens,
    draw_ground_shadow,
    draw_island,
    draw_lens,
    draw_lidar,
    draw_notch,
    draw_punch_hole,
    draw_wallpaper,
    finish,
    sheen,
)
from .toolkit import (
    Layer,
    Linear,
    Shape,
    capsule,
    circle,
    color,
    darken,
    lighten,
    mix,
    polygon,
    rounded_rect,
)

CANVAS = 900
PX_PER_MM = 4.5
SPRITE_MARGIN = 46  # transparent border around a phone sprite, room for its shadow
FRONT_SCALE = 0.94  # the front phone is drawn a little smaller than the back one
FRONT_OVERLAP = 0.80  # horizontal offset of the front phone, as a fraction of the back phone width
FRONT_DROP = 0.07  # vertical offset of the front phone, as a fraction of the back phone height
GROUND_MARGIN = 58  # free space kept below the phones for the floor shadow
S_PEN_LENGTH_MM = 108.0
S_PEN_WIDTH_MM = 5.8
S_PEN_LEAN = 11.0  # degrees the S Pen leans towards the phone
S_PEN_INSET = 0.04  # distance of its tip from the front phone's right edge, as a fraction of the phone width
SEAM = 0.9  # width of the dark hairline between rail and face
BAR_RIM = 1.6  # bright rim around a full width camera bar, in px


@dataclass(frozen=True)
class PhoneModel:
    """Real world proportions and design cues of one phone."""

    width_mm: float
    height_mm: float
    camera: str  # key of CAMERA_LAYOUTS
    corner: float = 0.15  # corner radius as a fraction of the width
    squareness: float = 3.4  # corner shape: 2 is a circle, larger values are squarer
    rail: float = 2.6  # side rail thickness in px
    bezel: float = 4.6  # screen bezel in px
    front: str = "island"  # "island", "notch" or "punch"
    camera_control: bool = False  # the extra capture button of the iPhone 16 and 17 families
    action_button: bool = True


# --------------------------------------------------------------------------- camera layouts
# Each layout draws the camera module in the top left corner of the back.  Positions are given
# as fractions of the phone width `u`; (ox, oy) is the top left corner of the back.


def _plate(layer: Layer, box: tuple, radius: float, fin: Finish, squareness: float = 3.0) -> Shape:
    """A raised camera plateau with a bright rim and a soft shadow on the back."""
    outer = rounded_rect(box, radius, squareness)
    layer.shadow(outer, blur=5, offset=(2.5, 5), opacity=0.34)
    layer.fill(outer, Linear.of(lighten(fin.module[0], 0.5), darken(fin.module[1], 0.28), angle=DIAGONAL))
    inset = 2.2
    inner_box = (box[0] + inset, box[1] + inset, box[2] - inset, box[3] - inset)
    inner = rounded_rect(inner_box, radius - inset, squareness)
    layer.fill(inner, Linear.of(fin.module[0], fin.module[1], angle=DIAGONAL + 10))
    return inner


def _bar(layer: Layer, box: tuple, radius: float, face: Shape, paints: tuple, rim: float, gloss: float) -> Shape:
    """A camera bar that runs to the edges of the back: bright rim, face paint and a soft reflection.

    `paints` holds the rim paint and the surface paint.  The bar is clipped to the back `face`,
    so its top corners follow the corners of the phone.
    """
    outer = rounded_rect(box, radius, 3.0).intersect(face)
    layer.shadow(outer, blur=5, offset=(0, 5), opacity=0.32)
    layer.fill(outer, paints[0])
    left, top, right, bottom = box
    inner = rounded_rect((left + rim * 2, top + rim * 2, right - rim * 2, bottom - rim), radius - rim, 3.0).intersect(face)
    layer.fill(inner, paints[1])
    sheen(layer, inner, gloss)
    return inner


def _lens_set(layer, ox, oy, u, fin, lenses, radius) -> None:
    for fx, fy in lenses:
        draw_lens(layer, ox + fx * u, oy + fy * u, radius * u, fin.ring)


def camera_diagonal(layer, ox, oy, u, fin, face):
    """iPhone 15 and 15 Plus: square plateau, two lenses on a diagonal."""
    _plate(layer, (ox + 0.05 * u, oy + 0.05 * u, ox + 0.53 * u, oy + 0.53 * u), 0.13 * u, fin)
    _lens_set(layer, ox, oy, u, fin, [(0.185, 0.185), (0.385, 0.385)], 0.1)
    draw_flash(layer, ox + 0.405 * u, oy + 0.165 * u, 0.03 * u, fin.ring)
    draw_dot(layer, ox + 0.165 * u, oy + 0.405 * u, 0.011 * u)


def camera_pill(layer, ox, oy, u, fin, face):
    """iPhone 16 and 16 Plus: vertical pill, two stacked lenses, flash beside it."""
    _plate(layer, (ox + 0.05 * u, oy + 0.05 * u, ox + 0.33 * u, oy + 0.54 * u), 0.14 * u, fin)
    _lens_set(layer, ox, oy, u, fin, [(0.19, 0.19), (0.19, 0.405)], 0.1)
    draw_flash(layer, ox + 0.455 * u, oy + 0.12 * u, 0.028 * u, fin.ring)
    draw_dot(layer, ox + 0.455 * u, oy + 0.205 * u, 0.011 * u)


def camera_triple(layer, ox, oy, u, fin, face):
    """iPhone 15/16 Pro: square plateau, three lenses, flash, LiDAR and microphone."""
    _plate(layer, (ox + 0.05 * u, oy + 0.05 * u, ox + 0.60 * u, oy + 0.60 * u), 0.135 * u, fin)
    _lens_set(layer, ox, oy, u, fin, [(0.195, 0.195), (0.195, 0.45), (0.44, 0.32)], 0.108)
    draw_flash(layer, ox + 0.48 * u, oy + 0.135 * u, 0.03 * u, fin.ring)
    draw_lidar(layer, ox + 0.48 * u, oy + 0.515 * u, 0.034 * u, fin.ring)
    draw_dot(layer, ox + 0.335 * u, oy + 0.12 * u, 0.011 * u)


def camera_single(layer, ox, oy, u, fin, face):
    """iPhone 16e: a single lens in a glass ring, flash to its right."""
    halo = circle(ox + 0.185 * u, oy + 0.185 * u, 0.15 * u)
    layer.shadow(halo, blur=4, offset=(2, 4), opacity=0.3)
    layer.fill(halo, Linear.of(lighten(fin.module[0], 0.45), darken(fin.module[1], 0.25), angle=DIAGONAL))
    layer.fill(circle(ox + 0.185 * u, oy + 0.185 * u, 0.138 * u), Linear.of(fin.module[0], fin.module[1], angle=DIAGONAL + 10))
    _lens_set(layer, ox, oy, u, fin, [(0.185, 0.185)], 0.105)
    draw_flash(layer, ox + 0.42 * u, oy + 0.135 * u, 0.028 * u, fin.ring)
    draw_dot(layer, ox + 0.42 * u, oy + 0.225 * u, 0.011 * u)


def camera_air(layer, ox, oy, u, fin, face):
    """iPhone Air: a bar across the whole top edge with one lens and the flash on its right."""
    paints = (Linear.of(lighten(fin.module[0], 0.35), darken(fin.module[1], 0.3), angle=DIAGONAL),
              Linear.of(fin.module[0], fin.module[1], angle=DIAGONAL + 10))
    _bar(layer, (ox, oy, ox + u, oy + 0.3 * u), 0.05 * u, face, paints, BAR_RIM, 0.18)
    layer.fill(circle(ox + 0.215 * u, oy + 0.15 * u, 0.12 * u), Linear.of(darken(fin.module[1], 0.35), fin.module[0], angle=DIAGONAL), 0.35)
    _lens_set(layer, ox, oy, u, fin, [(0.215, 0.15)], 0.098)
    draw_flash(layer, ox + 0.79 * u, oy + 0.1 * u, 0.026 * u, fin.ring)
    draw_dot(layer, ox + 0.9 * u, oy + 0.17 * u, 0.011 * u)


def camera_bar(layer, ox, oy, u, fin, face):
    """iPhone 17: a horizontal pill plateau with two lenses side by side."""
    _plate(layer, (ox + 0.05 * u, oy + 0.05 * u, ox + 0.95 * u, oy + 0.37 * u), 0.16 * u, fin)
    _lens_set(layer, ox, oy, u, fin, [(0.215, 0.21), (0.5, 0.21)], 0.105)
    draw_flash(layer, ox + 0.775 * u, oy + 0.15 * u, 0.03 * u, fin.ring)
    draw_dot(layer, ox + 0.84 * u, oy + 0.275 * u, 0.011 * u)


def camera_wide(layer, ox, oy, u, fin, face):
    """iPhone 17 Pro and Pro Max: an aluminium plateau across the whole back with three lenses."""
    paints = (Linear.of(lighten(fin.frame[0], 0.2), darken(fin.frame[1], 0.2), angle=DIAGONAL),
              Linear.of(fin.frame[0], mix(fin.frame[0], fin.frame[1], 0.8), angle=DIAGONAL + 10))
    _bar(layer, (ox, oy, ox + u, oy + 0.66 * u), 0.07 * u, face, paints, BAR_RIM, 0.12)
    _lens_set(layer, ox, oy, u, fin, [(0.2, 0.2), (0.2, 0.46), (0.45, 0.33)], 0.112)
    draw_flash(layer, ox + 0.73 * u, oy + 0.16 * u, 0.032 * u, fin.ring)
    draw_lidar(layer, ox + 0.73 * u, oy + 0.5 * u, 0.034 * u, fin.ring)
    draw_dot(layer, ox + 0.86 * u, oy + 0.33 * u, 0.012 * u)


def camera_ultra(layer, ox, oy, u, fin, face):
    """Galaxy Ultra: separate lenses without a plateau, three in a vertical stack."""
    column = 0.16
    for fy in (0.105, 0.272, 0.439):
        draw_glass_lens(layer, ox + column * u, oy + fy * u, 0.07 * u, fin.ring)
    draw_glass_lens(layer, ox + 0.33 * u, oy + 0.356 * u, 0.058 * u, fin.ring)
    draw_flash(layer, ox + 0.33 * u, oy + 0.1 * u, 0.02 * u, fin.ring)
    draw_dot(layer, ox + 0.33 * u, oy + 0.185 * u, 0.011 * u)


CAMERA_LAYOUTS = {
    "diagonal": camera_diagonal,
    "pill": camera_pill,
    "triple": camera_triple,
    "single": camera_single,
    "air": camera_air,
    "bar": camera_bar,
    "wide": camera_wide,
    "ultra": camera_ultra,
}

# --------------------------------------------------------------------------- models (sizes in mm)

MODELS = {
    "iphone-15": PhoneModel(71.6, 147.6, "diagonal"),
    "iphone-15-plus": PhoneModel(77.8, 160.9, "diagonal"),
    "iphone-15-pro": PhoneModel(70.6, 146.6, "triple", corner=0.14, bezel=3.6),
    "iphone-15-pro-max": PhoneModel(76.7, 159.9, "triple", corner=0.14, bezel=3.6),
    "iphone-16": PhoneModel(71.6, 147.6, "pill", camera_control=True),
    "iphone-16-plus": PhoneModel(77.8, 160.9, "pill", camera_control=True),
    "iphone-16-pro": PhoneModel(71.5, 149.6, "triple", corner=0.14, bezel=3.4, camera_control=True),
    "iphone-16-pro-max": PhoneModel(77.6, 163.0, "triple", corner=0.14, bezel=3.4, camera_control=True),
    "iphone-16e": PhoneModel(71.5, 146.7, "single", front="notch", camera_control=False),
    "iphone-17": PhoneModel(71.5, 149.6, "bar", camera_control=True, bezel=3.8),
    "iphone-air": PhoneModel(74.7, 156.2, "air", corner=0.16, rail=3.0, bezel=3.4, camera_control=True),
    "iphone-17-pro": PhoneModel(71.9, 150.0, "wide", corner=0.14, bezel=3.4, camera_control=True),
    "iphone-17-pro-max": PhoneModel(78.0, 163.4, "wide", corner=0.14, bezel=3.4, camera_control=True),
    "galaxy-s24-ultra": PhoneModel(79.0, 162.3, "ultra", corner=0.075, squareness=5.0, rail=3.0, bezel=3.8, front="punch", action_button=False),
    "galaxy-s25-ultra": PhoneModel(77.6, 162.8, "ultra", corner=0.11, squareness=4.0, rail=3.0, bezel=3.2, front="punch", action_button=False),
}

# --------------------------------------------------------------------------- finishes
# Illustrative colors chosen to look like the real devices; they are not official swatches.

FINISHES = {
    "blue": finish("#cddbe5", "#9fb6c7", "#e0e9ef", "#8ea5b7"),
    "pink": finish("#f4dedc", "#dcb9b7", "#f8e9e7", "#cfaaa8"),
    "green": finish("#d4e1d0", "#aac0a7", "#e3ece0", "#9bb198"),
    "black": finish("#4d5056", "#2a2c31", "#6d7178", "#1f2125"),
    "white": finish("#f7f7f6", "#dadbde", "#ffffff", "#c8c9cd"),
    "ultramarine": finish("#8597f2", "#5668cc", "#9dacf5", "#4859b8"),
    "teal": finish("#a8d6d2", "#6fabA7", "#bfe3df", "#5f9792"),
    "lavender": finish("#d4c8e7", "#a99dca", "#e3dbf1", "#9b8fbe"),
    "mist-blue": finish("#bed4e5", "#8faec9", "#d1e1ed", "#7f9fbb"),
    "natural-titanium": finish("#bfb8ac", "#8e877b", "#d7d1c6", "#7b7469"),
    "blue-titanium": finish("#5b667c", "#343e51", "#77849b", "#262f3f"),
    "white-titanium": finish("#e8e6e1", "#c0bdb6", "#f5f3ef", "#aaa7a1"),
    "black-titanium": finish("#46484c", "#27282b", "#66686d", "#1b1c1e"),
    "desert-titanium": finish("#d8bea3", "#b4936f", "#e8d4be", "#a08260"),
    "cosmic-orange": finish("#ec8a40", "#cf6420", "#f5a460", "#bb5416", "#f09a52", "#d96f26"),
    "deep-blue": finish("#3c5486", "#233965", "#5b74a7", "#1a2b50", "#496299", "#2b4478"),
    "silver": finish("#eaebee", "#c5c8ce", "#f6f7f9", "#adb1b9"),
    "sky-blue": finish("#c6dcef", "#98b9d5", "#a8c2dc", "#6e8eaf", "#a3bed9", "#7b9bbd"),
    "space-black": finish("#3b3d42", "#212226", "#54565c", "#17181b", "#2c2e32", "#18191c"),
    "light-gold": finish("#f0e1c7", "#d3be97", "#e5d3af", "#b9a275", "#ddcba2", "#c1a97c"),
    "titanium-gray": finish("#a5a6ac", "#7b7c82", "#bfc0c5", "#6a6b70"),
    "titanium-black": finish("#37393d", "#1e1f22", "#585a5f", "#141517"),
    "titanium-silverblue": finish("#b5c3d5", "#8598b1", "#cbd6e4", "#74869f"),
}

# --------------------------------------------------------------------------- drawing


def _geometry(model: PhoneModel, scale: float) -> tuple[float, float]:
    return model.width_mm * PX_PER_MM * scale, model.height_mm * PX_PER_MM * scale


def _buttons(layer: Layer, box: tuple, model: PhoneModel, fin: Finish) -> None:
    """Side keys, drawn first so that only the part that sticks out of the rail is visible."""
    left, top, right, bottom = box
    height = bottom - top
    sticks_out = 2.6
    paint = Linear.of(fin.frame[0], fin.frame[1], angle=0)

    def key(x: float, from_y: float, to_y: float, outward: int):
        inner = x - outward * 2.0
        outer = x + outward * sticks_out
        shape = rounded_rect((min(inner, outer), top + from_y * height, max(inner, outer), top + to_y * height), 1.3)
        layer.fill(shape, paint)

    if model.front == "punch":  # Galaxy: volume and power keys on the right
        key(right, 0.2, 0.275, 1)
        key(right, 0.3, 0.42, 1)
        return
    if model.action_button:
        key(left, 0.113, 0.141, -1)
    key(left, 0.175, 0.245, -1)
    key(left, 0.265, 0.335, -1)
    key(right, 0.23, 0.33, 1)
    if model.camera_control:
        key(right, 0.6, 0.66, 1)


def _rail(layer: Layer, outer: Shape, fin: Finish) -> None:
    """The metal side rail: a lit top left edge fading into a darker bottom right."""
    layer.fill(outer, Linear.of(fin.frame[0], fin.frame[1], angle=DIAGONAL))
    stops = ((0.0, color("#ffffff", 210)), (0.3, color("#ffffff", 0)), (0.72, color("#000000", 0)), (1.0, color("#000000", 80)))
    layer.fill(outer, Linear(stops, angle=DIAGONAL))


def _seam(layer: Layer, box: tuple, radius: float, inset: float, squareness: float) -> Shape:
    """Returns the face shape and first draws the hairline gap that separates it from the rail."""
    gap = rounded_rect((box[0] + inset - SEAM, box[1] + inset - SEAM, box[2] - inset + SEAM, box[3] - inset + SEAM), radius - inset + SEAM, squareness)
    layer.fill(gap, color("#000000", 70))
    return rounded_rect((box[0] + inset, box[1] + inset, box[2] - inset, box[3] - inset), radius - inset, squareness)


def draw_back(model: PhoneModel, fin: Finish, scale: float = 1.0) -> Layer:
    """The back of a phone with its camera module, on a transparent sprite with a shadow margin."""
    width, height = _geometry(model, scale)
    layer = Layer(width + 2 * SPRITE_MARGIN, height + 2 * SPRITE_MARGIN)
    box = (SPRITE_MARGIN, SPRITE_MARGIN, SPRITE_MARGIN + width, SPRITE_MARGIN + height)
    radius = model.corner * width
    _buttons(layer, box, model, fin)
    outer = rounded_rect(box, radius, model.squareness)
    _rail(layer, outer, fin)
    face = _seam(layer, box, radius, model.rail, model.squareness)
    layer.fill(face, Linear.of(fin.back[0], fin.back[1], angle=DIAGONAL + 12))
    sheen(layer, face, 0.16)
    CAMERA_LAYOUTS[model.camera](layer, box[0], box[1], width, fin, face)
    return layer


def _draw_front_screen(layer: Layer, box: tuple, model: PhoneModel, scale: float, wallpaper_key: str) -> None:
    left, top, right, bottom = box
    inset = model.rail + model.bezel * scale
    screen_box = (left + inset, top + inset, right - inset, bottom - inset)
    radius = model.corner * (right - left) - inset * 0.85
    screen = rounded_rect(screen_box, radius, model.squareness)
    draw_wallpaper(layer, screen, screen_box, WALLPAPERS[wallpaper_key])
    center = (left + right) / 2
    screen_width = screen_box[2] - screen_box[0]
    top_edge = screen_box[1]
    if model.front == "island":
        draw_island(layer, center, top_edge + screen_width * 0.035, screen_width * 0.3, screen_width * 0.082)
    elif model.front == "notch":
        draw_notch(layer, center, top_edge, screen_width * 0.46, screen_width * 0.075, screen)
    else:
        draw_punch_hole(layer, center, top_edge + screen_width * 0.045, screen_width * 0.026)


def draw_front(model: PhoneModel, fin: Finish, wallpaper_key: str, scale: float = 1.0) -> Layer:
    """The front of a phone: rail, black glass, wallpaper and camera cut-out."""
    width, height = _geometry(model, scale)
    layer = Layer(width + 2 * SPRITE_MARGIN, height + 2 * SPRITE_MARGIN)
    box = (SPRITE_MARGIN, SPRITE_MARGIN, SPRITE_MARGIN + width, SPRITE_MARGIN + height)
    radius = model.corner * width
    _buttons(layer, box, model, fin)
    outer = rounded_rect(box, radius, model.squareness)
    _rail(layer, outer, fin)
    glass = _seam(layer, box, radius, model.rail, model.squareness)
    layer.fill(glass, Linear.of(color("#10131c"), GLASS_BLACK, angle=DIAGONAL))
    _draw_front_screen(layer, box, model, scale, wallpaper_key)
    return layer


def draw_s_pen() -> Layer:
    """The S Pen standing on its tip: black body, silver cap and a side button."""
    length, width = S_PEN_LENGTH_MM * PX_PER_MM, S_PEN_WIDTH_MM * PX_PER_MM
    layer = Layer(width + 2 * SPRITE_MARGIN, length + 2 * SPRITE_MARGIN)
    cx, top = layer.width / 2, SPRITE_MARGIN
    tip_length = length * 0.1
    body_bottom = top + length - tip_length
    barrel = Linear(((0.0, color("#5b5f69")), (0.3, color("#22242b")), (1.0, color("#050507"))), angle=0)
    body = capsule((cx, top + width / 2), (cx, body_bottom), width / 2)
    cone = polygon([(cx - width / 2, body_bottom), (cx + width / 2, body_bottom), (cx + width * 0.08, top + length), (cx - width * 0.08, top + length)])
    layer.fill(cone, Linear(((0.0, color("#4a4e58")), (1.0, color("#050507"))), angle=0))
    layer.fill(body, barrel)
    cap = capsule((cx, top + width / 2), (cx, top + length * 0.07), width / 2)
    layer.fill(cap, Linear(((0.0, color("#f2f3f6")), (0.5, color("#aeb3bd")), (1.0, color("#6c727e"))), angle=0), clip=body)
    layer.fill(rounded_rect((cx - width * 0.62, top + length * 0.2, cx - width * 0.2, top + length * 0.27), width * 0.18), color("#8a909c"))
    layer.fill(circle(cx, top + length - width * 0.03, width * 0.09), color("#9aa1ae"))
    return layer


def _lean_s_pen(scene: Layer, tip_x: float, tip_y: float) -> None:
    pen = draw_s_pen()
    length = pen.height - 2 * SPRITE_MARGIN
    angle = math.radians(S_PEN_LEAN)
    top = (tip_x - length * math.sin(angle), tip_y - length * math.cos(angle))
    scene.shadow(capsule(top, (tip_x, tip_y), S_PEN_WIDTH_MM * PX_PER_MM / 2), blur=6, offset=(8, 4), opacity=0.28)
    center_x = tip_x - (length / 2) * math.sin(angle)
    center_y = tip_y - (length / 2) * math.cos(angle)
    scene.paste_centered(pen.rotated(S_PEN_LEAN), center_x, center_y)


def compose_pair(model: PhoneModel, fin: Finish, wallpaper_key: str) -> Image.Image:
    """The hero picture: a large back view overlapped by the front of the same phone."""
    back = draw_back(model, fin)
    front = draw_front(model, fin, wallpaper_key, FRONT_SCALE)
    back_w, back_h = back.width - 2 * SPRITE_MARGIN, back.height - 2 * SPRITE_MARGIN
    front_w, front_h = front.width - 2 * SPRITE_MARGIN, front.height - 2 * SPRITE_MARGIN
    front_dx = FRONT_OVERLAP * back_w
    front_dy = FRONT_DROP * back_h
    total_w = front_dx + front_w
    total_h = max(back_h, front_dy + front_h)
    left = (CANVAS - total_w) / 2
    top = (CANVAS - GROUND_MARGIN / 2 - total_h) / 2
    scene = Layer(CANVAS, CANVAS)
    floor = top + total_h + 14
    draw_ground_shadow(scene, left + back_w / 2, floor - 10, back_w * 1.1, 34, 0.22)
    scene.paste(back, left - SPRITE_MARGIN, top - SPRITE_MARGIN)
    front_x = left + front_dx
    front_y = top + front_dy
    draw_ground_shadow(scene, front_x + front_w / 2, floor, front_w * 1.15, 38, 0.26)
    front_box = rounded_rect((front_x, front_y, front_x + front_w, front_y + front_h), model.corner * front_w, model.squareness)
    scene.shadow(front_box, blur=13, offset=(-6, 14), opacity=0.34)
    scene.paste(front, front_x - SPRITE_MARGIN, front_y - SPRITE_MARGIN)
    if model.camera == "ultra":
        _lean_s_pen(scene, front_x + front_w * (1 - S_PEN_INSET), floor - 6)
    return scene.output((CANVAS, CANVAS))
