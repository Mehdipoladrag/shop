"""Audio illustrations: AirPods charging cases with floating earbuds, and the AirPods Max."""

from __future__ import annotations

import math
from dataclasses import dataclass

from PIL import Image

from .parts import DIAGONAL, Finish, draw_ground_shadow, finish
from .toolkit import (
    WHITE,
    Layer,
    Linear,
    Radial,
    arc_band,
    capsule,
    circle,
    color,
    darken,
    ellipse,
    lighten,
    rotated_ellipse,
    rounded_rect,
)

CANVAS = 900
SPRITE_MARGIN = 40
BUD_SCALE = 1.4  # earbuds are drawn larger than life so that they stay readable next to the case
CASE_SCALE = 1.12
PLASTIC = (color("#ffffff"), color("#eceff4"), color("#c2c8d3"))
SHADE_OVERLAY = ((0.0, color("#ffffff", 150)), (0.35, color("#ffffff", 0)), (0.72, color("#0b1630", 0)), (1.0, color("#0b1630", 46)))


@dataclass(frozen=True)
class EarbudStyle:
    """Shape differences between the earbud generations (sizes in px at scale 1)."""

    head: tuple[float, float]  # half width and half height of the head
    stem_length: float
    stem_radius: tuple[float, float]  # radius at the head and at the tip of the stem
    tip: str | None  # "silicone", "foam" or None for the open-ear design
    extra_mics: bool = False
    sensor: bool = False  # the heart rate sensor of the third generation Pro


@dataclass(frozen=True)
class CaseStyle:
    width: float
    height: float
    corner: float  # radius as a fraction of the height
    seam: float  # lid seam position as a fraction of the height
    loop: bool  # lanyard loop on the side
    speaker: bool = False  # a speaker grille on the front (Find My)


PRO_BUD = EarbudStyle((50, 45), 160, (19, 13.5), "silicone")
PRO3_BUD = EarbudStyle((50, 45), 150, (19, 13.5), "foam", sensor=True)
OPEN_BUD = EarbudStyle((52, 47), 120, (17, 12.5), None)
OPEN_ANC_BUD = EarbudStyle((52, 47), 120, (17, 12.5), None, extra_mics=True)

PRO_CASE = CaseStyle(390, 292, 0.34, 0.3, loop=True)
PRO3_CASE = CaseStyle(380, 290, 0.35, 0.3, loop=True, speaker=True)
OPEN_CASE = CaseStyle(330, 288, 0.32, 0.3, loop=False)
OPEN_ANC_CASE = CaseStyle(330, 288, 0.32, 0.3, loop=False, speaker=True)

MODELS = {
    "airpods-pro-2": (PRO_BUD, PRO_CASE),
    "airpods-pro-3": (PRO3_BUD, PRO3_CASE),
    "airpods-4": (OPEN_BUD, OPEN_CASE),
    "airpods-4-anc": (OPEN_ANC_BUD, OPEN_ANC_CASE),
}


# --------------------------------------------------------------------------- earbud


def _tip(layer: Layer, ox: float, oy: float, s: float, style: EarbudStyle) -> None:
    """The ear tip that sticks out on the inner side of the head."""
    cx, cy = ox - 54 * s, oy - 2 * s
    shape = rotated_ellipse(cx, cy, 31 * s, 27 * s, -10)
    paint = Linear.of(color("#f6f7fa"), color("#c3c9d3"), angle=DIAGONAL)
    layer.shadow(shape, blur=4 * s, offset=(2 * s, 4 * s), opacity=0.22)
    layer.fill(shape, paint)
    layer.fill(rotated_ellipse(cx - 10 * s, cy - 9 * s, 12 * s, 6 * s, -35), WHITE, 0.7)
    if style.tip == "foam":
        for dx, dy in ((-8, -4), (6, 9), (-2, 12), (10, -8), (-14, 6), (2, -14)):
            layer.fill(circle(cx + dx * s, cy + dy * s, 1.7 * s), color("#a9b1bf"), 0.7)
    mesh = rotated_ellipse(cx - 24 * s, cy, 6 * s, 14 * s, -10)
    layer.fill(mesh, Radial.of(color("#4b5260"), color("#242831")))


def draw_earbud(style: EarbudStyle, scale: float = 1.0) -> Layer:
    """One right earbud, upright, with its tip pointing left."""
    s = scale
    size = 340 * s
    layer = Layer(size, size)
    ox, oy = size * 0.55, size * 0.34
    rx, ry = style.head[0] * s, style.head[1] * s
    if style.tip:
        _tip(layer, ox, oy, s, style)
    head = ellipse((ox - rx, oy - ry, ox + rx, oy + ry))
    stem = capsule((ox + 12 * s, oy + 8 * s), (ox + 20 * s, oy + style.stem_length * s), style.stem_radius[0] * s, style.stem_radius[1] * s)
    body = head.union(stem).smoothed(6 * s)
    layer.shadow(body, blur=7 * s, offset=(5 * s, 10 * s), opacity=0.24)
    layer.fill(body, Radial.of(*PLASTIC, center=(0.36, 0.2), radius=0.95))
    layer.fill(body, Linear(SHADE_OVERLAY, angle=DIAGONAL))
    layer.fill(rotated_ellipse(ox - rx * 0.32, oy - ry * 0.42, rx * 0.3, ry * 0.14, -32), WHITE, 0.85, clip=body)
    _bud_details(layer, ox, oy, s, style)
    return layer


def _bud_details(layer: Layer, ox: float, oy: float, s: float, style: EarbudStyle) -> None:
    ink = color("#4a5160")
    layer.fill(circle(ox + 22 * s, oy - 28 * s, 3.2 * s), ink, 0.8)
    layer.fill(circle(ox + 20 * s + style.stem_length * 0.03 * s, oy + (style.stem_length - 12) * s, 3.4 * s), ink, 0.85)
    sensor = capsule((ox + 17 * s, oy + 52 * s), (ox + 18.5 * s, oy + 84 * s), 2.2 * s)
    layer.fill(sensor, color("#9aa3b2"), 0.5)
    if style.tip is None:  # open-ear speaker grille on the inner side
        center = (ox - 30 * s, oy + 6 * s)
        layer.fill(rotated_ellipse(*center, 7 * s, 10 * s, 12), Radial.of(color("#7a8294"), color("#4a505c")))
        layer.fill(rotated_ellipse(*center, 4.6 * s, 7.4 * s, 12), Radial.of(color("#383d48"), color("#596071"), radius=0.7))
    if style.extra_mics:
        layer.fill(circle(ox + 4 * s, oy - 36 * s, 2.6 * s), ink, 0.8)
    if style.sensor:
        layer.fill(circle(ox - 30 * s, oy + 22 * s, 6 * s), Radial.of(color("#6b7280"), color("#272a33")))


# --------------------------------------------------------------------------- case


def draw_case(style: CaseStyle, scale: float = 1.0) -> Layer:
    """The closed charging case seen from the front."""
    s = scale
    width, height = style.width * s, style.height * s
    layer = Layer(width + 2 * SPRITE_MARGIN, height + 2 * SPRITE_MARGIN)
    box = (SPRITE_MARGIN, SPRITE_MARGIN, SPRITE_MARGIN + width, SPRITE_MARGIN + height)
    body = rounded_rect(box, style.corner * height, 2.6)
    layer.shadow(body, blur=12 * s, offset=(8 * s, 16 * s), opacity=0.28)
    layer.fill(body, Linear(((0.0, color("#ffffff")), (0.55, color("#eef0f4")), (1.0, color("#c9cfda"))), angle=DIAGONAL + 15))
    layer.fill(body, Linear(SHADE_OVERLAY, angle=DIAGONAL))
    seam_y = box[1] + style.seam * height
    layer.fill(capsule((box[0], seam_y), (box[2], seam_y), 1.3 * s), color("#8d96a6"), 0.55, clip=body)
    layer.fill(capsule((box[0], seam_y + 2.4 * s), (box[2], seam_y + 2.4 * s), 1.1 * s), WHITE, 0.8, clip=body)
    layer.fill(rotated_ellipse(box[0] + width * 0.2, box[1] + height * 0.14, width * 0.13, height * 0.045, -18), WHITE, 0.8, clip=body)
    center_x = (box[0] + box[2]) / 2
    layer.fill(circle(center_x, box[1] + height * 0.56, 5 * s), Radial.of(color("#cfd4dd"), color("#8c95a5"), radius=0.6))
    if style.speaker:
        for index in range(5):
            layer.fill(circle(box[2] - width * 0.18 - index * 9 * s, box[3] - height * 0.16, 2.1 * s), color("#8d96a6"), 0.8)
    if style.loop:
        hole = capsule((box[2] - 2 * s, box[1] + height * 0.52), (box[2] - 2 * s, box[1] + height * 0.72), 5 * s)
        layer.fill(hole, color("#7c8596"), 0.55, clip=body)
    return layer


def compose_earbuds(key: str) -> Image.Image:
    """Charging case on the left with the two earbuds floating next to it."""
    bud_style, case_style = MODELS[key]
    case = draw_case(case_style, CASE_SCALE)
    bud = draw_earbud(bud_style, BUD_SCALE)
    scene = Layer(CANVAS, CANVAS)
    case_cx, case_cy = 318, 610
    floor = case_cy + case_style.height * CASE_SCALE / 2 + 28
    draw_ground_shadow(scene, case_cx + 10, floor, case_style.width * CASE_SCALE * 1.05, 42, 0.26)
    scene.paste_centered(case, case_cx, case_cy)
    right_bud = bud.rotated(-12)
    left_bud = bud.flipped().rotated(12)
    scene.paste_centered(left_bud, 630, 400)
    scene.paste_centered(right_bud, 742, 580)
    return scene.output((CANVAS, CANVAS))


# --------------------------------------------------------------------------- AirPods Max

MAX_FINISHES = {
    "midnight": finish("#555964", "#2a2c34", "#767b87", "#1d1e24"),
    "starlight": finish("#f1eee6", "#cfcabe", "#faf8f2", "#b8b3a6"),
    "blue": finish("#a9c3dd", "#7c9bbc", "#c1d4e8", "#6c8bad"),
    "orange": finish("#f4a560", "#d97e2e", "#f8bb85", "#c2691f"),
}
STEEL = (color("#f6f7f9"), color("#b7bcc6"), color("#7f8794"))
CUP_SIZE = (172, 292)
CUP_CENTERS = (222, 678)
CUP_CENTER_Y = 612
BAND_TOP = 292  # y of the top of the headband arch


def compose_max(finish_key: str) -> Image.Image:
    """AirPods Max seen from the front: steel arms, knit canopy, aluminium cups and cushions."""
    fin = MAX_FINISHES[finish_key]
    scene = Layer(CANVAS, CANVAS)
    draw_ground_shadow(scene, 450, CUP_CENTER_Y + CUP_SIZE[1] / 2 + 26, 640, 46, 0.26)
    _band(scene, fin)
    for index, cx in enumerate(CUP_CENTERS):
        _cup(scene, cx, fin, inner_side=1 if index == 0 else -1)
    _crown(scene, CUP_CENTERS[1] - 34, fin)
    return scene.output((CANVAS, CANVAS))


def _band(scene: Layer, fin: Finish) -> None:
    radius_y = CUP_CENTER_Y - BAND_TOP
    box = (CUP_CENTERS[0], BAND_TOP, CUP_CENTERS[1], BAND_TOP + 2 * radius_y)
    steel = Linear(((0.0, STEEL[0]), (0.4, STEEL[1]), (1.0, STEEL[2])), angle=DIAGONAL)
    arms = arc_band(box, 180, 360, 17)
    scene.shadow(arms, blur=5, offset=(2, 6), opacity=0.25)
    scene.fill(arms, steel)
    scene.fill(arc_band((box[0] - 4, box[1] - 4, box[2] + 4, box[3] + 4), 190, 350, 3), WHITE, 0.55)
    canopy = arc_band(box, 224, 316, 46)
    scene.shadow(canopy, blur=7, offset=(0, 7), opacity=0.3)
    scene.fill(canopy, Linear.of(darken(fin.back[0], 0.3), darken(fin.back[1], 0.5), angle=DIAGONAL))
    scene.fill(arc_band((box[0] - 12, box[1] - 12, box[2] + 12, box[3] + 12), 232, 290, 4), WHITE, 0.22)


def _cup(scene: Layer, cx: float, fin: Finish, inner_side: int) -> None:
    half_w, half_h = CUP_SIZE[0] / 2, CUP_SIZE[1] / 2
    box = (cx - half_w, CUP_CENTER_Y - half_h, cx + half_w, CUP_CENTER_Y + half_h)
    cushion_x = cx + inner_side * (half_w - 26)
    cushion = rounded_rect((cushion_x - 34, box[1] + 24, cushion_x + 34, box[3] - 24), 34)
    yoke = rounded_rect((cx - 18, box[1] - 26, cx + 18, box[1] + 30), 8)
    scene.fill(yoke, Linear.of(STEEL[0], STEEL[2], angle=0))
    outer = rounded_rect(box, 86, 2.4)
    scene.shadow(outer, blur=12, offset=(8, 16), opacity=0.3)
    scene.fill(cushion, Linear.of(darken(fin.back[1], 0.55), darken(fin.back[1], 0.8), angle=DIAGONAL))
    scene.fill(outer, Linear.of(lighten(fin.frame[0], 0.2), fin.frame[1], angle=DIAGONAL))
    face = rounded_rect((box[0] + 5, box[1] + 5, box[2] - 5, box[3] - 5), 81, 2.4)
    scene.fill(face, Linear.of(fin.back[0], fin.back[1], angle=DIAGONAL + 10))
    scene.fill(face, Linear(SHADE_OVERLAY, angle=DIAGONAL), 0.9)
    streak = capsule((cx - half_w * 0.62, box[1] + 70), (cx - half_w * 0.62, box[3] - 90), 4.5)
    scene.fill(streak, WHITE, 0.4, clip=face)
    scene.fill(circle(cx, CUP_CENTER_Y + 30, 4.5), darken(fin.back[1], 0.5), 0.8)


def _crown(scene: Layer, cx: float, fin: Finish) -> None:
    """The Digital Crown on top of the right cup."""
    top = CUP_CENTER_Y - CUP_SIZE[1] / 2 - 26
    crown = rounded_rect((cx - 21, top - 18, cx + 21, top + 6), 6)
    scene.fill(crown, Linear.of(fin.frame[0], fin.frame[1], angle=0))
    for offset in range(-15, 16, 6):
        scene.fill(capsule((cx + offset, top - 16), (cx + offset, top + 4), 0.8), color("#000000"), 0.22)
