"""Small drawing toolkit on top of Pillow: gradients, anti-aliased shapes, shadows and layers.

Every coordinate and size in this module is expressed in *output pixels* (floats are fine).
Layers are painted at SUPERSAMPLE times the output size and shapes are rasterised at an
even higher factor, so the final downscale gives smooth edges without any numpy dependency.
"""

from __future__ import annotations

import io
import math
from dataclasses import dataclass

from PIL import Image, ImageChops, ImageDraw, ImageFilter

SUPERSAMPLE = 3  # layers are painted at 3x the output size
MASK_SUPERSAMPLE = 2  # shape masks are rasterised at 2x the layer size, then averaged
MASK_PADDING = 2  # extra pixels around a shape mask (layer pixels)
CORNER_STEPS = 40  # polygon points used for one rounded corner
ELLIPSE_STEPS = 96  # polygon points used for a rotated ellipse
MAX_LEVEL = 255  # highest value of an 8-bit channel
RAMP_MARGIN = 1  # keeps gradient sampling inside the 256 px source ramp
SMOOTH_GAIN = 5.0  # steepness of the threshold used by Shape.smoothed

Color = tuple[int, int, int, int]

WHITE: Color = (255, 255, 255, 255)
BLACK: Color = (0, 0, 0, 255)
CLEAR: Color = (0, 0, 0, 0)
SHADOW_INK: Color = (9, 22, 48, 255)  # navy ink used for every shadow


def color(value: str, alpha: int = MAX_LEVEL) -> Color:
    """Converts '#rrggbb' to an RGBA tuple."""
    value = value.lstrip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha)


def mix(first: Color, second: Color, amount: float) -> Color:
    """Linear blend: amount 0 gives `first`, amount 1 gives `second`."""
    return tuple(round(a + (b - a) * amount) for a, b in zip(first, second))  # type: ignore[return-value]


def lighten(value: Color, amount: float) -> Color:
    return mix(value, (255, 255, 255, value[3]), amount)


def darken(value: Color, amount: float) -> Color:
    return mix(value, (0, 0, 0, value[3]), amount)


def with_alpha(value: Color, opacity: float) -> Color:
    return (value[0], value[1], value[2], round(value[3] * opacity))


# --------------------------------------------------------------------------- paints


@dataclass(frozen=True)
class Linear:
    """Linear gradient. `angle` is in degrees clockwise from +x: 90 runs top to bottom, 45 runs
    from the top-left corner to the bottom-right corner (the light comes from the top left)."""

    stops: tuple
    angle: float = 90.0

    @classmethod
    def of(cls, *colors: Color, angle: float = 90.0) -> "Linear":
        last = max(len(colors) - 1, 1)
        return cls(tuple((index / last, value) for index, value in enumerate(colors)), angle)


@dataclass(frozen=True)
class Radial:
    """Radial gradient; `center` is a fraction of the box, `radius` a fraction of its larger side."""

    stops: tuple
    center: tuple = (0.5, 0.5)
    radius: float = 0.5

    @classmethod
    def of(cls, *colors: Color, center: tuple = (0.5, 0.5), radius: float = 0.5) -> "Radial":
        last = max(len(colors) - 1, 1)
        return cls(tuple((index / last, value) for index, value in enumerate(colors)), center, radius)


Paint = Color | Linear | Radial


def _sample(stops: tuple, position: float) -> Color:
    if position <= stops[0][0]:
        return stops[0][1]
    for (left_at, left), (right_at, right) in zip(stops, stops[1:]):
        if position <= right_at:
            span = max(right_at - left_at, 1e-9)
            return mix(left, right, (position - left_at) / span)
    return stops[-1][1]


def _colorize(levels: Image.Image, stops: tuple) -> Image.Image:
    """Maps an 'L' image through the gradient stops to an RGBA image."""
    tables = [[0] * (MAX_LEVEL + 1) for _ in range(4)]
    for level in range(MAX_LEVEL + 1):
        sampled = _sample(stops, level / MAX_LEVEL)
        for channel in range(4):
            tables[channel][level] = sampled[channel]
    return Image.merge("RGBA", [levels.point(table) for table in tables])


def _linear_levels(size: tuple[int, int], angle: float) -> Image.Image:
    width, height = size
    radians = math.radians(angle)
    dx, dy = math.cos(radians), math.sin(radians)
    projections = [x * dx + y * dy for x in (0, width) for y in (0, height)]
    low = min(projections)
    span = max(max(projections) - low, 1e-6)
    scale = (MAX_LEVEL - 1 - 2 * RAMP_MARGIN) / span
    coefficients = (0, 0, 128, dx * scale, dy * scale, RAMP_MARGIN - low * scale)
    ramp = Image.linear_gradient("L")
    return ramp.transform(size, Image.Transform.AFFINE, coefficients, resample=Image.Resampling.BILINEAR)


# Image.radial_gradient reaches white only in the corners of its square; this table stretches
# it so that the inscribed circle (radius 128 px) is already white.
RADIAL_EDGE_LEVEL = MAX_LEVEL / math.sqrt(2)


def _radial_source() -> Image.Image:
    stretch = [min(MAX_LEVEL, round(level * MAX_LEVEL / RADIAL_EDGE_LEVEL)) for level in range(MAX_LEVEL + 1)]
    return Image.radial_gradient("L").point(stretch)


def _radial_levels(size: tuple[int, int], center: tuple, radius: float) -> Image.Image:
    width, height = size
    diameter = max(2, round(2 * radius * max(width, height)))
    disc = _radial_source().resize((diameter, diameter), Image.Resampling.BILINEAR)
    levels = Image.new("L", size, MAX_LEVEL)
    levels.paste(disc, (round(center[0] * width - diameter / 2), round(center[1] * height - diameter / 2)))
    return levels


def render_paint(paint: Paint, size: tuple[int, int]) -> Image.Image:
    """Renders a solid color or gradient into an RGBA image of `size` pixels."""
    if isinstance(paint, Linear):
        return _colorize(_linear_levels(size, paint.angle), paint.stops)
    if isinstance(paint, Radial):
        return _colorize(_radial_levels(size, paint.center, paint.radius), paint.stops)
    return Image.new("RGBA", size, paint)


# --------------------------------------------------------------------------- shapes


@dataclass
class Shape:
    """An anti-aliased 'L' mask placed at (x, y) in layer pixels."""

    mask: Image.Image
    x: int
    y: int

    @property
    def size(self) -> tuple[int, int]:
        return self.mask.size

    def intersect(self, other: "Shape") -> "Shape":
        """The part of this shape that lies inside `other`."""
        window = Image.new("L", self.mask.size, 0)
        window.paste(other.mask, (other.x - self.x, other.y - self.y))
        return Shape(ImageChops.multiply(self.mask, window), self.x, self.y)

    def moved(self, dx: float, dy: float) -> "Shape":
        return Shape(self.mask, self.x + round(dx * SUPERSAMPLE), self.y + round(dy * SUPERSAMPLE))

    def union(self, other: "Shape") -> "Shape":
        """This shape and `other` merged into one silhouette."""
        left, top = min(self.x, other.x), min(self.y, other.y)
        right = max(self.x + self.mask.width, other.x + other.mask.width)
        bottom = max(self.y + self.mask.height, other.y + other.mask.height)
        first = Image.new("L", (right - left, bottom - top), 0)
        second = Image.new("L", first.size, 0)
        first.paste(self.mask, (self.x - left, self.y - top))
        second.paste(other.mask, (other.x - left, other.y - top))
        return Shape(ImageChops.lighter(first, second), left, top)

    def smoothed(self, radius: float) -> "Shape":
        """Rounds off sharp corners (also concave ones) by blurring and re-thresholding the mask."""
        pad = math.ceil(radius * SUPERSAMPLE * 3)
        padded = Image.new("L", (self.mask.width + 2 * pad, self.mask.height + 2 * pad), 0)
        padded.paste(self.mask, (pad, pad))
        blurred = padded.filter(ImageFilter.GaussianBlur(radius * SUPERSAMPLE))
        crisp = blurred.point([max(0, min(MAX_LEVEL, round((level - 128) * SMOOTH_GAIN + 128))) for level in range(MAX_LEVEL + 1)])
        return Shape(crisp, self.x - pad, self.y - pad)


def _rasterise(bounds: tuple[float, float, float, float], draw_shape) -> Shape:
    """Builds a Shape; `draw_shape(draw, to_mask)` paints white on a high resolution mask."""
    left = math.floor(bounds[0] * SUPERSAMPLE) - MASK_PADDING
    top = math.floor(bounds[1] * SUPERSAMPLE) - MASK_PADDING
    right = math.ceil(bounds[2] * SUPERSAMPLE) + MASK_PADDING
    bottom = math.ceil(bounds[3] * SUPERSAMPLE) + MASK_PADDING
    size = (right - left, bottom - top)
    mask = Image.new("L", (size[0] * MASK_SUPERSAMPLE, size[1] * MASK_SUPERSAMPLE), 0)

    def to_mask(x: float, y: float) -> tuple[float, float]:
        return ((x * SUPERSAMPLE - left) * MASK_SUPERSAMPLE, (y * SUPERSAMPLE - top) * MASK_SUPERSAMPLE)

    draw_shape(ImageDraw.Draw(mask), to_mask)
    return Shape(mask.resize(size, Image.Resampling.BOX), left, top)


def _corner_points(cx: float, cy: float, radius: float, sign_x: int, sign_y: int, squareness: float):
    """Points of one superellipse corner (squareness 2 is a circle, larger is squarer)."""
    exponent = 2.0 / squareness
    points = []
    for step in range(CORNER_STEPS + 1):
        angle = (math.pi / 2) * step / CORNER_STEPS
        points.append((
            cx + sign_x * radius * math.cos(angle) ** exponent,
            cy + sign_y * radius * math.sin(angle) ** exponent,
        ))
    return points


def rounded_outline(box: tuple[float, float, float, float], radius: float, squareness: float = 2.0):
    """Polygon points of a rounded rectangle with (super)elliptic corners."""
    left, top, right, bottom = box
    radius = max(0.0, min(radius, (right - left) / 2, (bottom - top) / 2))
    if radius == 0:
        return [(left, top), (right, top), (right, bottom), (left, bottom)]
    corners = [
        (right - radius, top + radius, 1, -1),
        (right - radius, bottom - radius, 1, 1),
        (left + radius, bottom - radius, -1, 1),
        (left + radius, top + radius, -1, -1),
    ]
    points = []
    for index, (cx, cy, sign_x, sign_y) in enumerate(corners):
        corner = _corner_points(cx, cy, radius, sign_x, sign_y, squareness)
        # Corners are generated from the side point to the top/bottom point, so every other
        # corner is walked backwards to keep the clockwise outline continuous.
        points.extend(list(reversed(corner)) if index % 2 == 0 else corner)
    return points


def rounded_rect(box, radius: float, squareness: float = 2.0) -> Shape:
    points = rounded_outline(box, radius, squareness)
    return _rasterise(box, lambda draw, to_mask: draw.polygon([to_mask(*p) for p in points], fill=MAX_LEVEL))


def ellipse(box) -> Shape:
    return _rasterise(box, lambda draw, to_mask: draw.ellipse([*to_mask(box[0], box[1]), *to_mask(box[2], box[3])], fill=MAX_LEVEL))


def circle(cx: float, cy: float, radius: float) -> Shape:
    return ellipse((cx - radius, cy - radius, cx + radius, cy + radius))


def polygon(points) -> Shape:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return _rasterise((min(xs), min(ys), max(xs), max(ys)),
                      lambda draw, to_mask: draw.polygon([to_mask(*p) for p in points], fill=MAX_LEVEL))


def rotated_ellipse(cx: float, cy: float, rx: float, ry: float, degrees: float = 0.0) -> Shape:
    """Ellipse centered at (cx, cy) with radii rx and ry, turned clockwise by `degrees`."""
    radians = math.radians(degrees)
    cos, sin = math.cos(radians), math.sin(radians)
    points = []
    for step in range(ELLIPSE_STEPS):
        angle = 2 * math.pi * step / ELLIPSE_STEPS
        x, y = rx * math.cos(angle), ry * math.sin(angle)
        points.append((cx + x * cos - y * sin, cy + x * sin + y * cos))
    return polygon(points)


def capsule(start: tuple, end: tuple, start_radius: float, end_radius: float | None = None) -> Shape:
    """Rounded bar between two points; the radii may differ to taper it."""
    end_radius = start_radius if end_radius is None else end_radius
    pad = max(start_radius, end_radius)
    bounds = (min(start[0], end[0]) - pad, min(start[1], end[1]) - pad,
              max(start[0], end[0]) + pad, max(start[1], end[1]) + pad)
    angle = math.atan2(end[1] - start[1], end[0] - start[0]) + math.pi / 2
    nx, ny = math.cos(angle), math.sin(angle)

    def paint(draw, to_mask):
        quad = [
            to_mask(start[0] + nx * start_radius, start[1] + ny * start_radius),
            to_mask(end[0] + nx * end_radius, end[1] + ny * end_radius),
            to_mask(end[0] - nx * end_radius, end[1] - ny * end_radius),
            to_mask(start[0] - nx * start_radius, start[1] - ny * start_radius),
        ]
        draw.polygon(quad, fill=MAX_LEVEL)
        for (cx, cy), r in ((start, start_radius), (end, end_radius)):
            draw.ellipse([*to_mask(cx - r, cy - r), *to_mask(cx + r, cy + r)], fill=MAX_LEVEL)

    return _rasterise(bounds, paint)


def arc_band(box, start_angle: float, end_angle: float, width: float) -> Shape:
    """A curved stroke along the ellipse inscribed in `box`; angles in degrees clockwise from +x."""
    pad = width
    bounds = (box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad)

    def paint(draw, to_mask):
        draw.arc([*to_mask(box[0], box[1]), *to_mask(box[2], box[3])], start_angle, end_angle,
                 fill=MAX_LEVEL, width=max(1, round(width * SUPERSAMPLE * MASK_SUPERSAMPLE)))

    return _rasterise(bounds, paint)


def bezier(points: list[tuple[float, float]], steps: int = 24) -> list[tuple[float, float]]:
    """Samples a cubic Bezier curve given its four control points."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = points
    sampled = []
    for step in range(steps + 1):
        t = step / steps
        u = 1 - t
        sampled.append((
            u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
            u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3,
        ))
    return sampled


# --------------------------------------------------------------------------- layers


class Layer:
    """A transparent RGBA surface with a supersampled backing image."""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.image = Image.new("RGBA", (round(width * SUPERSAMPLE), round(height * SUPERSAMPLE)), CLEAR)

    def _blit(self, source: Image.Image, x: int, y: int) -> None:
        """Alpha-composites `source` at (x, y), cropping whatever falls outside the layer."""
        left, top = max(0, -x), max(0, -y)
        right = min(source.width, self.image.width - x)
        bottom = min(source.height, self.image.height - y)
        if right <= left or bottom <= top:
            return
        self.image.alpha_composite(source.crop((left, top, right, bottom)), dest=(x + left, y + top))

    def fill(self, shape: Shape, paint: Paint, opacity: float = 1.0, clip: Shape | None = None) -> None:
        """Fills `shape` (optionally restricted to `clip`) with a color or gradient."""
        shape = shape if clip is None else shape.intersect(clip)
        source = render_paint(paint, shape.size)
        alpha = ImageChops.multiply(source.getchannel("A"), shape.mask)
        if opacity < 1.0:
            alpha = alpha.point(lambda value: round(value * opacity))
        source.putalpha(alpha)
        self._blit(source, shape.x, shape.y)

    def shadow(self, shape: Shape, blur: float, offset: tuple = (0, 0), opacity: float = 0.3,
               ink: Color = SHADOW_INK, clip: Shape | None = None) -> None:
        """Soft shadow of a silhouette; `blur` is the Gaussian sigma in output pixels."""
        pad = math.ceil(blur * SUPERSAMPLE * 3)
        mask = Image.new("L", (shape.mask.width + 2 * pad, shape.mask.height + 2 * pad), 0)
        mask.paste(shape.mask, (pad, pad))
        mask = mask.filter(ImageFilter.GaussianBlur(blur * SUPERSAMPLE))
        blurred = Shape(mask, shape.x - pad + round(offset[0] * SUPERSAMPLE), shape.y - pad + round(offset[1] * SUPERSAMPLE))
        self.fill(blurred, ink, opacity, clip)

    def paste(self, other: "Layer", x: float, y: float, opacity: float = 1.0) -> None:
        """Places another layer with its top-left corner at (x, y)."""
        source = other.image
        if opacity < 1.0:
            source = source.copy()
            source.putalpha(source.getchannel("A").point(lambda value: round(value * opacity)))
        self._blit(source, round(x * SUPERSAMPLE), round(y * SUPERSAMPLE))

    def rotated(self, degrees: float) -> "Layer":
        """A copy rotated counter-clockwise around its center on a larger transparent canvas."""
        turned = self.image.rotate(degrees, resample=Image.Resampling.BICUBIC, expand=True)
        result = Layer(turned.width / SUPERSAMPLE, turned.height / SUPERSAMPLE)
        result.image = turned
        return result

    def flipped(self) -> "Layer":
        """A mirrored copy (left becomes right)."""
        result = Layer(self.width, self.height)
        result.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        return result

    def paste_centered(self, other: "Layer", cx: float, cy: float, opacity: float = 1.0) -> None:
        self.paste(other, cx - other.width / 2, cy - other.height / 2, opacity)

    def output(self, size: tuple[int, int] | None = None) -> Image.Image:
        """The final image, averaged down from the supersampled backing store."""
        size = size or (round(self.width), round(self.height))
        return self.image.resize(size, Image.Resampling.LANCZOS)


def blurred_layer_fill(layer: Layer, shape: Shape, paint: Paint, blur: float, opacity: float = 1.0, clip: Shape | None = None) -> None:
    """Fills `shape` with a paint whose edges are softened; used for glows and wallpaper blobs."""
    pad = math.ceil(blur * SUPERSAMPLE * 3)
    mask = Image.new("L", (shape.mask.width + 2 * pad, shape.mask.height + 2 * pad), 0)
    mask.paste(shape.mask, (pad, pad))
    soft = Shape(mask.filter(ImageFilter.GaussianBlur(blur * SUPERSAMPLE)), shape.x - pad, shape.y - pad)
    layer.fill(soft, paint, opacity, clip)


# --------------------------------------------------------------------------- output


SIZE_BUDGET = 120 * 1024  # target maximum size of a PNG file in bytes
COLOR_STEPS = (1, 2, 3, 4, 5, 6, 8)  # allowed color precision, finest first (1 keeps all 256 levels)
ALPHA_STEP_LIMIT = 2  # transparency never gets coarser than this, soft shadows would show bands


def _precision_table(step: int) -> list[int]:
    """Lookup table that rounds a channel to a multiple of `step`, keeping pure white exact."""
    snap = MAX_LEVEL - step / 2
    return [MAX_LEVEL if level >= snap else min(MAX_LEVEL, round(level / step) * step) for level in range(MAX_LEVEL + 1)]


def _reduced(image: Image.Image, step: int) -> Image.Image:
    """The picture with coarser color precision (alpha is reduced less) so that it compresses better."""
    red, green, blue, alpha = image.split()
    color_table = _precision_table(step)
    alpha_table = _precision_table(min(step, ALPHA_STEP_LIMIT))
    return Image.merge("RGBA", [red.point(color_table), green.point(color_table), blue.point(color_table), alpha.point(alpha_table)])


def encode_png(image: Image.Image, budget: int = SIZE_BUDGET) -> tuple[bytes, int]:
    """Encodes an optimised PNG; returns the bytes and the color step that was needed.

    Smooth gradients are expensive in a truecolor PNG, so the color precision is lowered step by
    step until the file fits the budget.  Most pictures need a step of only 2 or 3 (about 7 bits
    per channel), which is not visible in the gradients.
    """
    best = (b"", 0)
    for step in COLOR_STEPS:
        buffer = io.BytesIO()
        _reduced(image, step).save(buffer, format="PNG", optimize=True)
        data = buffer.getvalue()
        if not best[0] or len(data) < len(best[0]):
            best = (data, step)
        if len(data) <= budget:
            break
    return best


def save_png(image: Image.Image, path, budget: int = SIZE_BUDGET) -> int:
    """Writes an optimised PNG with a transparent background and returns its size in bytes."""
    data, _ = encode_png(image, budget)
    path.write_bytes(data)
    return len(data)
