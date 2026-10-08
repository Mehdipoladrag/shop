"""Add three Persian blog posts with local images; safe to run repeatedly."""

from pathlib import Path
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import CustomUser
from blog.models import Blogs, Category_blog

POSTS = [
    dict(slug="how-to-choose-iphone", image="post-1.jpg",
         title="راهنمای انتخاب آیفون مناسب",
         text="انتخاب آیفون به نیاز شما بستگی دارد، نه فقط به جدیدترین مدل.\n\n"
              "اگر گوشی جمع‌وجور می‌خواهید، مدل‌های مینی و نمایشگر ۶٫۱ اینچی گزینه‌های مناسبی هستند. "
              "اگر فیلم و بازی بیشتر برایتان مهم است، مدل‌های Plus و Pro Max با نمایشگر ۶٫۷ اینچی تجربه بهتری می‌دهند.\n\n"
              "مدل‌های Pro از نمایشگر ProMotion با نرخ نوسازی تا ۱۲۰ هرتز و دوربین تله‌فوتو بهره می‌برند. "
              "در مدل‌های معمولی، آیفون ۱۳ و ۱۴ برای استفاده روزمره و عکاسی کاملاً کافی‌اند.\n\n"
              "حافظه داخلی را هم دست‌کم نگیرید؛ آیفون حافظه قابل افزایش ندارد و اگر زیاد عکس و ویدیو می‌گیرید، ۲۵۶ گیگابایت انتخاب مطمئن‌تری است."),
    dict(slug="iphone-14-vs-13", image="post-2.jpg",
         title="مقایسه آیفون ۱۴ و آیفون ۱۳",
         text="آیفون ۱۴ و ۱۳ هر دو تراشه A15 Bionic و نمایشگر OLED ۶٫۱ اینچی دارند و تفاوتشان در جزئیات است.\n\n"
              "آیفون ۱۴ قابلیت‌های جدیدی مانند تشخیص تصادف و حالت اکشن برای فیلم‌برداری را اضافه کرده و با iOS 16 عرضه شد. "
              "آیفون ۱۳ هم با iOS 15 آمد و به‌روزرسانی‌های جدید را دریافت می‌کند.\n\n"
              "اگر تفاوت قیمت زیاد است، آیفون ۱۳ انتخاب اقتصادی‌تری است. اگر قابلیت‌های تازه‌تر برایتان مهم است، آیفون ۱۴ ارزش بررسی دارد.\n\n"
              "برای مشخصات دقیق هر مدل، صفحه مقایسه رسمی اپل را ببینید."),
    dict(slug="iphone-care-tips", image="post-3.jpg",
         title="نکاتی برای نگهداری بهتر گوشی",
         text="چند عادت ساده عمر گوشی را بیشتر می‌کند.\n\n"
              "۱. از قاب و گلس محافظ استفاده کنید تا خط‌وخش و ضربه به نمایشگر آسیب نزند.\n"
              "۲. گوشی را در گرما، مثلاً داخل ماشین زیر آفتاب، رها نکنید.\n"
              "۳. از شارژر و کابل معتبر استفاده کنید.\n"
              "۴. نرم‌افزار را به‌روز نگه دارید تا اصلاحات امنیتی را دریافت کنید.\n"
              "۵. از اطلاعاتتان به‌طور منظم نسخه پشتیبان بگیرید.\n\n"
              "مقاومت در برابر آب و گرد و غبار تضمین‌شده نیست و با گذر زمان کاهش می‌یابد؛ پس با گوشی مرطوب شارژ نکنید."),
]


EDITOR_USERNAME = "techshop_editor"
EDITOR_NAME = "تحریریه تک‌شاپ"
# The editor account created before the shop was renamed.
LEGACY_EDITOR_USERNAME = "masai_editor"


class Command(BaseCommand):
    help = "Add three demo blog posts (author: techshop_editor)."

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
