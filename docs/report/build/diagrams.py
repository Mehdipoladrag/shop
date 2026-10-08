"""Draws every diagram of the report into ../figures/*.svg (rendered to PNG by render_figures.js)."""
from pathlib import Path

from svgkit import *

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)


def architecture():
    s = Svg(1600, 990)
    bands = [("لایه کاربر", 30, 190), ("لایه ارتباط", 250, 150), ("لایه سرویس‌دهی", 410, 300), ("لایه داده و پیام‌رسانی", 740, 220)]
    for name, y, h in bands:
        s.rect(30, y, 1540, h, NAVY_50, NAVY_100, rx=18)
        s.text(1545, y + 34, name, 22, NAVY_700, 700, "end")
    s.box(1020, 80, 430, 100, "فروشگاه تک‌شاپ", "برنامه تک‌صفحه‌ای React (مسیر /)", NAVY_100)
    s.box(560, 80, 430, 100, "پنل مدیریت", "برنامه تک‌صفحه‌ای React (مسیر /panel)", NAVY_100)
    s.box(100, 80, 430, 100, "مستندات API", "Swagger UI و ReDoc", "#ffffff")
    s.box(1020, 290, 430, 80, "Vite Dev Server :5173", "پروکسی مسیرهای API و رسانه", "#ffffff")
    s.box(560, 290, 430, 80, "فایل‌های ساخته‌شده (dist)", "نسخه تولید فرانت‌اند", "#ffffff", dash="8 6")
    s.arrow([(1235, 180), (1235, 290)], "درخواست fetch / JSON", size=18)
    s.arrow([(775, 180), (775, 290)], None, dash="8 6")
    s.rect(60, 465, 1480, 225, "#ffffff", NAVY_700, 2.5, rx=18)
    s.text(800, 500, "Django 5.0 + Django REST Framework", 24, NAVY_700, 700)
    apps = [("accounts", "کاربران، پروفایل، ورود"), ("shop", "محصول، سبد، سفارش"), ("blog", "وبلاگ و دسته‌ها"), ("contact", "پیام‌های تماس"), ("adminpanel", "آمار پنل مدیریت")]
    for index, (name, sub) in enumerate(apps):
        s.box(1275 - index * 288, 520, 255, 70, name, sub, NAVY_50, size=21, latin=True)
    infra = ["نشست و CSRF", "JWT برای پنل", "محدودیت نرخ", "Serializer و اعتبارسنجی", "Middleware بی‌کش API"]
    for index, name in enumerate(infra):
        s.box(1275 - index * 288, 612, 255, 56, name, None, "#ffffff", stroke=NAVY_300, size=19)
    s.arrow([(1235, 370), (1235, 465)], "HTTP", size=18)
    s.arrow([(775, 370), (775, 465)], None, dash="8 6")
    data = [("PostgreSQL", "داده‌های اصلی"), ("Redis", "نشست، کش، قفل"), ("RabbitMQ", "صف پیام"), ("Celery", "Worker و Beat"), ("Media", "تصاویر بارگذاری‌شده")]
    for index, (name, sub) in enumerate(data):
        s.box(1275 - index * 288, 805, 255, 100, name, sub, NAVY_100, latin=True)
    for index, label in enumerate(["ORM", "django-redis", "broker", "وظایف", "فایل"]):
        x = 1402 - index * 288
        s.arrow([(x, 690), (x, 805)], label, size=17, offset=(0, -4))
    s.save(OUT / "architecture.svg")


def use_cases():
    s = Svg(1600, 1060)
    s.rect(30, 190, 1540, 840, "#fcfdff", NAVY_300, 2, rx=20, dash="10 8")
    s.text(1540, 228, "سامانه تک‌شاپ", 24, NAVY_700, 700, "end")
    columns = [
        (1300, "مهمان", ["مرور محصولات و دسته‌بندی‌ها", "جست‌وجو و فیلتر محصولات", "مشاهده جزئیات محصول", "مدیریت سبد خرید", "مطالعه مقالات وبلاگ", "ارسال پیام تماس", "ثبت‌نام", "ورود به حساب"]),
        (800, "مشتری", ["ویرایش پروفایل و تصویر", "ثبت و ویرایش آدرس", "تغییر گذرواژه", "ثبت سفارش از سبد", "مشاهده فهرست سفارش‌ها", "پیگیری وضعیت سفارش", "خروج از حساب"]),
        (300, "مدیر", ["ورود به پنل (JWT)", "مشاهده داشبورد آمار", "مدیریت دسته‌بندی‌ها", "مدیریت محصولات", "مشاهده و جست‌وجوی سفارش‌ها", "مشاهده و جست‌وجوی کاربران"]),
    ]
    for cx, actor, cases in columns:
        for index, case in enumerate(cases):
            s.line(cx, 178, cx, 285 + index * 96 - 38, NAVY_300, 1.5)
        s.circle(cx, 70, 22, "#ffffff", NAVY_700, 3)
        s.line(cx, 92, cx, 140, NAVY_700, 3); s.line(cx - 36, 112, cx + 36, 112, NAVY_700, 3)
        s.line(cx, 140, cx - 28, 175, NAVY_700, 3); s.line(cx, 140, cx + 28, 175, NAVY_700, 3)
        s.text(cx + 48 + text_width(actor, 24) / 2, 112, actor, 24, NAVY_900, 700)
        for index, case in enumerate(cases):
            y = 285 + index * 96
            s.ellipse(cx, y, 215, 38, NAVY_50, NAVY_600, 2)
            s.text(cx, y + 8, case, 20, INK)
    s.arrow([(860, 120), (1240, 120)], "ارث‌بری از مهمان", dash="9 6", size=18, offset=(0, -14))
    s.save(OUT / "use_cases.svg")


def entity(s, x, y, w, name, rows, header=NAVY_700):
    height = 46 + len(rows) * 27 + 12
    s.rect(x, y, w, height, "#ffffff", header, 2, rx=10)
    s.rect(x, y, w, 46, header, header, 2, rx=10)
    s.add(f'<rect x="{x}" y="{y + 30}" width="{w}" height="16" fill="{header}"/>')
    s.text(x + w / 2, y + 32, name, 21, "#ffffff", 700, latin=True)
    for index, row in enumerate(rows):
        key = row.startswith(("PK", "FK", "1:1"))
        s.text(x + w - 14, y + 74 + index * 27, row, 17, NAVY_700 if key else INK, 700 if key else 400, "end", latin=True)
    return height


def er_diagram():
    s = Svg(1800, 1230)
    w = 380
    H = {}
    H["Category"] = entity(s, 1380, 30, w, "Category", ["PK id", "category_name", "category_code", "category_slug", "category_pic"])
    H["Brand"] = entity(s, 960, 30, w, "Brand", ["PK id", "brand_name", "brand_code", "brand_pic", "M2M category_brand"])
    H["Product"] = entity(s, 960, 270, w, "Product", ["PK id", "FK product_category", "FK product_brand", "FK product_inf", "product_name, product_color", "price, offer (0-100)", "product_number (stock)", "product_rate, time_send", "specifications, description", "pic .. pic5, slug"])
    H["Info"] = entity(s, 1380, 520, w, "Info", ["PK id", "product_info"])
    H["CustomUser"] = entity(s, 40, 30, w, "CustomUser", ["PK id", "uuid", "username, email", "first_name, last_name", "is_staff, is_superuser", "password (hash)"])
    H["Profile"] = entity(s, 40, 300, w, "CustomProfileModel", ["PK id", "1:1 user", "national_code, age, gender", "address, street, city, zipcode", "mobile, card_number, iban", "customer_image, is_complete"])
    H["Order"] = entity(s, 500, 320, w, "Order", ["PK id", "FK customer", "order_date"])
    H["OrderItem"] = entity(s, 500, 560, w, "OrderItem", ["PK id", "FK order", "FK customer", "FK product", "product_price, product_count", "product_cost, discounted_price"])
    H["Invoice"] = entity(s, 960, 700, w, "Invoice", ["PK id", "FK order", "invoice_date", "authority"])
    H["Transaction"] = entity(s, 1380, 700, w, "Transaction", ["PK id", "FK invoice", "amount", "status", "transaction_date"])
    H["Comment"] = entity(s, 40, 640, w, "Comment", ["PK id", "FK username", "FK product", "comment, rate", "created_date"])
    H["Blogs"] = entity(s, 500, 900, w, "Blogs", ["PK id", "FK username", "FK category", "blog_name, slug", "blog_description, blog_image", "create_date, update_date"])
    H["CatBlog"] = entity(s, 960, 960, w, "Category_blog", ["PK id", "name", "slug_cat"])
    H["Contact"] = entity(s, 1380, 960, w, "Contact", ["PK id", "name, email, phone", "subject, desc", "created"])

    def rel(points, one="1", many="N"):
        s.arrow(points, None, NAVY_500, 2.2)
        (x1, y1), (x2, y2) = points[0], points[-1]
        s.text(x1 + (14 if x2 < x1 else -14), y1 - 8 if y2 == y1 else y1 + (22 if y2 > y1 else -8), one, 20, CORAL, 700, latin=True)
        s.text(x2 + (-14 if x2 < x1 and y2 == y1 else 14 if y2 == y1 else 0), y2 - 8 if y2 == y1 else y2 + (-8 if y2 > y1 else 22), many, 20, CORAL, 700, latin=True)

    rel([(1380, 125), (1340, 125)], "M", "N")                                  # Brand - Category (many to many)
    rel([(1450, 30 + H["Category"]), (1450, 320), (1340, 320)])                # Category 1-N Product
    rel([(1380, 570), (1340, 570)])                                            # Info 1-N Product
    rel([(1150, 30 + H["Brand"]), (1150, 270)])                                # Brand 1-N Product
    rel([(230, 30 + H["CustomUser"]), (230, 300)], "1", "1")                   # User 1-1 Profile
    rel([(420, 100), (690, 100), (690, 320)])                                  # User 1-N Order
    rel([(690, 320 + H["Order"]), (690, 560)])                                 # Order 1-N OrderItem
    rel([(960, 500), (920, 500), (920, 640), (880, 640)])                      # Product 1-N OrderItem
    rel([(880, 380), (940, 380), (940, 780), (960, 780)])                      # Order 1-N Invoice
    rel([(1340, 783), (1380, 783)])                                            # Invoice 1-N Transaction
    rel([(40, 720), (18, 720), (18, 70), (40, 70)], "N", "1")                  # Comment N-1 User
    rel([(880, 1010), (960, 1010)], "N", "1")                                  # Blogs N-1 Category_blog
    s.save(OUT / "er_diagram.svg")


def seq_login():
    msgs = [(0, 1, "GET /customer/csrf/", "call"), (1, 0, "Set-Cookie: csrftoken", "return"),
            (0, 1, "POST /customer/login/ (X-CSRFToken)", "call"), (1, 2, "بررسی نرخ (۱۰ در دقیقه)", "call"),
            (1, 3, "authenticate(username, password)", "call"), (3, 1, "کاربر معتبر", "return"),
            (1, 2, "ساخت نشست جدید و چرخش CSRF", "call"), (1, 0, "200 + Set-Cookie: sessionid", "return"),
            (0, 0, "به‌روزرسانی AuthContext", "self")]
    sequence("", ["مرورگر (React)", "Django / DRF", "Redis", "PostgreSQL"], msgs).save(OUT / "seq_login.svg")


def seq_cart():
    msgs = [(0, 1, "POST /public/cart/ {product_id, count}", "call"), (1, 1, "بررسی CSRF و محدودیت‌ها", "self"),
            (1, 2, "خواندن سبد از نشست", "call"), (2, 1, "سبد فعلی", "return"),
            (1, 3, "یافتن محصول و قیمت", "call"), (3, 1, "Product", "return"),
            (1, 2, "ذخیره سبد در نشست", "call"), (1, 0, "200 + سبد (اقلام، جمع تعداد، جمع قیمت)", "return"),
            (0, 0, "CartContext و نشان تعداد هدر", "self")]
    sequence("", ["مرورگر (React)", "Django / DRF", "Redis (نشست)", "PostgreSQL"], msgs).save(OUT / "seq_cart.svg")


def seq_checkout():
    msgs = [(0, 1, "POST /public/checkout/", "call"), (1, 2, "قفل کاربر (cache.add)", "call"),
            (2, 1, "قفل گرفته شد", "return"), (1, 2, "بارگذاری دوباره نشست و سبد", "call"),
            (1, 3, "شروع تراکنش اتمیک", "call"), (1, 3, "ایجاد Order, Invoice, Transaction(pending)", "call"),
            (1, 3, "ایجاد OrderItem برای هر خط سبد", "call"), (3, 1, "commit", "return"),
            (1, 2, "پاک‌سازی سبد و آزاد کردن قفل", "call"), (1, 0, "201 {order_id}", "return"),
            (0, 1, "GET /customer/orders/{id}/", "call"), (1, 0, "جزئیات سفارش (صفحه موفقیت)", "return")]
    sequence("", ["مرورگر (React)", "Django / DRF", "Redis", "PostgreSQL"], msgs).save(OUT / "seq_checkout.svg")


def flow_purchase():
    s = Svg(1600, 1100)
    def node(kind, cx, cy, text, w=300, h=70):
        if kind == "term":
            s.rect(cx - w / 2, cy - h / 2, w, h, NAVY_700, NAVY_700, rx=35); s.text(cx, cy + 8, text, 21, "#ffffff", 700)
        elif kind == "dec":
            s.diamond(cx, cy, w + 40, h + 40); s.text(cx, cy + 8, text, 19, INK, 700)
        else:
            s.rect(cx - w / 2, cy - h / 2, w, h, NAVY_50, NAVY_600, rx=12); s.text(cx, cy + 8, text, 20, INK)
    node("term", 800, 50, "شروع")
    node("proc", 800, 160, "مرور و جست‌وجوی محصولات")
    node("proc", 800, 275, "افزودن محصول به سبد خرید")
    node("proc", 800, 390, "مشاهده سبد و تنظیم تعداد")
    node("dec", 800, 535, "وارد حساب شده است؟", 260)
    node("proc", 1300, 535, "ورود یا ثبت‌نام", 280)
    node("dec", 800, 715, "آدرس و موبایل کامل است؟", 280)
    node("proc", 1300, 710, "تکمیل آدرس در حساب", 280)
    node("proc", 800, 880, "ثبت سفارش (Order + Invoice)")
    node("proc", 300, 880, "پاک شدن سبد و نمایش کد سفارش", 360)
    node("term", 300, 1020, "پایان")
    for a, b, lab in [((800, 85), (800, 125), None), ((800, 195), (800, 240), None), ((800, 310), (800, 355), None), ((800, 425), (800, 475), None)]:
        s.arrow([a, b], lab)
    s.arrow([(800, 595), (800, 665)], "بله", offset=(-34, 0))
    s.arrow([(960, 535), (1160, 535)], "خیر", offset=(0, -14))
    s.arrow([(1300, 570), (1300, 622), (806, 622)], None)
    s.arrow([(800, 770), (800, 845)], "بله", offset=(-34, -4))
    s.arrow([(960, 710), (1160, 710)], "خیر", offset=(0, -14))
    s.arrow([(1300, 745), (1300, 812), (806, 812)], None)
    s.arrow([(650, 880), (480, 880)], None)
    s.arrow([(300, 915), (300, 985)], None)
    s.save(OUT / "flow_purchase.svg")


def state_order():
    s = Svg(1600, 620)
    s.circle(1500, 300, 18, NAVY_900)
    s.arrow([(1482, 300), (1330, 300)], "ثبت سفارش")
    s.rect(1000, 240, 330, 120, NAVY_50, NAVY_700, 2.5, rx=24); s.text(1165, 288, "pending", 26, NAVY_700, 700, latin=True); s.text(1165, 328, "در انتظار پرداخت", 21, MUTED)
    s.rect(420, 90, 330, 120, GREEN_BG, GREEN, 2.5, rx=24); s.text(585, 138, "completed", 26, GREEN, 700, latin=True); s.text(585, 178, "پرداخت موفق", 21, MUTED)
    s.rect(420, 390, 330, 120, RED_BG, RED, 2.5, rx=24); s.text(585, 438, "failed", 26, RED, 700, latin=True); s.text(585, 478, "پرداخت ناموفق", 21, MUTED)
    s.arrow([(1000, 270), (750, 160)], "تأیید درگاه پرداخت")
    s.arrow([(1000, 330), (750, 440)], "خطا یا انصراف")
    s.arrow([(585, 390), (585, 210)], None, dash="8 6")
    s.text(640, 300, "تلاش مجدد", 19, MUTED, 400, "start")
    s.circle(150, 150, 18, "#ffffff", NAVY_900, 4); s.circle(150, 150, 9, NAVY_900)
    s.arrow([(420, 150), (180, 150)], None)
    s.rect(80, 380, 1240, 0, "none", "none", 0)
    s.rect(40, 540, 1520, 60, CORAL_50, CORAL, 1.5, rx=12)
    s.text(800, 578, "در نسخه فعلی درگاه پرداخت آنلاین متصل نیست؛ سفارش با تراکنش pending ذخیره می‌شود.", 20, INK)
    s.save(OUT / "state_order.svg")


def deployment():
    s = Svg(1600, 900)
    s.rect(30, 30, 1540, 380, NAVY_50, NAVY_200, 2, rx=18); s.text(1545, 66, "محیط توسعه (بدون Docker)", 22, NAVY_700, 700, "end")
    s.box(1180, 100, 330, 110, "مرورگر", "http://127.0.0.1:5173", "#ffffff", latin=False)
    s.box(740, 100, 330, 110, "Vite Dev Server", "پورت ۵۱۷۳ + پروکسی", NAVY_100)
    s.box(300, 100, 330, 110, "Django runserver", "پورت ۸۰۰۱", NAVY_100)
    s.arrow([(1180, 155), (1070, 155)], "HTTP"); s.arrow([(740, 155), (630, 155)], "پروکسی")
    s.box(1180, 270, 330, 100, "PostgreSQL", "پایگاه داده shop_db", NAVY_50, latin=True)
    s.box(740, 270, 330, 100, "Redis", "نشست، کش، قفل", NAVY_50, latin=True)
    s.box(300, 270, 330, 100, "پوشه media", "تصاویر آپلودی", NAVY_50)
    s.arrow([(465, 210), (1345, 270)], None, NAVY_300); s.arrow([(465, 210), (905, 270)], None, NAVY_300); s.arrow([(465, 210), (465, 270)], None, NAVY_300)
    s.rect(30, 450, 1540, 420, "#ffffff", NAVY_700, 2.5, rx=18, dash="10 8"); s.text(1545, 486, "استقرار با Docker Compose", 22, NAVY_700, 700, "end")
    names = [("web", "Django :8000"), ("db", "PostgreSQL"), ("redis", "Redis"), ("rabbitmq", "RabbitMQ"), ("celery", "Worker"), ("celery_beat", "Beat"), ("pgadmin", "pgAdmin"), ("flower", "Flower")]
    for index, (name, sub) in enumerate(names):
        col, row = index % 4, index // 4
        s.box(1170 - col * 370, 530 + row * 150, 330, 110, name, sub, NAVY_100 if index < 4 else NAVY_50, latin=True)
    s.save(OUT / "deployment.svg")


def frontend_tree():
    s = Svg(1600, 900)
    chain = [("main.jsx", "نقطه ورود + BrowserRouter"), ("AuthProvider", "وضعیت ورود، انقضای نشست"), ("CartProvider", "سبد خرید سمت سرور"), ("FlashProvider", "پیام‌های موقت"), ("App", "مسیرها و صفحه‌های lazy")]
    for index, (name, sub) in enumerate(chain):
        s.box(1300 - index * 310, 20, 270, 100, name, sub, NAVY_200 if index == 0 else NAVY_100, size=21, latin=True)
        if index:
            s.arrow([(1300 - (index - 1) * 310, 70), (1300 - index * 310 + 270, 70)], None)
    s.box(560, 190, 480, 90, "Layout", "Header، MobileDrawer، Footer، Outlet", NAVY_100, latin=True)
    s.arrow([(190, 120), (190, 155), (800, 155), (800, 190)], None)
    pages = ["HomePage", "ShopPage", "ProductPage", "CartPage", "BlogPages", "InfoPages", "Login / Register", "AccountLayout", "CheckoutPage"]
    for index, name in enumerate(pages):
        col, row = index % 5, index // 5
        s.box(1300 - col * 300, 360 + row * 90, 260, 62, name, None, "#ffffff", size=20, latin=True)
    s.arrow([(800, 280), (800, 320), (1430, 320), (1430, 360)], None, NAVY_300); s.arrow([(800, 320), (230, 320), (230, 360)], None, NAVY_300)
    s.rect(30, 600, 1540, 270, "#ffffff", NAVY_500, 2, rx=16, dash="9 7"); s.text(1540, 640, "کیت طراحی مشترک (components)", 21, NAVY_700, 700, "end")
    kit = ["ProductCard", "Carousel", "FormField", "Pagination", "SectionHeader", "States", "Breadcrumb", "QuantityStepper"]
    for index, name in enumerate(kit):
        col, row = index % 4, index // 4
        s.box(1180 - col * 380, 670 + row * 90, 340, 64, name, None, NAVY_50, size=20, latin=True)
    s.arrow([(800, 530), (800, 600)], "استفاده از", dash="8 6", size=18)
    s.save(OUT / "frontend_tree.svg")


def sitemap():
    s = Svg(1600, 900)
    s.box(620, 20, 360, 70, "تک‌شاپ (/)", None, NAVY_700, title_fill="#ffffff")
    groups = [(1210, "فروشگاه", ["/products", "/category/:slug", "/search?q=", "/products/:slug"]), (840, "خرید", ["/cart", "/checkout", "/checkout/success/:id"]),
              (470, "حساب کاربری", ["/login", "/register", "/account", "/account/edit", "/account/password", "/account/address", "/account/orders", "/account/orders/:id"]), (100, "محتوا", ["/blog", "/blog/:slug", "/about", "/contact"])]
    for cx, title, items in groups:
        w = 330
        s.box(cx, 190, w, 70, title, None, NAVY_100)
        s.arrow([(800, 90), (800, 140), (cx + w / 2, 140), (cx + w / 2, 190)], None, NAVY_300)
        for index, item in enumerate(items):
            s.rect(cx + 20, 295 + index * 68, w - 40, 52, "#ffffff", NAVY_300, 1.8, rx=10)
            s.text(cx + w / 2, 295 + index * 68 + 34, item, 19, INK, 400, latin=True)
    s.save(OUT / "sitemap.svg")


def security_pipeline():
    s = Svg(1600, 620)
    steps = [("مرورگر", "کوکی نشست + هدر CSRF"), ("مبداهای مجاز", "CORS و TRUSTED_ORIGINS"), ("CSRF", "csrf_protect روی نمای‌های API"), ("محدودیت نرخ", "ورود ۱۰/دقیقه، ثبت‌نام ۱۰/ساعت"),
             ("احراز هویت", "نشست مشتری یا JWT مدیر"), ("مجوز", "IsAuthenticated / IsAdminUser"), ("اعتبارسنجی", "Serializer و فیلد‌های محدود"), ("پایگاه داده", "ORM و پرس‌وجوی پارامتری")]
    for index, (title, sub) in enumerate(steps):
        col, row = index % 4, index // 4
        x, y = 1270 - col * 400, 40 + row * 270
        s.box(x, y, 310, 150, title, sub, NAVY_100 if row == 0 else NAVY_50, size=23)
        s.text(x + 155, y - 4, str(index + 1), 18, CORAL, 700)
        if col < 3:
            s.arrow([(x, y + 75), (x - 90, y + 75)], None)
    s.arrow([(225, 190), (225, 250), (1425, 250), (1425, 310)], None, NAVY_300, dash="8 6")
    s.rect(40, 530, 1520, 70, CORAL_50, CORAL, 1.5, rx=12)
    s.text(800, 573, "پاسخ‌های API با سرآیند عدم‌کش ارسال می‌شوند تا داده شخصی در کش مرورگر یا پراکسی نماند.", 20, INK)
    s.save(OUT / "security_pipeline.svg")


def palette():
    s = Svg(1600, 560)
    navy = [("50", NAVY_50), ("100", NAVY_100), ("200", NAVY_200), ("300", NAVY_300), ("400", "#6b8cc9"), ("500", NAVY_500), ("600", NAVY_600), ("700", NAVY_700), ("800", NAVY_800), ("900", NAVY_900), ("950", "#0a1429")]
    for index, (name, color) in enumerate(navy):
        x = 1520 - (index + 1) * 135
        s.rect(x, 60, 125, 150, color, NAVY_200, 1.5, rx=14)
        s.text(x + 62, 245, name, 22, INK, 700, latin=True); s.text(x + 62, 275, color, 17, MUTED, 400, latin=True)
    s.text(1520, 40, "مقیاس رنگ سورمه‌ای (برند)", 22, NAVY_700, 700, "end")
    coral = [("500", CORAL), ("600", "#ee5532"), ("700", "#c93f1f")]
    for index, (name, color) in enumerate(coral):
        x = 1520 - (index + 1) * 135
        s.rect(x, 360, 125, 110, color, NAVY_200, 1.5, rx=14)
        s.text(x + 62, 500, name, 22, INK, 700, latin=True); s.text(x + 62, 528, color, 17, MUTED, 400, latin=True)
    s.text(1520, 345, "رنگ تأکیدی (کورال)", 22, NAVY_700, 700, "end")
    status = [("موفق", GREEN, GREEN_BG), ("هشدار", "#8a5a00", AMBER_BG), ("خطا", RED, RED_BG)]
    for index, (name, fg, bg) in enumerate(status):
        x = 900 - (index + 1) * 200
        s.rect(x, 360, 180, 110, bg, fg, 1.5, rx=14); s.text(x + 90, 425, name, 24, fg, 700)
    s.text(880, 345, "رنگ‌های وضعیت", 22, NAVY_700, 700, "end")
    s.save(OUT / "palette.svg")


def timeline():
    s = Svg(1600, 640)
    phases = [("تحلیل و طراحی پایگاه داده", 0, 2), ("API مدیریتی و JWT (Django REST)", 1, 4), ("پنل مدیریت React", 3, 5), ("ویترین React و API عمومی", 4, 7),
              ("API مشتری و ثبت سفارش", 6, 9), ("بازبینی امنیتی و رفع ایرادها", 8, 10), ("بازطراحی رابط و کیت طراحی", 9, 12), ("داده نمونه و تست نهایی", 11, 13)]
    unit, left = 100, 80
    s.text(800, 40, "زمان‌بندی نسبی مراحل (واحدهای نسبی، بدون تاریخ)", 22, NAVY_700, 700)
    for week in range(14):
        x = 1520 - week * unit - unit
        s.line(x, 70, x, 600, NAVY_100, 1.5)
    for index, (name, start, end) in enumerate(phases):
        y = 90 + index * 62
        x2 = 1520 - start * unit
        x1 = 1520 - end * unit
        s.rect(x1, y + 24, x2 - x1, 26, NAVY_500 if index % 2 == 0 else NAVY_700, NAVY_700, 1, rx=8)
        s.text(x2, y + 14, name, 20, INK, 400, "end")
    s.save(OUT / "timeline.svg")


def logo():
    s = Svg(400, 400, "#ffffff")
    s.rect(20, 20, 360, 360, NAVY_700, NAVY_700, rx=100)
    s.add('<path d="M115 135 H285 M200 135 V290" fill="none" stroke="#ffffff" stroke-width="34" stroke-linecap="round"/>')
    s.circle(305, 290, 30, CORAL)
    s.save(OUT / "logo.svg")


if __name__ == "__main__":
    logo()
    for function in (architecture, use_cases, er_diagram, seq_login, seq_cart, seq_checkout, flow_purchase, state_order, deployment, frontend_tree, sitemap, security_pipeline, palette, timeline):
        function()
    print("svg done")
