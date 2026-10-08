"""Populate the local shop with real models and explicitly marked demo commerce data."""

from decimal import Decimal
from pathlib import Path
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from shop.models import Brand, Category, Info, Product


NOTICE = (
    "کاتالوگ نمایشی: مدل و مشخصات فنی واقعی‌اند؛ قیمت‌ها به تومان، موجودی، "
    "تخفیف، امتیاز و زمان ارسال دادهٔ نمونه هستند و پیشنهاد فروش واقعی نیستند. "
    "تصاویر از فایل‌های موجود پروژه هستند. سیستم‌عامل ذکرشده مربوط به زمان عرضه است."
)

CATALOG = [
    dict(slug="apple-iphone-13-128-blue", name="اپل iPhone 13 ظرفیت ۱۲۸ گیگابایت", brand="Apple", image="p_21.jpg",
         color="آبی", price=42000000, offer=8, stock=12, rate="4.6", camera=12, os="iOS 15", tech="Apple A15 Bionic / 5G", capability="Face ID",
         mini="نمایشگر OLED، تراشه A15 و دوربین دوگانه",
         specs="حافظه داخلی: ۱۲۸ گیگابایت\nنمایشگر: ۶٫۱ اینچ Super Retina XDR OLED\nتراشه: A15 Bionic\nدوربین پشت: دو دوربین ۱۲ مگاپیکسلی\nشبکه: 5G\nدرگاه: Lightning",
         desc="آیفون ۱۳ با نمایشگر OLED و تراشه A15 برای استفاده روزمره، عکاسی و اجرای برنامه‌ها طراحی شده است. دوربین دوگانه آن از حالت سینمایی پشتیبانی می‌کند.",
         source="https://support.apple.com/en-us/111872"),
    dict(slug="apple-iphone-13-256-blue", name="اپل iPhone 13 ظرفیت ۲۵۶ گیگابایت", brand="Apple", image="p_21.jpg",
         color="آبی", price=48000000, offer=5, stock=7, rate="4.7", camera=12, os="iOS 15", tech="Apple A15 Bionic / 5G", capability="Face ID",
         mini="۲۵۶ گیگابایت حافظه برای عکس و ویدیو",
         specs="حافظه داخلی: ۲۵۶ گیگابایت\nنمایشگر: ۶٫۱ اینچ Super Retina XDR OLED\nتراشه: A15 Bionic\nدوربین پشت: دو دوربین ۱۲ مگاپیکسلی\nشبکه: 5G\nدرگاه: Lightning",
         desc="این نسخه از آیفون ۱۳ فضای بیشتری برای عکس، ویدیو و برنامه‌ها دارد. نمایشگر، پردازنده و دوربین آن با نسخه ۱۲۸ گیگابایتی یکسان است.",
         source="https://support.apple.com/en-us/111872"),
    dict(slug="apple-iphone-13-pro-256-silver", name="اپل iPhone 13 Pro ظرفیت ۲۵۶ گیگابایت", brand="Apple", image="p_8.jpg",
         color="نقره‌ای", price=68000000, offer=10, stock=5, rate="4.8", camera=12, os="iOS 15", tech="Apple A15 Bionic / 5G", capability="ProMotion / Face ID",
         mini="نمایشگر ۱۲۰ هرتز و دوربین سه‌گانه",
         specs="حافظه داخلی: ۲۵۶ گیگابایت\nنمایشگر: ۶٫۱ اینچ OLED با ProMotion تا ۱۲۰ هرتز\nتراشه: A15 Bionic\nدوربین پشت: سه دوربین ۱۲ مگاپیکسلی\nویژگی دوربین: عکاسی ماکرو و Apple ProRAW\nشبکه: 5G",
         desc="آیفون ۱۳ پرو با نمایشگر ProMotion و دوربین‌های واید، اولتراواید و تله‌فوتو عرضه شده است. قابلیت عکاسی ماکرو و ProRAW امکانات بیشتری برای ثبت و ویرایش تصویر فراهم می‌کنند.",
         source="https://support.apple.com/en-us/111871"),
    dict(slug="apple-iphone-12-pro-256-graphite", name="اپل iPhone 12 Pro ظرفیت ۲۵۶ گیگابایت", brand="Apple", image="p_22.jpg",
         color="گرافیتی", price=39000000, offer=12, stock=4, rate="4.5", camera=12, os="iOS 14", tech="Apple A14 Bionic / 5G", capability="LiDAR / Face ID",
         mini="تراشه A14، دوربین سه‌گانه و حسگر LiDAR",
         specs="حافظه داخلی: ۲۵۶ گیگابایت\nنمایشگر: ۶٫۱ اینچ Super Retina XDR OLED\nتراشه: A14 Bionic\nدوربین پشت: سه دوربین ۱۲ مگاپیکسلی\nحسگر: LiDAR\nشبکه: 5G",
         desc="آیفون ۱۲ پرو ترکیبی از بدنه با قاب فولادی، نمایشگر OLED و دوربین سه‌گانه است. حسگر LiDAR برای تشخیص عمق و برخی کاربردهای واقعیت افزوده به کار می‌رود.",
         source="https://support.apple.com/en-us/111875"),
    dict(slug="samsung-galaxy-a52-128-peach", name="سامسونگ Galaxy A52 ظرفیت ۱۲۸ گیگابایت", brand="Samsung", image="p_17.jpg",
         color="هلویی", price=14500000, offer=15, stock=18, rate="4.3", camera=64, os="Android 11 / One UI 3.1", tech="Snapdragon 720G / 4G", capability="لرزش‌گیر اپتیکال",
         mini="نمایشگر AMOLED و دوربین ۶۴ مگاپیکسلی",
         specs="مدل: Galaxy A52 4G\nحافظه داخلی: ۱۲۸ گیگابایت\nنمایشگر: ۶٫۵ اینچ Super AMOLED، نرخ ۹۰ هرتز\nتراشه: Snapdragon 720G\nدوربین اصلی: ۶۴ مگاپیکسل با OIS\nباتری: ۴۵۰۰ میلی‌آمپرساعت\nپشتیبانی از شارژ: ۲۵ وات\nمقاومت: IP67",
         desc="گلکسی A52 نسخه 4G دارای نمایشگر AMOLED و دوربین اصلی مجهز به لرزش‌گیر اپتیکال است. باتری ۴۵۰۰ میلی‌آمپرساعتی و مقاومت IP67 از ویژگی‌های این مدل هستند.",
         source="https://news.samsung.com/in/samsung-launches-galaxy-a52-and-galaxy-a72-in-india-makes-exciting-innovations-accessible-to-all"),
    dict(slug="samsung-galaxy-s21-ultra-256-black", name="سامسونگ Galaxy S21 Ultra ظرفیت ۲۵۶ گیگ", brand="Samsung", image="p_23.jpg",
         color="مشکی", price=45000000, offer=7, stock=6, rate="4.7", camera=108, os="Android 11 / One UI 3.1", tech="Exynos 2100 / 5G", capability="پشتیبانی از S Pen",
         mini="دوربین ۱۰۸ مگاپیکسل و نمایشگر ۱۲۰ هرتز",
         specs="نسخه: بین‌المللی با Exynos 2100\nحافظه داخلی: ۲۵۶ گیگابایت\nنمایشگر: ۶٫۸ اینچ Dynamic AMOLED 2X، تا ۱۲۰ هرتز\nدوربین اصلی: ۱۰۸ مگاپیکسل\nتله‌فوتو: بزرگ‌نمایی اپتیکال ۳ و ۱۰ برابر\nباتری: ۵۰۰۰ میلی‌آمپرساعت\nشبکه: 5G\nقلم S Pen: پشتیبانی می‌شود، جداگانه",
         desc="گلکسی S21 Ultra نمایشگر بزرگ و مجموعه دوربین متنوعی دارد. دو دوربین تله‌فوتو برای بزرگ‌نمایی اپتیکال به کار می‌روند و دستگاه از قلم S Pen پشتیبانی می‌کند.",
         source="https://news.samsung.com/global/samsung-galaxy-s21-ultra-the-ultimate-smartphone-experience-designed-to-be-epic-in-every-way"),
    dict(slug="poco-x4-pro-5g-256-black", name="پوکو X4 Pro 5G ظرفیت ۲۵۶ گیگابایت", brand="Xiaomi / POCO", image="p_9.jpg",
         color="مشکی", price=16500000, offer=10, stock=14, rate="4.4", camera=108, os="Android 11 / MIUI 13 for POCO", tech="Snapdragon 695 / 5G", capability="شارژ سریع ۶۷ وات",
         mini="AMOLED ۱۲۰ هرتز، رم ۸ و شارژ ۶۷ وات",
         specs="نسخه: جهانی\nحافظه داخلی: ۲۵۶ گیگابایت\nرم: ۸ گیگابایت LPDDR4X\nنمایشگر: ۶٫۶۷ اینچ AMOLED، نرخ ۱۲۰ هرتز\nتراشه: Snapdragon 695\nدوربین اصلی: ۱۰۸ مگاپیکسل\nباتری: ۵۰۰۰ میلی‌آمپرساعت\nشارژ سریع: ۶۷ وات\nبلوتوث: ۵٫۱",
         desc="پوکو X4 Pro 5G نسخه جهانی دارای نمایشگر AMOLED با نرخ نوسازی ۱۲۰ هرتز، اسپیکرهای دوگانه و دوربین اصلی ۱۰۸ مگاپیکسلی است. شارژ سریع ۶۷ وات از امکانات آن است.",
         source="https://www.po.co/global/product/poco-x4-pro-5g/specs/"),
    dict(slug="sony-playstation-5-disc-825", name="کنسول سونی PlayStation 5 دیسک‌خور ۸۲۵ گیگ", brand="Sony", image="p_11.jpg", category="gaming",
         color="سفید", price=39000000, offer=6, stock=8, rate="4.8", camera=0, os="نرم‌افزار سیستم PS5", tech="AMD Zen 2 / RDNA 2", capability="4K / Ray Tracing",
         mini="نسخه اصلی دیسک‌خور با کنترلر DualSense",
         specs="مدل: PS5 اصلی دیسک‌خور، نه Slim\nحافظه SSD: ۸۲۵ گیگابایت\nحافظه RAM: ۱۶ گیگابایت GDDR6\nپردازنده: AMD Zen 2، هشت هسته\nگرافیک: AMD RDNA 2\nدرایو: Ultra HD Blu-ray\nکنترلر: DualSense\nبلوتوث: ۵٫۱\nدوربین: ندارد",
         desc="نسخه اصلی پلی‌استیشن ۵ دیسک‌خور از بازی‌های فیزیکی و دیجیتال پشتیبانی می‌کند. SSD پرسرعت و کنترلر DualSense با بازخورد لمسی و تریگرهای تطبیقی از ویژگی‌های آن هستند. فضای قابل استفاده کمتر از ظرفیت اسمی است.",
         source="https://sonyinteractive.com/en/press-releases/2020/playstation-5-launches-this-november-at-399-for-ps5-digital-edition-and-499-for-ps5-with-ultra-hd-blu-ray-disc-drive/"),
]


APPLE_COMPARE = "https://www.apple.com/iphone/compare/"


def _iphone(slug, title, storage, color, image, price, offer, stock, rate, camera, os, chip, capability, mini, display, rear, extra, desc):
    return dict(
        slug=slug, name=f"اپل iPhone {title} ظرفیت {storage} گیگابایت", brand="Apple", image=image,
        color=color, price=price, offer=offer, stock=stock, rate=rate, camera=camera, os=os,
        tech=f"{chip} / 5G", capability=capability, mini=mini,
        specs=f"حافظه داخلی: {storage} گیگابایت\nنمایشگر: {display}\nتراشه: {chip}\nدوربین پشت: {rear}\n{extra}\nشبکه: 5G",
        desc=desc, source=APPLE_COMPARE,
    )


CATALOG += [
    _iphone("apple-iphone-14-128-blue", "14", "۱۲۸", "آبی", "p_21.jpg", 52000000, 6, 10, "4.7", 12, "iOS 16", "A15 Bionic",
            "Face ID / SOS", "نمایشگر OLED، حالت اکشن و تشخیص تصادف", "۶٫۱ اینچ Super Retina XDR OLED",
            "دو دوربین ۱۲ مگاپیکسلی", "درگاه: Lightning",
            "آیفون ۱۴ با نمایشگر OLED و تراشه A15 عرضه شد و قابلیت‌هایی مانند تشخیص تصادف و حالت اکشن برای فیلم‌برداری دارد."),
    _iphone("apple-iphone-14-plus-128-blue", "14 Plus", "۱۲۸", "آبی", "p_21.jpg", 59000000, 5, 6, "4.6", 12, "iOS 16", "A15 Bionic",
            "نمایشگر بزرگ", "نمایشگر ۶٫۷ اینچی و باتری قوی‌تر", "۶٫۷ اینچ Super Retina XDR OLED",
            "دو دوربین ۱۲ مگاپیکسلی", "درگاه: Lightning",
            "آیفون ۱۴ پلاس همان تراشه و دوربین آیفون ۱۴ را در بدنه‌ای بزرگ‌تر با نمایشگر ۶٫۷ اینچی ارائه می‌کند."),
    _iphone("apple-iphone-14-pro-256-silver", "14 Pro", "۲۵۶", "نقره‌ای", "p_8.jpg", 78000000, 9, 5, "4.8", 48, "iOS 16", "A16 Bionic",
            "Dynamic Island", "دوربین ۴۸ مگاپیکسل و Dynamic Island", "۶٫۱ اینچ OLED با ProMotion و Always-On",
            "سه دوربین؛ اصلی ۴۸ مگاپیکسل", "درگاه: Lightning",
            "آیفون ۱۴ پرو با تراشه A16 Bionic، دوربین اصلی ۴۸ مگاپیکسلی، نمایشگر Always-On و Dynamic Island عرضه شده است."),
    _iphone("apple-iphone-14-pro-max-256-silver", "14 Pro Max", "۲۵۶", "نقره‌ای", "p_8.jpg", 88000000, 8, 4, "4.9", 48, "iOS 16", "A16 Bionic",
            "Dynamic Island", "بزرگ‌ترین نمایشگر خانواده ۱۴ با A16", "۶٫۷ اینچ OLED با ProMotion و Always-On",
            "سه دوربین؛ اصلی ۴۸ مگاپیکسل", "درگاه: Lightning",
            "آیفون ۱۴ پرو مکس همان امکانات ۱۴ پرو را با نمایشگر ۶٫۷ اینچی و باتری بزرگ‌تر ارائه می‌دهد."),
    _iphone("apple-iphone-13-pro-max-256-gold", "13 Pro Max", "۲۵۶", "طلایی", "p_7.jpg", 74000000, 10, 5, "4.8", 12, "iOS 15", "A15 Bionic",
            "ProMotion / Face ID", "نمایشگر ۶٫۷ اینچ ۱۲۰ هرتز", "۶٫۷ اینچ OLED با ProMotion تا ۱۲۰ هرتز",
            "سه دوربین ۱۲ مگاپیکسلی", "ویژگی دوربین: ماکرو و Apple ProRAW",
            "آیفون ۱۳ پرو مکس نسخه بزرگ آیفون ۱۳ پرو با نمایشگر ProMotion و دوربین سه‌گانه است."),
    _iphone("apple-iphone-13-mini-128-blue", "13 mini", "۱۲۸", "آبی", "p_21.jpg", 36000000, 12, 9, "4.5", 12, "iOS 15", "A15 Bionic",
            "Face ID / جمع‌وجور", "کوچک‌ترین آیفون ۱۳ با تراشه A15", "۵٫۴ اینچ Super Retina XDR OLED",
            "دو دوربین ۱۲ مگاپیکسلی", "درگاه: Lightning",
            "آیفون ۱۳ مینی با نمایشگر ۵٫۴ اینچی برای کسانی مناسب است که گوشی جمع‌وجور می‌خواهند."),
    _iphone("apple-iphone-12-pro-max-256-graphite", "12 Pro Max", "۲۵۶", "گرافیتی", "p_22.jpg", 46000000, 11, 3, "4.6", 12, "iOS 14", "A14 Bionic",
            "LiDAR / Face ID", "نمایشگر ۶٫۷ اینچ، A14 و LiDAR", "۶٫۷ اینچ Super Retina XDR OLED",
            "سه دوربین ۱۲ مگاپیکسلی", "حسگر: LiDAR",
            "آیفون ۱۲ پرو مکس قاب فولادی، نمایشگر ۶٫۷ اینچی و دوربین سه‌گانه همراه با حسگر LiDAR دارد."),
    _iphone("apple-iphone-12-128-blue", "12", "۱۲۸", "آبی", "p_21.jpg", 30000000, 14, 8, "4.4", 12, "iOS 14", "A14 Bionic",
            "5G / Face ID", "اولین آیفون 5G با نمایشگر OLED", "۶٫۱ اینچ Super Retina XDR OLED",
            "دو دوربین ۱۲ مگاپیکسلی", "درگاه: Lightning",
            "آیفون ۱۲ اولین نسل آیفون با پشتیبانی 5G است و نمایشگر OLED و تراشه A14 دارد."),
]


class Command(BaseCommand):
    help = "Add real product models with local photos and marked demo prices; preserve existing products."

    def handle(self, *args, **options):
        static = Path(settings.BASE_DIR) / "static" / "assets" / "img"

        def picture(relative, destination):
            source = static / relative
            target = Path(settings.MEDIA_ROOT) / "images" / "demo-catalog" / destination
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            return target.relative_to(settings.MEDIA_ROOT).as_posix()

        # Validate bundled assets before making database changes.
        for row in CATALOG:
            if not (static / "product_img" / row["image"]).is_file():
                raise FileNotFoundError(row["image"])

        created = 0
        with transaction.atomic():
            categories = {}
            for slug, name, code, image in [
                ("mobile", "گوشی موبایل", 91001, "img-11.png"),
                ("gaming", "کنسول بازی", 91002, "img-7.png"),
            ]:
                category, _ = Category.objects.get_or_create(category_slug=slug, defaults={
                    "category_name": name, "category_code": code,
                    "category_pic": picture(f"Masai/bigicon/{image}", f"category-{slug}.png"),
                })
                categories[slug] = category
            brands = {}
            for code, name, image in [
                (92001, "Apple", "brand-3.jpg"),
                (92002, "Samsung", "brand-8.jpg"),
                (92003, "Xiaomi / POCO", "brand-2.jpg"),
                (92004, "Sony", None),
            ]:
                defaults = {"brand_code": code}
                if image:
                    defaults["brand_pic"] = picture(f"brands/{image}", f"brand-{code}.jpg")
                brands[name], _ = Brand.objects.get_or_create(brand_name=name, defaults=defaults)
            notice, _ = Info.objects.get_or_create(product_info=NOTICE)
            for index, row in enumerate(CATALOG, start=1):
                category = categories[row.get("category", "mobile")]
                brand = brands[row["brand"]]
                brand.category_brand.add(category)
                if Product.objects.filter(slug=row["slug"]).exists():
                    continue
                product = Product(
                    slug=row["slug"], product_code=93000 + index,
                    product_name=row["name"], product_color=row["color"],
                    product_category=category, product_brand=brand,
                    product_number=row["stock"], capability=row["capability"],
                    resolution=row["camera"], technology=row["tech"],
                    platform_os=row["os"], bluetooth="دارد",
                    product_rate=Decimal(row["rate"]),
                    specifications=row["specs"] + "\n\nمنبع مشخصات سازنده: " + row["source"],
                    product_description=row["desc"] + "\n\n" + NOTICE,
                    mini_description=row["mini"], price=Decimal(row["price"]),
                    offer=row["offer"], time_send=2, product_inf=notice,
                    pic=picture(f"product_img/{row['image']}", row["slug"] + ".jpg"),
                )
                product.full_clean()
                product.save()
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} products; retained {len(CATALOG) - created} existing catalog entries."))
