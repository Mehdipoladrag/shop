import io
from dataclasses import replace
from decimal import Decimal
from pathlib import Path

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import call_command
from PIL import Image

from accounts.models import CustomUser
from blog.models import Blogs
from conftest import make_image
from shop.management.commands import seed_demo_catalog as seed
from shop.management.commands.seed_demo_blog import EDITOR_NAME, EDITOR_USERNAME, LEGACY_EDITOR_USERNAME
from shop.models import Brand, Category, Info, Product

pytestmark = pytest.mark.django_db

MIN_PRODUCTS, MAX_PRODUCTS = 30, 45
STOCK_RANGE = (3, 20)
RATE_RANGE = (Decimal("4.2"), Decimal("4.9"))
MAX_OFFER = 15
FIRST_YEAR = 2023
NEWEST_YEAR = 2025
TOP_RATED_COUNT = 5
MIN_OFFER_PRODUCTS = 5
MIN_PICTURE_SIDE = 500
MAX_PICTURE_BYTES = 120 * 1024
SAMSUNG_PRODUCTS = 3
DEMO_FOLDER = "images/demo-catalog"

# Product lines from the newest to the oldest generation; the cheapest version of each must cost less than the one before.
GENERATIONS = [
    ("apple-iphone-17-pro-max", "apple-iphone-16-pro-max", "apple-iphone-15-pro-max"),
    ("apple-iphone-17-pro", "apple-iphone-16-pro", "apple-iphone-15-pro"),
    ("apple-iphone-17", "apple-iphone-16", "apple-iphone-15"),
    ("apple-iphone-16-plus", "apple-iphone-15-plus"),
    ("samsung-galaxy-s25-ultra", "samsung-galaxy-s24-ultra"),
    ("apple-ipad-pro-13-m5", "apple-ipad-pro-13-m4"),
    ("apple-ipad-pro-11-m5", "apple-ipad-pro-11-m4"),
    ("apple-airpods-pro-3", "apple-airpods-pro-2-usb-c"),
]


def run_seed(*arguments):
    output = io.StringIO()
    call_command("seed_demo_catalog", *arguments, stdout=output)
    return output.getvalue()


def media_file(name):
    return Path(settings.MEDIA_ROOT) / name


def year_of(slug):
    return {spec.slug: spec.year for spec in seed.CATALOG}[slug]


def make_legacy_product(slug, picture=DEMO_FOLDER + "/{slug}.jpg"):
    """A product like the ones the previous seed created, with its picture file on disk (run the seed first)."""
    picture = picture.format(slug=slug)
    path = media_file(picture)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(make_image("legacy.png").read())
    template = Product.objects.first()
    return Product.objects.create(
        product_code=93001,
        product_name="محصول قدیمی",
        product_color="آبی",
        product_category=template.product_category,
        product_brand=template.product_brand,
        product_number=3,
        capability="x",
        resolution=12,
        technology="x",
        platform_os="x",
        bluetooth="دارد",
        product_rate=Decimal("4.5"),
        specifications="x",
        product_description="x",
        mini_description="x",
        price=Decimal("1000000"),
        offer=0,
        time_send=2,
        product_inf=template.product_inf,
        slug=slug,
        pic=picture,
    )


# --------------------------------------------------------------------------- catalog data


def test_catalog_has_between_30_and_45_products_all_from_2023_or_later():
    slugs = [spec.slug for spec in seed.CATALOG]

    assert MIN_PRODUCTS <= len(slugs) <= MAX_PRODUCTS
    assert all(spec.year >= FIRST_YEAR for spec in seed.CATALOG)
    assert len(set(slugs)) == len(slugs)
    assert not set(slugs) & set(seed.LEGACY_SLUGS)


def test_every_picture_is_bundled_and_is_a_small_transparent_illustration():
    assert seed.missing_assets() == []
    for spec in seed.CATALOG:
        path = seed.art_file(spec.image)
        assert path.stat().st_size <= MAX_PICTURE_BYTES, path.name
        with Image.open(path) as picture:
            assert picture.format == "PNG" and min(picture.size) >= MIN_PICTURE_SIDE, path.name
            assert picture.convert("RGBA").getpixel((0, 0))[3] == 0, f"{path.name} needs a transparent background"


def test_prices_grow_with_storage_and_with_each_generation():
    sizes_by_model = {}
    for variant in seed.VARIANTS:
        if variant.storage:
            sizes_by_model.setdefault(variant.model, []).append((variant.storage, variant.price))
    for model, sizes in sizes_by_model.items():
        prices = [price for _, price in sorted(sizes)]
        assert prices == sorted(prices), f"{model}: a bigger storage must not cost less"

    def cheapest(model):
        return min(variant.price for variant in seed.VARIANTS if variant.model == model)

    for newer_to_older in GENERATIONS:
        prices = [cheapest(model) for model in newer_to_older]
        assert prices == sorted(prices, reverse=True), newer_to_older


def test_notice_states_what_is_real_and_what_is_sample_data():
    for phrase in (
        "اطلاعات عمومی سازندگان",
        "قیمت",
        "موجودی",
        "تخفیف",
        "امتیاز",
        "زمان ارسال",
        "تصویرسازی",
        "عکس رسمی",
    ):
        assert phrase in seed.NOTICE


# --------------------------------------------------------------------------- seeding


def test_catalog_seed_creates_the_new_products_with_pictures():
    output = run_seed()

    products = Product.objects.all()
    assert products.count() == len(seed.CATALOG)
    assert f"Created {len(seed.CATALOG)} products" in output
    for product in products:
        assert product.pic and product.price > 0
        assert 0 <= product.offer <= MAX_OFFER
        assert STOCK_RANGE[0] <= product.product_number <= STOCK_RANGE[1]
        assert RATE_RANGE[0] <= product.product_rate <= RATE_RANGE[1]
        assert product.pic.name.startswith(DEMO_FOLDER + "/")
        with Image.open(media_file(product.pic.name)) as picture:  # the copied file is a valid image
            assert picture.format == "PNG"
    assert Product.objects.filter(offer__gt=0).count() >= MIN_OFFER_PRODUCTS  # the offers section has material


def test_catalog_seed_creates_only_the_expected_categories_brands_and_texts():
    run_seed()

    assert Category.objects.get(category_slug="mobile").category_name == "گوشی موبایل"
    assert Category.objects.get(category_slug="tablet").category_name == "تبلت"
    assert Category.objects.get(category_slug="audio").category_name == "هدفون و ایرپاد"
    for slug in ("mobile", "tablet", "audio"):
        assert Category.objects.get(category_slug=slug).category_pic.name == f"{DEMO_FOLDER}/category-{slug}.png"
        assert Product.objects.filter(product_category__category_slug=slug).exists()
    assert set(Brand.objects.values_list("brand_name", flat=True)) == {"Apple", "Samsung"}
    assert all(brand.brand_pic for brand in Brand.objects.all())
    assert Product.objects.filter(product_brand__brand_name="Samsung").count() == SAMSUNG_PRODUCTS
    assert not Product.objects.filter(slug__in=seed.LEGACY_SLUGS).exists()
    names = " ".join(Product.objects.values_list("product_name", flat=True))
    for old_model in ("iPhone 12", "iPhone 13", "iPhone 14", "A52", "S21", "POCO", "PlayStation"):
        assert old_model not in names

    product = Product.objects.get(slug="apple-iphone-17-pro-max-256-cosmic-orange")
    assert product.product_inf.product_info == seed.NOTICE
    assert product.product_description.endswith(seed.NOTICE)
    assert "منبع مشخصات سازنده: https://www.apple.com/iphone/compare/" in product.specifications
    assert product.product_color == "نارنجی" and "۲۵۶ گیگابایت" in product.product_name


def test_newest_products_come_first_and_are_top_rated_and_in_stock():
    run_seed()

    newest = Product.objects.order_by("-create_date").first()
    assert year_of(newest.slug) == NEWEST_YEAR
    top_rated = Product.objects.order_by("-product_rate")[:TOP_RATED_COUNT]
    assert all(product.product_number > 0 and year_of(product.slug) == NEWEST_YEAR for product in top_rated)
    assert top_rated[0].product_rate == RATE_RANGE[1]


def test_catalog_seed_can_run_twice():
    run_seed()
    pictures = sorted(path.name for path in media_file(DEMO_FOLDER).iterdir())

    output = run_seed()

    assert Product.objects.count() == len(seed.CATALOG)
    assert "Created 0 products" in output
    assert Category.objects.count() == 3 and Brand.objects.count() == 2
    assert Info.objects.filter(product_info=seed.NOTICE).count() == 1
    assert sorted(path.name for path in media_file(DEMO_FOLDER).iterdir()) == pictures


def test_catalog_seed_fails_without_changes_when_a_picture_is_missing(monkeypatch):
    monkeypatch.setattr(seed, "art_file", lambda name: Path("/nonexistent") / name)

    with pytest.raises(seed.CommandError, match="generate_demo_art"):
        run_seed()

    assert not Product.objects.exists() and not Category.objects.exists()


def test_catalog_seed_rolls_back_database_and_pictures_when_a_product_is_invalid(monkeypatch):
    broken = [replace(seed.CATALOG[0], slug="not a valid slug!")] + seed.CATALOG[1:4]  # the newest is created last
    monkeypatch.setattr(seed, "CATALOG", broken)

    with pytest.raises(ValidationError):
        run_seed()

    assert not Product.objects.exists() and not Info.objects.exists()
    assert not list(media_file(DEMO_FOLDER).glob("apple-*.png"))


def test_seed_replaces_its_own_old_category_picture_but_keeps_other_pictures():
    old = media_file(f"{DEMO_FOLDER}/category-mobile.png")
    old.parent.mkdir(parents=True, exist_ok=True)
    old.write_bytes(make_image("old.png").read())
    Category.objects.create(
        category_slug="mobile",
        category_name="گوشی موبایل",
        category_code=91001,
        category_pic=f"{DEMO_FOLDER}/category-mobile.png",
    )
    Category.objects.create(
        category_slug="tablet", category_name="تبلت", category_code=2, category_pic=make_image("mine.png")
    )
    own_picture = Category.objects.get(category_slug="tablet").category_pic.name

    run_seed()

    assert old.read_bytes() == seed.art_file("category-mobile.png").read_bytes()
    assert Category.objects.get(category_slug="tablet").category_pic.name == own_picture
    assert Category.objects.filter(category_slug="tablet").count() == 1


# --------------------------------------------------------------------------- --prune-old


def test_without_the_flag_nothing_is_deleted():
    run_seed()
    legacy = make_legacy_product("apple-iphone-13-128-blue")

    run_seed()

    assert Product.objects.filter(pk=legacy.pk).exists()
    assert media_file(legacy.pic.name).exists()


def test_prune_old_removes_only_legacy_products_and_their_pictures():
    run_seed()
    first = make_legacy_product("apple-iphone-13-128-blue")
    second = make_legacy_product("sony-playstation-5-disc-825")
    unrelated = make_legacy_product("my-own-product", picture="images/product/mine-{slug}.png")
    other_picture = make_legacy_product("apple-iphone-12-128-blue", picture="images/product/other-{slug}.png")

    output = run_seed("--prune-old")

    assert "Removed 2 legacy products" in output
    assert not Product.objects.filter(pk__in=[first.pk, second.pk]).exists()
    assert not media_file(first.pic.name).exists() and not media_file(second.pic.name).exists()
    assert Product.objects.filter(pk=unrelated.pk).exists() and media_file(unrelated.pic.name).exists()
    assert Product.objects.filter(pk=other_picture.pk).exists()  # same slug but not a seed picture: left alone
    assert Product.objects.count() == len(seed.CATALOG) + 2
    assert Category.objects.count() == 3 and Brand.objects.count() == 2


def test_prune_old_on_a_clean_database_removes_nothing_and_is_repeatable():
    output = run_seed("--prune-old")
    again = run_seed("--prune-old")

    assert "Removed 0 legacy products" in output and "Removed 0 legacy products" in again
    assert Product.objects.count() == len(seed.CATALOG)


# --------------------------------------------------------------------------- blog seed


def test_blog_seed_creates_posts_once():
    call_command("seed_demo_blog")
    call_command("seed_demo_blog")

    assert Blogs.objects.filter(slug__in=["how-to-choose-iphone", "iphone-14-vs-13", "iphone-care-tips"]).count() == 3
    assert CustomUser.objects.filter(username=EDITOR_USERNAME).count() == 1


def test_blog_seed_renames_the_legacy_editor_account_instead_of_duplicating_it():
    legacy = CustomUser.objects.create(username=LEGACY_EDITOR_USERNAME, is_staff=True, first_name="old name")

    call_command("seed_demo_blog")

    legacy.refresh_from_db()
    assert legacy.username == EDITOR_USERNAME and legacy.first_name == EDITOR_NAME
    assert not CustomUser.objects.filter(username=LEGACY_EDITOR_USERNAME).exists()
    assert CustomUser.objects.filter(username=EDITOR_USERNAME).count() == 1
    assert Blogs.objects.filter(username=legacy).count() == 3


def test_blog_seed_keeps_both_accounts_when_the_new_editor_already_exists():
    CustomUser.objects.create(username=LEGACY_EDITOR_USERNAME, is_staff=True)
    current = CustomUser.objects.create(username=EDITOR_USERNAME, is_staff=True)

    call_command("seed_demo_blog")

    assert CustomUser.objects.filter(username=LEGACY_EDITOR_USERNAME).exists()
    assert Blogs.objects.filter(username=current).count() == 3
