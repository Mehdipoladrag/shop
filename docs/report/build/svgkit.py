"""Tiny SVG toolkit for the report diagrams (RTL Persian labels, rendered to PNG by Chromium)."""
from html import escape

NAVY_900, NAVY_800, NAVY_700, NAVY_600, NAVY_500 = "#0f1f44", "#172d5c", "#1f3a6e", "#2b4d8f", "#3f66b0"
NAVY_300, NAVY_200, NAVY_100, NAVY_50 = "#9db4de", "#c7d4ec", "#e3eaf6", "#f3f6fb"
CORAL, CORAL_50, GREEN, GREEN_BG, AMBER_BG, RED, RED_BG = "#ff6b4a", "#fff1ed", "#1d6b2f", "#dff2bf", "#fff3cd", "#b42318", "#fdecec"
INK, MUTED = "#14213d", "#566686"
CHAR_WIDTH = 0.56  # average glyph width as a fraction of the font size (Persian text)


def text_width(value, size):
    return len(value) * size * CHAR_WIDTH


class Svg:
    def __init__(self, width, height, background="#ffffff"):
        self.width, self.height, self.parts, self.background = width, height, [], background

    def add(self, markup):
        self.parts.append(markup)

    def rect(self, x, y, w, h, fill="#ffffff", stroke=NAVY_700, sw=2, rx=14, dash=None, opacity=1):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash_attr} opacity="{opacity}"/>')

    def ellipse(self, cx, cy, rx, ry, fill="#ffffff", stroke=NAVY_700, sw=2, dash=None):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash_attr}/>')

    def diamond(self, cx, cy, w, h, fill=CORAL_50, stroke=CORAL, sw=2):
        points = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
        self.add(f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def circle(self, cx, cy, r, fill=NAVY_700, stroke=None, sw=2):
        stroke_attr = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{stroke_attr}/>')

    def text(self, x, y, value, size=22, fill=INK, weight=400, anchor="middle", latin=False):
        family = "Vazirmatn UI FD, Arial, sans-serif"
        # The page is right-to-left, so SVG's start/end anchors are mirrored: callers say what they see
        # ("end" = the text ends at x, on the right), this swaps them.
        anchor = {"start": "end", "end": "start"}.get(anchor, anchor)
        self.add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" '
                 f'font-family="{family}" style="unicode-bidi:plaintext">{escape(value)}</text>')

    def lines(self, x, y, values, size=22, fill=INK, weight=400, anchor="middle", gap=1.55, latin=False):
        """Several text lines, vertically centred around y."""
        step = size * gap
        top = y - step * (len(values) - 1) / 2
        for index, value in enumerate(values):
            self.text(x, top + index * step + size * 0.35, value, size, fill, weight, anchor, latin)

    def box(self, x, y, w, h, title, subtitle=None, fill=NAVY_50, stroke=NAVY_700, size=22, title_fill=NAVY_900, latin=False, dash=None, sw=2):
        self.rect(x, y, w, h, fill, stroke, sw=sw, dash=dash)
        if subtitle:
            sub = subtitle if isinstance(subtitle, list) else [subtitle]
            self.text(x + w / 2, y + h * 0.36, title, size, title_fill, 700, latin=latin)
            self.lines(x + w / 2, y + h * 0.36 + size * 1.45 + (len(sub) - 1) * size * 0.5, sub, size - 4, MUTED, 400, latin=latin)
        else:
            self.text(x + w / 2, y + h / 2 + size * 0.35, title, size, title_fill, 700, latin=latin)

    def line(self, x1, y1, x2, y2, stroke=NAVY_600, sw=2.5, dash=None):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{dash_attr}/>')

    def arrow(self, points, label=None, stroke=NAVY_600, sw=2.5, dash=None, both=False, size=19, label_at=0.5, label_fill=INK, latin=False, offset=(0, -14)):
        """Polyline with an arrowhead at the end (and the start when `both`)."""
        coords = " ".join(f"{px},{py}" for px, py in points)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        start = ' marker-start="url(#arrow-start)"' if both else ""
        self.add(f'<polyline points="{coords}" fill="none" stroke="{stroke}" stroke-width="{sw}"{dash_attr} marker-end="url(#arrow-end)"{start}/>')
        if label:
            (x1, y1), (x2, y2) = points[0], points[-1]
            lx, ly = x1 + (x2 - x1) * label_at + offset[0], y1 + (y2 - y1) * label_at + offset[1]
            width = text_width(label, size) + 16
            self.rect(lx - width / 2, ly - size * 0.95, width, size * 1.55, fill="#ffffff", stroke="none", sw=0, rx=6, opacity=0.92)
            self.text(lx, ly + size * 0.2, label, size, label_fill, 400, latin=latin)

    def save(self, path):
        defs = (f'<defs><marker id="arrow-end" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">'
                f'<path d="M1,1 L11,6 L1,11 z" fill="{NAVY_600}"/></marker>'
                f'<marker id="arrow-start" viewBox="0 0 12 12" refX="2" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">'
                f'<path d="M11,1 L1,6 L11,11 z" fill="{NAVY_600}"/></marker></defs>')
        body = "".join(self.parts)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" direction="rtl">'
               f'{defs}<rect width="100%" height="100%" fill="{self.background}"/>{body}</svg>')
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(svg)


def sequence(title_unused, participants, messages, width=1600, top=60, row=62, latin_participants=()):
    """UML-like sequence diagram. participants: [name]; messages: (from, to, label, kind) with kind call|return|self|note."""
    count = len(participants)
    margin = 150
    gap = (width - 2 * margin) / (count - 1)
    xs = [width - margin - index * gap for index in range(count)]  # first participant on the right (RTL)
    height = top + 110 + row * len(messages) + 80
    svg = Svg(width, height)
    for index, name in enumerate(participants):
        latin = index in latin_participants
        box_w = min(gap - 30, 270)
        svg.rect(xs[index] - box_w / 2, top - 50, box_w, 70, NAVY_700, NAVY_700, rx=14)
        svg.text(xs[index], top - 50 + 43, name, 21, "#ffffff", 700, latin=latin)
        svg.line(xs[index], top + 20, xs[index], height - 40, NAVY_300, 2, "8 8")
    y = top + 75
    for number, (src, dst, label, kind) in enumerate(messages, start=1):
        if kind == "self":
            x = xs[src]
            svg.arrow([(x, y - 10), (x - 70, y - 10), (x - 70, y + 24), (x, y + 24)], None, NAVY_500, 2.5)
            width_label = text_width(label, 19)
            svg.text(x - 82 - width_label / 2, y + 10, f"{number}. {label}", 19, INK)
        elif kind == "note":
            x = (xs[src] + xs[dst]) / 2
            w = abs(xs[src] - xs[dst]) + 150
            svg.rect(x - w / 2, y - 22, w, 46, CORAL_50, CORAL, 1.5, rx=10)
            svg.text(x, y + 8, label, 19, INK)
        else:
            dash = "9 6" if kind == "return" else None
            direction = 1 if xs[dst] > xs[src] else -1
            svg.arrow([(xs[src], y), (xs[dst], y)], None, NAVY_600 if kind == "call" else MUTED, 2.5, dash)
            mid = (xs[src] + xs[dst]) / 2
            tw = text_width(f"{number}. {label}", 19) + 14
            svg.rect(mid - tw / 2, y - 31, tw, 27, "#ffffff", "none", 0, rx=5, opacity=0.95)
            svg.text(mid, y - 11, f"{number}. {label}", 19, INK if kind == "call" else MUTED)
        y += row
    return svg
