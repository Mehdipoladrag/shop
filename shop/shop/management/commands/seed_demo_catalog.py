"""Populate the shop with a demo catalog of phones, tablets and AirPods released in 2023 or later.

Model names and specifications follow the manufacturers' public information.  Prices, stock,
discounts, ratings and delivery times are sample data, and the pictures are original
illustrations drawn by scripts/generate_demo_art.py (they are not official product photos).

The command is idempotent (existing slugs are skipped) and atomic.  `--prune-old` additionally
removes the products created by the previous version of this seed; without it nothing is deleted.
"""

import shutil
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from shop.management.commands._demo_catalog_data import (
    APPLE,
    AUDIO,
    COLORS,
    MODELS,
    MOBILE,
    SAMSUNG,
    TABLET,
    VARIANTS,
)
from shop.models import Brand, Category, Info, Product

NOTICE = (
    "کاتالوگ نمایشی تک‌شاپ: نام مدل‌ها و مشخصات فنی بر پایهٔ اطلاعات عمومی سازندگان است. "
    "قیمت (به تومان)، موجودی، تخفیف، امتیاز و زمان ارسال دادهٔ نمونه هستند و پیشنهاد فروش واقعی نیستند. "
    "تصاویر، تصویرسازی هستند و عکس رسمی محصولات نیستند؛ رنگ‌ها نیز تقریبی‌اند. "
    "سیستم‌عامل ذکرشده مربوط به زمان عرضه است."
)

# Folder (below MEDIA_ROOT) that holds every picture copied by this seed.
DEMO_FOLDER = "images/demo-catalog"
# Illustrations drawn by scripts/generate_demo_art.py (below the static image folder).
ART_FOLDER = "product_img/new"
BRAND_FOLDER = "brands"

PRODUCT_CODE_BASE = 94000  # the previous seed used 93001-93016
DELIVERY_DAYS = (1, 2, 3)  # sample delivery times, handed out in turn
OFFER_RANGE = (0, 15)  # sample discounts stay between 0 and 15 percent

CATEGORIES = [
    (MOBILE, "گوشی موبایل", 91001),
    (TABLET, "تبلت", 91003),
    (AUDIO, "هدفون و ایرپاد", 91004),
]
# (name, code, picture in static/assets/img/brands, categories it sells in)
BRANDS = [
    (APPLE, 92001, "brand-3.jpg", (MOBILE, TABLET, AUDIO)),
    (SAMSUNG, 92002, "brand-8.jpg", (MOBILE,)),
]
BRAND_NAMES_FA = {APPLE: "اپل", SAMSUNG: "سامسونگ"}
STORAGE_LABELS = {128: "۱۲۸ گیگابایت", 256: "۲۵۶ گیگابایت", 512: "۵۱۲ گیگابایت", 1024: "۱ ترابایت", 2048: "۲ ترابایت"}
GIGABYTES_PER_TERABYTE = 1024

# Products created by the previous version of this seed (iPhone 12/13/14, Galaxy A52 and S21 Ultra,
# POCO X4 Pro and PlayStation 5).  Only `--prune-old` touches them.
LEGACY_SLUGS = (
    "apple-iphone-13-128-blue",
    "apple-iphone-13-256-blue",
    "apple-iphone-13-pro-256-silver",
    "apple-iphone-12-pro-256-graphite",
    "samsung-galaxy-a52-128-peach",
    "samsung-galaxy-s21-ultra-256-black",
    "poco-x4-pro-5g-256-black",
    "sony-playstation-5-disc-825",
    "apple-iphone-14-128-blue",
    "apple-iphone-14-plus-128-blue",
    "apple-iphone-14-pro-256-silver",
    "apple-iphone-14-pro-max-256-silver",
    "apple-iphone-13-pro-max-256-gold",
    "apple-iphone-13-mini-128-blue",
    "apple-iphone-12-pro-max-256-graphite",
    "apple-iphone-12-128-blue",
)


@dataclass(frozen=True)
class ProductSpec:
    """Everything needed to create one product."""

    slug: str
    name: str
    brand: str
    category: str
    color: str
    image: str  # file name of the illustration
    price: int
    offer: int
    stock: int
    rate: str
    camera: int
    os: str
    tech: str
    capability: str
    mini: str
    specs: str
    desc: str
    year: int


def _storage_slug(gigabytes):
    if gigabytes >= GIGABYTES_PER_TERABYTE:
        return f"{gigabytes // GIGABYTES_PER_TERABYTE}tb"
    return str(gigabytes)


def build_spec(variant):
    """Turns a model plus one variant (storage, color, commerce data) into a ProductSpec."""
    model = MODELS[variant.model]
    if model.storages and variant.storage not in model.storages:
        raise ValueError(f"{model.title} has no {variant.storage} GB version")
    if not model.storages and variant.storage is not None:
        raise ValueError(f"{model.title} has no storage")
    if not OFFER_RANGE[0] <= variant.offer <= OFFER_RANGE[1]:
        raise ValueError(f"offer of {model.title} is out of range")
    color = COLORS[variant.color]

    slug_parts = [model.key]
    name = f"{BRAND_NAMES_FA[model.brand]} {model.title}"
    lines = []
    if variant.storage:
        slug_parts.append(_storage_slug(variant.storage))
        name += f" ظرفیت {STORAGE_LABELS[variant.storage]}"
        lines.append(f"حافظه داخلی: {STORAGE_LABELS[variant.storage]}")
    image = model.art
    if model.has_colors:
        slug_parts.append(variant.color)
        image += f"-{variant.color}"
    lines += list(model.specs) + [f"رنگ: {color}"]
    return ProductSpec(
        slug="-".join(slug_parts),
        name=name,
        brand=model.brand,
        category=model.category,
        color=color,
        image=f"{image}.png",
        price=variant.price,
        offer=variant.offer,
        stock=variant.stock,
        rate=variant.rate,
        camera=model.camera,
        os=model.os,
        tech=f"{model.chip} / {model.network}",
        capability=model.capability,
        mini=model.mini,
        specs="\n".join(lines) + f"\n\nمنبع مشخصات سازنده: {model.source}",
        desc=model.desc,
        year=model.year,
    )


CATALOG = [build_spec(variant) for variant in VARIANTS]  # newest products first


def static_images():
    return Path(settings.BASE_DIR) / "static" / "assets" / "img"


def art_file(name):
    return static_images() / ART_FOLDER / name


def missing_assets():
    """Names of the bundled picture files that are needed but not present."""
    needed = {art_file(spec.image) for spec in CATALOG}
    needed |= {art_file(f"category-{slug}.png") for slug, _, _ in CATEGORIES}
    needed |= {static_images() / BRAND_FOLDER / picture for _, _, picture, _ in BRANDS}
    return sorted(str(path) for path in needed if not path.is_file())


def copy_picture(source, destination):
    """Copies a bundled picture into MEDIA_ROOT/images/demo-catalog and returns the name stored in the database."""
    target = Path(settings.MEDIA_ROOT) / DEMO_FOLDER / destination
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return f"{DEMO_FOLDER}/{destination}"


def owns_picture(field_file):
    """True when a picture is missing or was put there by a seed, so that it may be replaced."""
    return not field_file or field_file.name.startswith(f"{DEMO_FOLDER}/")


def prune_legacy_products():
    """Deletes the products of the previous seed; returns how many were removed and their picture names.

    Only products that still use a picture from the demo folder are touched, and the picture
    files themselves are removed by the caller after the database change has been committed.
    Deleting a product also deletes its comments; order items keep their data (the product link is cleared).
    """
    legacy = Product.objects.filter(slug__in=LEGACY_SLUGS, pic__startswith=f"{DEMO_FOLDER}/")
    pictures = [product.pic.name for product in legacy]
    count = legacy.count()
    legacy.delete()
    return count, pictures


class Command(BaseCommand):
    help = (
        "Add the 2023+ demo catalog (iPhone, Galaxy, iPad, AirPods) with illustrations and marked sample "
        "commerce data. Existing products are kept; --prune-old removes the previous seed's products."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--prune-old",
            action="store_true",
            help="Also delete the products created by the previous version of this seed, with their pictures.",
        )

    def handle(self, *args, **options):
        missing = missing_assets()
        if missing:
            raise CommandError(
                "Missing picture files (run `python scripts/generate_demo_art.py`):\n" + "\n".join(missing)
            )
        new_files, old_pictures = [], []
        removed = 0
        try:
            with transaction.atomic():
                categories = self.ensure_categories()
                brands = self.ensure_brands(categories)
                notice, _ = Info.objects.get_or_create(product_info=NOTICE)
                created = self.create_products(categories, brands, notice, new_files)
                if options["prune_old"]:
                    removed, old_pictures = prune_legacy_products()
        except Exception:
            for path in new_files:  # keep the media folder in step with the rolled back database
                path.unlink(missing_ok=True)
            raise
        for name in old_pictures:
            (Path(settings.MEDIA_ROOT) / name).unlink(missing_ok=True)
        self.stdout.write(self.style.SUCCESS(f"Created {created} products; {len(CATALOG) - created} already existed."))
        if options["prune_old"]:
            self.stdout.write(
                self.style.SUCCESS(f"Removed {removed} legacy products and {len(old_pictures)} picture files.")
            )

    def ensure_categories(self):
        categories = {}
        for slug, name, code in CATEGORIES:
            source = art_file(f"category-{slug}.png")
            category = Category.objects.filter(category_slug=slug).first()
            if category is None:
                category = Category(category_slug=slug, category_name=name, category_code=code)
                category.category_pic = copy_picture(source, f"category-{slug}.png")
                category.full_clean()
                category.save()
            elif owns_picture(category.category_pic):
                category.category_pic = copy_picture(source, f"category-{slug}.png")
                category.save(update_fields=["category_pic"])
            categories[slug] = category
        return categories

    def ensure_brands(self, categories):
        brands = {}
        for name, code, picture, category_slugs in BRANDS:
            source = static_images() / BRAND_FOLDER / picture
            brand = Brand.objects.filter(brand_name=name).first()
            if brand is None:
                brand = Brand(brand_name=name, brand_code=code)
                brand.brand_pic = copy_picture(source, f"brand-{code}.jpg")
                brand.full_clean(exclude=["category_brand"])
                brand.save()
            elif owns_picture(brand.brand_pic):
                brand.brand_pic = copy_picture(source, f"brand-{code}.jpg")
                brand.save(update_fields=["brand_pic"])
            brand.category_brand.add(*[categories[slug] for slug in category_slugs])
            brands[name] = brand
        return brands

    def create_products(self, categories, brands, notice, new_files):
        """Creates the missing products, oldest first, so that the newest get the latest creation date
        and therefore come first in the default (newest first) ordering of the shop."""
        created = 0
        numbered = list(enumerate(CATALOG, start=1))
        for index, spec in reversed(numbered):
            if Product.objects.filter(slug=spec.slug).exists():
                continue
            picture = art_file(spec.image)
            stored = copy_picture(picture, f"{spec.slug}.png")
            new_files.append(Path(settings.MEDIA_ROOT) / stored)
            product = Product(
                slug=spec.slug,
                product_code=PRODUCT_CODE_BASE + index,
                product_name=spec.name,
                product_color=spec.color,
                product_category=categories[spec.category],
                product_brand=brands[spec.brand],
                product_number=spec.stock,
                capability=spec.capability,
                resolution=spec.camera,
                technology=spec.tech,
                platform_os=spec.os,
                bluetooth="دارد",
                product_rate=Decimal(spec.rate),
                specifications=spec.specs,
                product_description=f"{spec.desc}\n\n{NOTICE}",
                mini_description=spec.mini,
                price=Decimal(spec.price),
                offer=spec.offer,
                time_send=DELIVERY_DAYS[index % len(DELIVERY_DAYS)],
                product_inf=notice,
                pic=stored,
            )
            product.full_clean()
            product.save()
            created += 1
        return created
