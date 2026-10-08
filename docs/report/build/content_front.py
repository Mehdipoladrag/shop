from blocks import *

THANKS = [
    "سپاس بی‌کران خدای مهربان را که توفیق انجام این پروژه را عطا فرمود.",
    "از استاد گران‌قدر، جناب آقای سجاد پیراهش، به‌خاطر راهنمایی‌ها، نکته‌سنجی‌ها و فرصتی که برای یادگیری عملی فراهم کردند، صمیمانه سپاسگزارم.",
    "از خانواده‌ام که در تمام مراحل تحصیل همراه و پشتیبانم بودند، و از همکلاسی‌ها و دوستانی که با نظرات خود در بهبود این کار کمک کردند، قدردانی می‌کنم.",
]

ABSTRACT_FA = [
    "این گزارش مراحل تحلیل، طراحی، پیاده‌سازی و آزمون «تک‌شاپ» را شرح می‌دهد؛ یک فروشگاه اینترنتی کالای دیجیتال که برای مشتریان ایرانی و به زبان فارسی (راست‌به‌چپ) ساخته شده است. بخش سرور با زبان Python و چارچوب Django و Django REST Framework نوشته شده و داده‌ها در PostgreSQL ذخیره می‌شوند؛ Redis برای نشست، کش، محدودیت نرخ و قفل سفارش، و RabbitMQ و Celery برای کارهای زمان‌بندی‌شده به کار رفته‌اند. رابط کاربری از دو برنامه‌ی تک‌صفحه‌ای React و Vite ساخته شده است: ویترین فروشگاه برای مشتریان و پنل مدیریت برای کارکنان.",
    "سامانه شامل مرور و جست‌وجوی محصولات با فیلتر، سبد خرید مبتنی بر نشست، ثبت‌نام و ورود، مدیریت پروفایل و آدرس، ثبت سفارش با تراکنش اتمیک، پیگیری وضعیت سفارش، وبلاگ، فرم تماس و پنل مدیریت است. در طراحی به امنیت (CSRF، محدودیت نرخ، اعتبارسنجی)، دسترس‌پذیری و واکنش‌گرایی توجه شده و یک کیت طراحی اختصاصی با رنگ‌های سورمه‌ای و کورال ساخته شده است. کیفیت کار با ۱۷۳ آزمون خودکار، آزمون‌های انتها‌به‌انتها با Playwright و یک بازبینی امنیتی مستقل سنجیده شد که ایرادهای یافت‌شده در آن برطرف گردید.",
    "گزارش با دیاگرام‌های UML (موارد کاربرد، توالی، فعالیت، حالت)، نمودار موجودیت-رابطه، معماری و استقرار، سناریوهای کاربردی و جدول فناوری‌ها همراه است.",
]
KEYWORDS_FA = "فروشگاه اینترنتی، Django، React، Vite، REST API، PostgreSQL، Redis، تجربه کاربری، آزمون نرم‌افزار"

ABSTRACT_EN = [
    "This report describes the analysis, design, implementation and testing of TechShop, an online store for digital goods built for Persian-speaking customers with a right-to-left interface. The server side is written in Python with Django and Django REST Framework and stores its data in PostgreSQL; Redis is used for sessions, caching, rate limiting and an order lock, and RabbitMQ with Celery runs scheduled jobs. The user interface consists of two single-page applications built with React and Vite: the storefront for customers and an admin panel for staff.",
    "The system offers product browsing and filtered search, a session-based shopping cart, registration and login, profile and address management, order placement inside an atomic transaction, order tracking, a blog, a contact form and an administration panel. The design pays attention to security (CSRF protection, rate limiting, input validation), accessibility and responsiveness, and includes a custom design kit based on navy and coral colors. Quality was checked with 173 automated tests, end-to-end browser tests with Playwright and an independent security review whose findings were fixed.",
    "The report contains UML use-case, sequence, activity and state diagrams, an entity-relationship diagram, architecture and deployment diagrams, usage scenarios and a table of technologies.",
]
KEYWORDS_EN = "Online store, Django, React, Vite, REST API, PostgreSQL, Redis, User experience, Software testing"
