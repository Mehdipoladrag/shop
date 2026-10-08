#!/usr/bin/env python3
"""Generates the original illustrations used by the demo catalog (seed_demo_catalog).

The pictures are drawn with code (Pillow only, no photographs, no network access): phones,
tablets and AirPods with a transparent background, plus the three category tiles.  The drawing
is fully deterministic, so running the script twice produces byte-identical files.

Usage:
    python scripts/generate_demo_art.py                       # writes every picture
    python scripts/generate_demo_art.py --only iphone-15-blue # writes selected pictures
    python scripts/generate_demo_art.py --contact-sheet /tmp/sheet.png

A real photograph can replace any generated file: keep the file name and the seed picks it up.
"""

from __future__ import annotations

import argparse
import sys
from multiprocessing import Pool
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from demo_art.catalog import all_artworks  # noqa: E402
from demo_art.toolkit import save_png  # noqa: E402

DEFAULT_OUTPUT = REPO_ROOT / "shop" / "static" / "assets" / "img" / "product_img" / "new"
SIZE_BUDGET = 120 * 1024  # bytes; a larger picture is reported as a warning
SHEET_COLUMNS = 6
SHEET_CELL = 280
SHEET_CAPTION = 26
SHEET_BACKGROUND = (238, 243, 250)
SHEET_INK = (31, 58, 110)


def render(job: tuple[str, str]) -> tuple[str, int]:
    """Draws one picture and returns its name and file size (runs in a worker process)."""
    name, output = job
    artwork = next(item for item in all_artworks() if item.name == name)
    target = Path(output) / f"{name}.png"
    return name, save_png(artwork.render(), target)


def contact_sheet(directory: Path, names: list[str], destination: Path) -> None:
    """One overview PNG with every picture in a grid, for a quick visual review."""
    rows = -(-len(names) // SHEET_COLUMNS)
    cell_height = SHEET_CELL + SHEET_CAPTION
    sheet = Image.new("RGB", (SHEET_COLUMNS * SHEET_CELL, rows * cell_height), SHEET_BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=13)
    for index, name in enumerate(names):
        picture = Image.open(directory / f"{name}.png").convert("RGBA")
        picture.thumbnail((SHEET_CELL, SHEET_CELL), Image.Resampling.LANCZOS)
        x, y = (index % SHEET_COLUMNS) * SHEET_CELL, (index // SHEET_COLUMNS) * cell_height
        sheet.paste(picture, (x + (SHEET_CELL - picture.width) // 2, y), picture)
        draw.text((x + 8, y + SHEET_CELL + 4), name, fill=SHEET_INK, font=font)
    destination.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(destination)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the demo catalog illustrations.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="folder for the PNG files")
    parser.add_argument("--only", nargs="+", metavar="NAME", help="draw only these pictures (file names without .png)")
    parser.add_argument("--jobs", type=int, default=0, help="worker processes (default: one per CPU)")
    parser.add_argument("--contact-sheet", type=Path, help="also write an overview image of all pictures")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    names = [artwork.name for artwork in all_artworks()]
    if arguments.only:
        unknown = sorted(set(arguments.only) - set(names))
        if unknown:
            print(f"Unknown picture names: {', '.join(unknown)}", file=sys.stderr)
            return 2
        names = [name for name in names if name in arguments.only]
    arguments.output.mkdir(parents=True, exist_ok=True)
    jobs = [(name, str(arguments.output)) for name in names]
    with Pool(arguments.jobs or None) as pool:
        results = dict(pool.imap_unordered(render, jobs))
    oversize = 0
    for name in names:
        size = results[name]
        flag = "" if size <= SIZE_BUDGET else "  <-- over budget"
        oversize += bool(flag)
        print(f"{name + '.png':52} {size / 1024:7.1f} KB{flag}")
    print(f"{len(names)} pictures written to {arguments.output} ({oversize} over {SIZE_BUDGET // 1024} KB)")
    if arguments.contact_sheet:
        contact_sheet(arguments.output, names, arguments.contact_sheet)
        print(f"Contact sheet: {arguments.contact_sheet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
