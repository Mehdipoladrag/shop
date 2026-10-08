"""Add three Persian blog posts with local images; safe to run repeatedly."""

from pathlib import Path
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import CustomUser
from blog.models import Blogs, Category_blog

POSTS = [
    dict(slug="choose-the-right-iphone", image="cover-choose-iphone.jpg",
         title="راهنمای انتخاب آیفون مناسب",
         text="انتخاب آیفون به نیاز شما بستگی دارد، نه فقط به جدیدترین مدل.\n\n"
              "اندازه: اگر گوشی جمع‌وجور می‌خواهید، مدل‌های ۶٫۱ اینچی گزینه‌های مناسبی هستند. "
              "برای تماشای فیلم و بازی، مدل‌های Plus و Pro Max نمایشگر بزرگ‌تری دارند.\n\n"
              "دوربین: مدل‌های Pro معمولاً دوربین تله‌فوتو و امکانات بیشتری برای عکاسی و فیلم‌برداری دارند؛ "
              "مدل‌های معمولی برای عکاسی روزمره کاملاً کافی‌اند.\n\n"
              "نمایشگر و کارایی: در نسل‌های قبل فقط مدل‌های Pro نمایشگر ProMotion با نرخ نوسازی بالا داشتند و "
              "در مدل‌های جدیدتر این امکان به مدل‌های بیشتری رسیده است؛ مشخصات هر مدل را جداگانه بررسی کنید.\n\n"
              "حافظه: آیفون حافظه قابل افزایش ندارد و اگر زیاد عکس و ویدیو می‌گیرید، ظرفیت بیشتر انتخاب مطمئن‌تری است.\n\n"
              "پشتیبانی نرم‌افزاری: مدل‌های جدیدتر معمولاً سال‌های بیشتری به‌روزرسانی دریافت می‌کنند. "
              "برای مشخصات دقیق هر مدل، صفحه مقایسه رسمی اپل را ببینید."),
    dict(slug="iphone-16-vs-15", image="cover-iphone-16-vs-15.jpg",
         title="مقایسه آیفون ۱۶ و آیفون ۱۵",
         text="آیفون ۱۶ و ۱۵ هر دو نمایشگر OLED ۶٫۱ اینچی دارند و هر دو با درگاه USB-C عرضه شدند. "
              "تفاوت‌ها در جزئیات است.\n\n"
              "تراشه: آیفون ۱۵ با A16 Bionic و آیفون ۱۶ با A18 عرضه شد.\n\n"
              "دکمه‌ها: آیفون ۱۶ دکمه Action و دکمه Camera Control دارد؛ آیفون ۱۵ معمولی هیچ‌کدام را ندارد.\n\n"
              "هوش مصنوعی: طبق اعلام اپل، قابلیت‌های Apple Intelligence روی آیفون ۱۶ و آیفون ۱۵ پرو پشتیبانی می‌شود "
              "و آیفون ۱۵ معمولی را شامل نمی‌شود.\n\n"
              "اگر تفاوت قیمت زیاد است، آیفون ۱۵ انتخاب اقتصادی‌تری است. اگر جدیدترین امکانات و سال‌های بیشتر پشتیبانی "
              "برایتان مهم است، آیفون ۱۶ ارزش بررسی دارد.\n\n"
              "برای مشخصات دقیق هر مدل، صفحه مقایسه رسمی اپل را ببینید."),
    dict(slug="device-care-guide", image="cover-device-care.jpg",
         title="نکاتی برای نگهداری بهتر گوشی، تبلت و ایرپاد",
         text="چند عادت ساده عمر دستگاه‌هایتان را بیشتر می‌کند.\n\n"
              "۱. از قاب و گلس محافظ استفاده کنید تا خط‌وخش و ضربه به نمایشگر آسیب نزند.\n"
              "۲. دستگاه را در گرما، مثلاً داخل ماشین زیر آفتاب، رها نکنید.\n"
              "۳. از شارژر و کابل معتبر استفاده کنید.\n"
              "۴. نرم‌افزار را به‌روز نگه دارید تا اصلاحات امنیتی را دریافت کنید.\n"
              "۵. از اطلاعاتتان به‌طور منظم نسخه پشتیبان بگیرید.\n"
              "۶. توری اسپیکر ایرپاد و گوشی را با پارچه خشک و نرم تمیز کنید، نه با آب یا مواد شوینده.\n\n"
              "مقاومت در برابر آب و گرد و غبار تضمین‌شده نیست و با گذر زمان کاهش می‌یابد؛ پس با دستگاه مرطوب شارژ نکنید."),
]

# Posts created by the previous version of this seed (about older iPhone models).
LEGACY_SLUGS = ["how-to-choose-iphone", "iphone-14-vs-13", "iphone-care-tips"]

EDITOR_USERNAME = "techshop_editor"
EDITOR_NAME = "تحریریه تک‌شاپ"
# The editor account created before the shop was renamed.
LEGACY_EDITOR_USERNAME = "masai_editor"


class Command(BaseCommand):
    help = "Add three demo blog posts (author: techshop_editor); --prune-old removes the posts of the previous version."

    @staticmethod
    def get_editor():
        """The editor account; an account that still has the old shop name is renamed, not duplicated."""
        legacy = CustomUser.objects.filter(username=LEGACY_EDITOR_USERNAME).first()
        if legacy and not CustomUser.objects.filter(username=EDITOR_USERNAME).exists():
            legacy.username = EDITOR_USERNAME
            legacy.first_name = EDITOR_NAME
            legacy.save(update_fields=["username", "first_name"])
            return legacy
        editor, made = CustomUser.objects.get_or_create(
            username=EDITOR_USERNAME, defaults={"is_staff": True, "first_name": EDITOR_NAME})
        if made:
            editor.set_unusable_password()
            editor.save()
        return editor

    def add_arguments(self, parser):
        parser.add_argument(
            "--prune-old",
            action="store_true",
            help="Delete the demo posts of the previous version of this seed (and their pictures).",
        )

    def prune_legacy_posts(self):
        """Removes only the posts listed in LEGACY_SLUGS; returns how many were deleted."""
        posts = list(Blogs.objects.filter(slug__in=LEGACY_SLUGS))
        pictures = [post.blog_image.name for post in posts if post.blog_image]
        storage = Blogs._meta.get_field("blog_image").storage
        with transaction.atomic():
            for post in posts:
                post.delete()
        for name in pictures:
            if name.startswith("blog_images/demo-") and storage.exists(name):
                storage.delete(name)
        return len(posts)

    def handle(self, *args, **options):
        static = Path(settings.BASE_DIR) / "static" / "assets" / "img" / "blog"
        for row in POSTS:
            if not (static / row["image"]).is_file():
                raise FileNotFoundError(row["image"])
        created = 0
        with transaction.atomic():
            author = self.get_editor()
            category, _ = Category_blog.objects.get_or_create(
                slug_cat="mobile-guide", defaults={"name": "راهنمای موبایل"})
            for row in POSTS:
                if Blogs.objects.filter(slug=row["slug"]).exists():
                    continue
                target = Path(settings.MEDIA_ROOT) / "blog_images" / ("demo-" + row["image"])
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(static / row["image"], target)
                post = Blogs(username=author, blog_name=row["title"], category=category,
                             blog_description=row["text"], slug=row["slug"],
                             blog_image="blog_images/" + target.name)
                post.full_clean()
                post.save()
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} blog posts."))
        if options["prune_old"]:
            removed = self.prune_legacy_posts()
            self.stdout.write(self.style.SUCCESS(f"Removed {removed} old demo posts."))
