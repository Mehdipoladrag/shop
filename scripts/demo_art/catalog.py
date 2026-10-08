"""The list of pictures this project generates: one entry per product color, plus category tiles."""

from __future__ import annotations

import zlib
from dataclasses import dataclass
from typing import Callable

from PIL import Image

from . import audio, categories, phones, tablets
from .parts import WALLPAPER_ORDER

PHONE_PICTURES = [
    ("iphone-17-pro-max", "cosmic-orange"), ("iphone-17-pro-max", "deep-blue"), ("iphone-17-pro-max", "silver"),
    ("iphone-17-pro", "silver"), ("iphone-17-pro", "deep-blue"),
    ("iphone-air", "sky-blue"), ("iphone-air", "space-black"),
    ("iphone-17", "lavender"), ("iphone-17", "black"), ("iphone-17", "mist-blue"),
    ("iphone-16e", "black"), ("iphone-16e", "white"),
    ("iphone-16-pro-max", "desert-titanium"),
    ("iphone-16-pro", "natural-titanium"), ("iphone-16-pro", "white-titanium"),
    ("iphone-16-plus", "ultramarine"),
    ("iphone-16", "pink"), ("iphone-16", "teal"),
    ("iphone-15-pro-max", "natural-titanium"), ("iphone-15-pro-max", "blue-titanium"),
    ("iphone-15-pro", "black-titanium"),
    ("iphone-15-plus", "green"),
    ("iphone-15", "blue"),
    ("galaxy-s25-ultra", "titanium-silverblue"), ("galaxy-s25-ultra", "titanium-black"),
    ("galaxy-s24-ultra", "titanium-gray"),
]
TABLET_PICTURES = [
    ("ipad-pro-13", "space-black"), ("ipad-pro-13", "silver"),
    ("ipad-pro-11", "silver"), ("ipad-pro-11", "space-black"),
    ("ipad-air-11", "blue"), ("ipad-air-11", "purple"),
    ("ipad-mini", "starlight"), ("ipad-mini", "blue"),
    ("ipad", "yellow"), ("ipad", "pink"),
]
EARBUD_PICTURES = ["airpods-pro-3", "airpods-pro-2", "airpods-4", "airpods-4-anc"]
MAX_PICTURES = ["midnight", "orange", "blue"]

# Hero illustrations used inside the category tiles.
CATEGORY_HEROES = {
    "category-mobile": lambda: phones.compose_pair(phones.MODELS["iphone-17-pro-max"], phones.FINISHES["cosmic-orange"], "ocean"),
    "category-tablet": lambda: tablets.compose(tablets.MODELS["ipad-pro-13"], tablets.FINISHES["silver"], "ocean"),
    "category-audio": lambda: audio.compose_earbuds("airpods-pro-2"),
}


@dataclass(frozen=True)
class Artwork:
    """A picture to render: its file name (without extension) and the function that draws it."""

    name: str
    render: Callable[[], Image.Image]


def _wallpaper_for(name: str) -> str:
    """A stable wallpaper per picture, so that regenerating never changes the artwork."""
    return WALLPAPER_ORDER[zlib.crc32(name.encode()) % len(WALLPAPER_ORDER)]


def _phone(model: str, finish: str) -> Artwork:
    name = f"{model}-{finish}"
    return Artwork(name, lambda: phones.compose_pair(phones.MODELS[model], phones.FINISHES[finish], _wallpaper_for(name)))


def _tablet(model: str, finish: str) -> Artwork:
    name = f"{model}-{finish}"
    return Artwork(name, lambda: tablets.compose(tablets.MODELS[model], tablets.FINISHES[finish], _wallpaper_for(name)))


def _category(name: str) -> Artwork:
    return Artwork(name, lambda: categories.category_picture(CATEGORY_HEROES[name]()))


def all_artworks() -> list[Artwork]:
    """Every picture in a stable order: products first, category tiles last."""
    artworks = [_phone(model, finish) for model, finish in PHONE_PICTURES]
    artworks += [_tablet(model, finish) for model, finish in TABLET_PICTURES]
    artworks += [Artwork(key, lambda key=key: audio.compose_earbuds(key)) for key in EARBUD_PICTURES]
    artworks += [Artwork(f"airpods-max-{key}", lambda key=key: audio.compose_max(key)) for key in MAX_PICTURES]
    artworks += [_category(name) for name in CATEGORY_HEROES]
    return artworks
