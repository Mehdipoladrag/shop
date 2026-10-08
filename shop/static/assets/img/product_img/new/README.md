# Demo catalog pictures

These PNG files are **generated illustrations, not photographs**. They were drawn with code
(`scripts/generate_demo_art.py`, Pillow only) so that the demo shop has pictures of the 2023+
phones, tablets and AirPods without using copyrighted press photos. Real products can look
different: colors are approximate, logos are left out and the screens show an abstract wallpaper.

Every file has a transparent background, is about 900 x 900 px (the three `category-*.png` tiles are
600 x 600 px) and stays under 120 KB.

| Files | Content |
| ----- | ------- |
| `iphone-*`, `galaxy-*` | the back of a phone overlapped by the front of a second one (Galaxy Ultra models with an S Pen) |
| `ipad-*` | the screen with an Apple Pencil leaning on it and the back panel behind it |
| `airpods-pro-*`, `airpods-4*` | charging case with the two earbuds |
| `airpods-max-*` | AirPods Max headphones |
| `category-mobile.png`, `category-tablet.png`, `category-audio.png` | navy tiles for the home page categories |

The file name is `<model>-<color>.png`. `python manage.py seed_demo_catalog` copies the pictures to
`MEDIA_ROOT/images/demo-catalog/` and attaches them to the products.

## Regenerate

From the repository root:

```bash
python scripts/generate_demo_art.py                          # every picture
python scripts/generate_demo_art.py --only iphone-15-blue    # selected pictures
python scripts/generate_demo_art.py --contact-sheet sheet.png  # also writes an overview image
```

The drawing is deterministic: running the script again gives identical files. Models, colors and
proportions live in `scripts/demo_art/` (`phones.py`, `tablets.py`, `audio.py`, `catalog.py`).

## Use a real photo instead

Any file can be replaced by a real product photo: keep the same file name (for example
`iphone-17-pro-max-cosmic-orange.png`) and run the seed again on an empty catalog (or replace the
picture of an existing product in the admin panel). Make sure you own the rights to the photo.
