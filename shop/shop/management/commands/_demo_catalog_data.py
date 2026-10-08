"""Data of the demo catalog: products released in 2023 or later (the file name starts with an
underscore so that Django does not treat it as a management command).

Model names and specifications follow the manufacturers' public information.  Prices, stock,
discounts, ratings and delivery times are made-up sample data.  Details that could not be
confirmed with confidence (RAM of the iPhones, battery capacities, weights, ...) are left out.
"""

from dataclasses import dataclass

APPLE_IPHONE = "https://www.apple.com/iphone/compare/"
APPLE_IPAD = "https://www.apple.com/ipad/compare/"
APPLE_AIRPODS = "https://www.apple.com/airpods/"
SAMSUNG_S24_ULTRA = "https://www.samsung.com/global/galaxy/galaxy-s24-ultra/"
SAMSUNG_S25_ULTRA = "https://www.samsung.com/global/galaxy/galaxy-s25-ultra/"

MOBILE, TABLET, AUDIO = "mobile", "tablet", "audio"
APPLE, SAMSUNG = "Apple", "Samsung"


@dataclass(frozen=True)
class Model:
    """One product line with everything that does not depend on storage or color."""

    key: str  # slug prefix
    art: str  # prefix of the picture file names
    brand: str
    category: str
    title: str
    year: int
    os: str  # system software at launch
    chip: str
    network: str  # shown after the chip in the "technology" field
    camera: int  # megapixels of the main rear camera, 0 when there is none
    capability: str
    mini: str
    desc: str
    specs: tuple
    source: str
    storages: tuple = ()  # available storage sizes in GB, empty for products without storage
    has_colors: bool = True  # False when there is one color and one picture (the white AirPods)


MODELS = {model.key: model for model in [
    # ------------------------------------------------------------------ iPhone 2023
    Model("apple-iphone-15", "iphone-15", APPLE, MOBILE, "iPhone 15", 2023, "iOS 17", "A16 Bionic", "5G", 48,
          "Dynamic Island", "A16 Bionic، دوربین ۴۸ مگاپیکسل و درگاه USB-C",
          "آیفون ۱۵ در سال ۲۰۲۳ با Dynamic Island، دوربین اصلی ۴۸ مگاپیکسلی و درگاه USB-C عرضه شد؛ تراشهٔ A16 Bionic و نمایشگر OLED آن برای استفادهٔ روزمره و عکاسی مناسب است.",
          ("نمایشگر: ۶٫۱ اینچ Super Retina XDR OLED", "تراشه: A16 Bionic",
           "دوربین پشت: اصلی ۴۸ مگاپیکسل و اولتراواید ۱۲ مگاپیکسل", "ویژگی: Dynamic Island",
           "درگاه: USB-C", "شبکه: 5G", "سیستم‌عامل هنگام عرضه: iOS 17"),
          APPLE_IPHONE, (128, 256, 512)),
    Model("apple-iphone-15-plus", "iphone-15-plus", APPLE, MOBILE, "iPhone 15 Plus", 2023, "iOS 17", "A16 Bionic", "5G", 48,
          "Dynamic Island", "نسخهٔ ۶٫۷ اینچی آیفون ۱۵ با دوربین ۴۸ مگاپیکسل",
          "آیفون ۱۵ پلاس همان تراشه و دوربین آیفون ۱۵ را با نمایشگر بزرگ‌تر ۶٫۷ اینچی ارائه می‌کند.",
          ("نمایشگر: ۶٫۷ اینچ Super Retina XDR OLED", "تراشه: A16 Bionic",
           "دوربین پشت: اصلی ۴۸ مگاپیکسل و اولتراواید ۱۲ مگاپیکسل", "ویژگی: Dynamic Island",
           "درگاه: USB-C", "شبکه: 5G", "سیستم‌عامل هنگام عرضه: iOS 17"),
          APPLE_IPHONE, (128, 256, 512)),
    Model("apple-iphone-15-pro", "iphone-15-pro", APPLE, MOBILE, "iPhone 15 Pro", 2023, "iOS 17", "A17 Pro", "5G", 48,
          "ProMotion / Action", "قاب تیتانیوم، A17 Pro و دکمهٔ Action",
          "آیفون ۱۵ پرو نخستین آیفون با قاب تیتانیوم و تراشهٔ A17 Pro است. نمایشگر ProMotion تا ۱۲۰ هرتز، دکمهٔ Action و دوربین سه‌گانه با تله‌فوتو ۳ برابر از ویژگی‌های آن است.",
          ("نمایشگر: ۶٫۱ اینچ Super Retina XDR OLED با ProMotion تا ۱۲۰ هرتز", "تراشه: A17 Pro",
           "دوربین پشت: اصلی ۴۸ مگاپیکسل، اولتراواید ۱۲ مگاپیکسل و تله‌فوتو ۱۲ مگاپیکسل (۳ برابر اپتیکال)",
           "بدنه: قاب تیتانیوم", "ویژگی: دکمهٔ Action", "درگاه: USB-C", "شبکه: 5G", "سیستم‌عامل هنگام عرضه: iOS 17"),
          APPLE_IPHONE, (128, 256, 512, 1024)),
    Model("apple-iphone-15-pro-max", "iphone-15-pro-max", APPLE, MOBILE, "iPhone 15 Pro Max", 2023, "iOS 17", "A17 Pro", "5G", 48,
          "ProMotion / Action", "تله‌فوتو ۵ برابر، تیتانیوم و نمایشگر ۶٫۷ اینچ",
          "آیفون ۱۵ پرو مکس نسخهٔ بزرگ‌تر خانوادهٔ پرو است و برخلاف پرو، تله‌فوتو ۱۲ مگاپیکسلی با بزرگ‌نمایی اپتیکال ۵ برابر دارد.",
          ("نمایشگر: ۶٫۷ اینچ Super Retina XDR OLED با ProMotion تا ۱۲۰ هرتز", "تراشه: A17 Pro",
           "دوربین پشت: اصلی ۴۸ مگاپیکسل، اولتراواید ۱۲ مگاپیکسل و تله‌فوتو ۱۲ مگاپیکسل (۵ برابر اپتیکال)",
           "بدنه: قاب تیتانیوم", "ویژگی: دکمهٔ Action", "درگاه: USB-C", "شبکه: 5G", "سیستم‌عامل هنگام عرضه: iOS 17"),
          APPLE_IPHONE, (256, 512, 1024)),
    # ------------------------------------------------------------------ iPhone 2024
    Model("apple-iphone-16", "iphone-16", APPLE, MOBILE, "iPhone 16", 2024, "iOS 18", "A18", "5G", 48,
          "Camera Control", "A18، دکمهٔ Camera Control و دوربین ۴۸ مگاپیکسل",
          "آیفون ۱۶ با تراشهٔ A18، دکمهٔ Camera Control برای کنترل دوربین و دوربین اصلی ۴۸ مگاپیکسلی عرضه شد و iOS 18 را همراه دارد.",
          ("نمایشگر: ۶٫۱ اینچ Super Retina XDR OLED", "تراشه: A18",
           "دوربین پشت: اصلی Fusion ۴۸ مگاپیکسل و اولتراواید ۱۲ مگاپیکسل", "ویژگی: Camera Control و دکمهٔ Action",
           "درگاه: USB-C", "شبکه: 5G", "سیستم‌عامل هنگام عرضه: iOS 18"),
          APPLE_IPHONE, (128, 256, 512)),
    Model("apple-iphone-16-plus", "iphone-16-plus", APPLE, MOBILE, "iPhone 16 Plus", 2024, "iOS 18", "A18", "5G", 48,
          "Camera Control", "نسخهٔ ۶٫۷ اینچی آیفون ۱۶ با تراشهٔ A18",
          "آیفون ۱۶ پلاس همان تراشه و دوربین آیفون ۱۶ را با نمایشگر بزرگ‌تر ۶٫۷ اینچی ارائه می‌کند.",
          ("نمایشگر: ۶٫۷ اینچ Super Retina XDR OLED", "تراشه: A18",
           "دوربین پشت: اصلی Fusion ۴۸ مگاپیکسل و اولتراواید ۱۲ مگاپیکسل", "ویژگی: Camera Control و دکمهٔ Action",
           "درگاه: USB-C", "شبکه: 5G", "سیستم‌عامل هنگام عرضه: iOS 18"),
          APPLE_IPHONE, (128, 256, 512)),
    Model("apple-iphone-16-pro", "iphone-16-pro", APPLE, MOBILE, "iPhone 16 Pro", 2024, "iOS 18", "A18 Pro", "5G", 48,
          "Camera Control", "A18 Pro، تیتانیوم و تله‌فوتو ۵ برابر",
          "آیفون ۱۶ پرو با نمایشگر ۶٫۳ اینچی، تراشهٔ A18 Pro، دوربین اولتراواید ۴۸ مگاپیکسلی و تله‌فوتو ۵ برابر عرضه شد.",
          ("نمایشگر: ۶٫۳ اینچ Super Retina XDR OLED با ProMotion تا ۱۲۰ هرتز", "تراشه: A18 Pro",
           "دوربین پشت: اصلی ۴۸ مگاپیکسل، اولتراواید ۴۸ مگاپیکسل و تله‌فوتو ۱۲ مگاپیکسل (۵ برابر اپتیکال)",
           "بدنه: قاب تیتانیوم", "ویژگی: Camera Control و دکمهٔ Action", "درگاه: USB-C", "شبکه: 5G",
           "سیستم‌عامل هنگام عرضه: iOS 18"),
          APPLE_IPHONE, (128, 256, 512, 1024)),
    Model("apple-iphone-16-pro-max", "iphone-16-pro-max", APPLE, MOBILE, "iPhone 16 Pro Max", 2024, "iOS 18", "A18 Pro", "5G", 48,
          "Camera Control", "نمایشگر ۶٫۹ اینچی، A18 Pro و تله‌فوتو ۵ برابر",
          "آیفون ۱۶ پرو مکس بزرگ‌ترین نمایشگر خانوادهٔ ۱۶ را با تراشهٔ A18 Pro، دوربین اولتراواید ۴۸ مگاپیکسلی و تله‌فوتو ۵ برابر ارائه می‌کند.",
          ("نمایشگر: ۶٫۹ اینچ Super Retina XDR OLED با ProMotion تا ۱۲۰ هرتز", "تراشه: A18 Pro",
           "دوربین پشت: اصلی ۴۸ مگاپیکسل، اولتراواید ۴۸ مگاپیکسل و تله‌فوتو ۱۲ مگاپیکسل (۵ برابر اپتیکال)",
           "بدنه: قاب تیتانیوم", "ویژگی: Camera Control و دکمهٔ Action", "درگاه: USB-C", "شبکه: 5G",
           "سیستم‌عامل هنگام عرضه: iOS 18"),
          APPLE_IPHONE, (256, 512, 1024)),
    # ------------------------------------------------------------------ iPhone 2025
    Model("apple-iphone-16e", "iphone-16e", APPLE, MOBILE, "iPhone 16e", 2025, "iOS 18", "A18", "5G", 48,
          "Action / مودم C1", "A18، یک دوربین ۴۸ مگاپیکسلی و مودم C1",
          "آیفون ۱۶e مدل ساده‌تر خانوادهٔ ۱۶ است با تراشهٔ A18، نمایشگر OLED ۶٫۱ اینچی، یک دوربین پشتی ۴۸ مگاپیکسلی، دکمهٔ Action و مودم C1 ساخت اپل.",
          ("نمایشگر: ۶٫۱ اینچ Super Retina XDR OLED", "تراشه: A18", "دوربین پشت: یک دوربین ۴۸ مگاپیکسلی (Fusion)",
           "ویژگی: دکمهٔ Action و مودم Apple C1", "درگاه: USB-C", "شبکه: 5G", "سیستم‌عامل هنگام عرضه: iOS 18"),
          APPLE_IPHONE, (128, 256, 512)),
    Model("apple-iphone-17", "iphone-17", APPLE, MOBILE, "iPhone 17", 2025, "iOS 26", "A19", "5G", 48,
          "ProMotion ۱۲۰ هرتز", "A19، نمایشگر ۱۲۰ هرتز و دو دوربین ۴۸ مگاپیکسل",
          "آیفون ۱۷ در ۲۰۲۵ با تراشهٔ A19، نمایشگر ۶٫۳ اینچی ProMotion، دو دوربین پشتی ۴۸ مگاپیکسلی و دوربین سلفی ۱۸ مگاپیکسلی Center Stage عرضه شد و iOS 26 را همراه دارد.",
          ("نمایشگر: ۶٫۳ اینچ Super Retina XDR OLED با ProMotion تا ۱۲۰ هرتز", "تراشه: A19",
           "دوربین پشت: اصلی ۴۸ مگاپیکسل و اولتراواید ۴۸ مگاپیکسل", "دوربین سلفی: ۱۸ مگاپیکسل Center Stage",
           "درگاه: USB-C", "شبکه: 5G", "سیستم‌عامل هنگام عرضه: iOS 26"),
          APPLE_IPHONE, (256, 512)),
    Model("apple-iphone-air", "iphone-air", APPLE, MOBILE, "iPhone Air", 2025, "iOS 26", "A19 Pro", "5G", 48,
          "ضخامت ۵٫۶ میلی‌متر", "ضخامت ۵٫۶ میلی‌متر، A19 Pro و قاب تیتانیوم",
          "آیفون ایر باریک‌ترین آیفون است؛ با ضخامت ۵٫۶ میلی‌متر، قاب تیتانیوم، نمایشگر ۶٫۵ اینچی ProMotion، تراشهٔ A19 Pro و یک دوربین اصلی ۴۸ مگاپیکسلی.",
          ("نمایشگر: ۶٫۵ اینچ Super Retina XDR OLED با ProMotion تا ۱۲۰ هرتز", "تراشه: A19 Pro",
           "دوربین پشت: یک دوربین اصلی ۴۸ مگاپیکسلی (Fusion)", "دوربین سلفی: ۱۸ مگاپیکسل Center Stage",
           "ضخامت: ۵٫۶ میلی‌متر", "بدنه: قاب تیتانیوم", "درگاه: USB-C", "شبکه: 5G", "سیستم‌عامل هنگام عرضه: iOS 26"),
          APPLE_IPHONE, (256, 512, 1024)),
    Model("apple-iphone-17-pro", "iphone-17-pro", APPLE, MOBILE, "iPhone 17 Pro", 2025, "iOS 26", "A19 Pro", "5G", 48,
          "Vapor chamber", "A19 Pro، سه دوربین ۴۸ مگاپیکسل و خنک‌کنندهٔ بخار",
          "آیفون ۱۷ پرو با بدنهٔ یکپارچهٔ آلومینیومی، تراشهٔ A19 Pro، سیستم خنک‌کنندهٔ vapor chamber و سه دوربین پشتی ۴۸ مگاپیکسلی عرضه شد.",
          ("نمایشگر: ۶٫۳ اینچ Super Retina XDR OLED با ProMotion تا ۱۲۰ هرتز", "تراشه: A19 Pro",
           "دوربین پشت: سه دوربین ۴۸ مگاپیکسلی (اصلی، اولتراواید و تله‌فوتو)", "دوربین سلفی: ۱۸ مگاپیکسل Center Stage",
           "بدنه: آلومینیوم یکپارچه با خنک‌کنندهٔ vapor chamber", "درگاه: USB-C", "شبکه: 5G",
           "سیستم‌عامل هنگام عرضه: iOS 26"),
          APPLE_IPHONE, (256, 512, 1024)),
    Model("apple-iphone-17-pro-max", "iphone-17-pro-max", APPLE, MOBILE, "iPhone 17 Pro Max", 2025, "iOS 26", "A19 Pro", "5G", 48,
          "Vapor chamber", "نمایشگر ۶٫۹ اینچی، A19 Pro و سه دوربین ۴۸ مگاپیکسل",
          "آیفون ۱۷ پرو مکس بزرگ‌ترین نمایشگر خانوادهٔ ۱۷ را با تراشهٔ A19 Pro، بدنهٔ یکپارچهٔ آلومینیومی و سه دوربین پشتی ۴۸ مگاپیکسلی ارائه می‌کند.",
          ("نمایشگر: ۶٫۹ اینچ Super Retina XDR OLED با ProMotion تا ۱۲۰ هرتز", "تراشه: A19 Pro",
           "دوربین پشت: سه دوربین ۴۸ مگاپیکسلی (اصلی، اولتراواید و تله‌فوتو)", "دوربین سلفی: ۱۸ مگاپیکسل Center Stage",
           "بدنه: آلومینیوم یکپارچه با خنک‌کنندهٔ vapor chamber", "درگاه: USB-C", "شبکه: 5G",
           "سیستم‌عامل هنگام عرضه: iOS 26"),
          APPLE_IPHONE, (256, 512, 1024)),
    # ------------------------------------------------------------------ Samsung
    Model("samsung-galaxy-s24-ultra", "galaxy-s24-ultra", SAMSUNG, MOBILE, "Galaxy S24 Ultra", 2024, "Android 14 / One UI 6.1",
          "Snapdragon 8 Gen 3 for Galaxy", "5G", 200, "S Pen / Galaxy AI", "S Pen، دوربین ۲۰۰ مگاپیکسل و قاب تیتانیوم",
          "گلکسی S24 اولترا با نمایشگر تخت ۶٫۸ اینچی، قاب تیتانیوم، دوربین اصلی ۲۰۰ مگاپیکسلی، S Pen داخلی و قابلیت‌های Galaxy AI در ۲۰۲۴ عرضه شد.",
          ("نمایشگر: ۶٫۸ اینچ Dynamic LTPO AMOLED 2X با نرخ نوسازی ۱ تا ۱۲۰ هرتز", "تراشه: Snapdragon 8 Gen 3 for Galaxy",
           "رم: ۱۲ گیگابایت",
           "دوربین پشت: اصلی ۲۰۰ مگاپیکسل، اولتراواید ۱۲ مگاپیکسل، تله‌فوتو ۱۰ مگاپیکسل (۳ برابر) و تله‌فوتو ۵۰ مگاپیکسل (۵ برابر)",
           "دوربین سلفی: ۱۲ مگاپیکسل", "باتری: ۵۰۰۰ میلی‌آمپرساعت با شارژ سریع ۴۵ وات", "قلم: S Pen داخلی",
           "بدنه: قاب تیتانیوم", "شبکه: 5G", "سیستم‌عامل هنگام عرضه: Android 14 / One UI 6.1"),
          SAMSUNG_S24_ULTRA, (256, 512, 1024)),
    Model("samsung-galaxy-s25-ultra", "galaxy-s25-ultra", SAMSUNG, MOBILE, "Galaxy S25 Ultra", 2025, "Android 15 / One UI 7",
          "Snapdragon 8 Elite for Galaxy", "5G", 200, "S Pen / Galaxy AI", "Snapdragon 8 Elite، نمایشگر ۶٫۹ اینچ و S Pen",
          "گلکسی S25 اولترا با نمایشگر ۶٫۹ اینچی، تراشهٔ Snapdragon 8 Elite for Galaxy، دوربین اصلی ۲۰۰ مگاپیکسلی، S Pen داخلی و One UI 7 در ۲۰۲۵ عرضه شد.",
          ("نمایشگر: ۶٫۹ اینچ Dynamic LTPO AMOLED 2X با نرخ نوسازی ۱ تا ۱۲۰ هرتز", "تراشه: Snapdragon 8 Elite for Galaxy",
           "رم: ۱۲ گیگابایت",
           "دوربین پشت: اصلی ۲۰۰ مگاپیکسل، اولتراواید ۵۰ مگاپیکسل، تله‌فوتو ۱۰ مگاپیکسل (۳ برابر) و تله‌فوتو ۵۰ مگاپیکسل (۵ برابر)",
           "دوربین سلفی: ۱۲ مگاپیکسل", "باتری: ۵۰۰۰ میلی‌آمپرساعت با شارژ سریع ۴۵ وات", "قلم: S Pen داخلی",
           "بدنه: قاب تیتانیوم", "شبکه: 5G", "سیستم‌عامل هنگام عرضه: Android 15 / One UI 7"),
          SAMSUNG_S25_ULTRA, (256, 512, 1024)),
    # ------------------------------------------------------------------ iPad
    Model("apple-ipad-pro-13-m4", "ipad-pro-13", APPLE, TABLET, "iPad Pro 13 اینچ M4", 2024, "iPadOS 17", "Apple M4", "Wi-Fi 6E", 12,
          "Apple Pencil Pro", "M4، OLED دولایه و ضخامت ۵٫۱ میلی‌متر",
          "آیپد پرو ۱۳ اینچی با تراشهٔ M4 و نمایشگر Ultra Retina XDR از نوع OLED دولایه در ۲۰۲۴ عرضه شد؛ ضخامت آن ۵٫۱ میلی‌متر است و از Apple Pencil Pro و Magic Keyboard پشتیبانی می‌کند.",
          ("نمایشگر: ۱۳ اینچ Ultra Retina XDR (OLED دولایه)", "تراشه: Apple M4", "ضخامت: ۵٫۱ میلی‌متر",
           "دوربین پشت: ۱۲ مگاپیکسل", "دوربین جلو: ۱۲ مگاپیکسل اولتراواید", "احراز هویت: Face ID",
           "درگاه: USB-C با Thunderbolt / USB 4", "مدل: Wi-Fi", "پشتیبانی: Apple Pencil Pro و Magic Keyboard",
           "سیستم‌عامل هنگام عرضه: iPadOS 17"),
          APPLE_IPAD, (256, 512, 1024, 2048)),
    Model("apple-ipad-pro-11-m4", "ipad-pro-11", APPLE, TABLET, "iPad Pro 11 اینچ M4", 2024, "iPadOS 17", "Apple M4", "Wi-Fi 6E", 12,
          "Apple Pencil Pro", "M4، OLED دولایه و ضخامت ۵٫۳ میلی‌متر",
          "آیپد پرو ۱۱ اینچی با تراشهٔ M4 و نمایشگر Ultra Retina XDR از نوع OLED دولایه در ۲۰۲۴ عرضه شد؛ ضخامت آن ۵٫۳ میلی‌متر است و از Apple Pencil Pro و Magic Keyboard پشتیبانی می‌کند.",
          ("نمایشگر: ۱۱ اینچ Ultra Retina XDR (OLED دولایه)", "تراشه: Apple M4", "ضخامت: ۵٫۳ میلی‌متر",
           "دوربین پشت: ۱۲ مگاپیکسل", "دوربین جلو: ۱۲ مگاپیکسل اولتراواید", "احراز هویت: Face ID",
           "درگاه: USB-C با Thunderbolt / USB 4", "مدل: Wi-Fi", "پشتیبانی: Apple Pencil Pro و Magic Keyboard",
           "سیستم‌عامل هنگام عرضه: iPadOS 17"),
          APPLE_IPAD, (256, 512, 1024, 2048)),
    Model("apple-ipad-pro-13-m5", "ipad-pro-13", APPLE, TABLET, "iPad Pro 13 اینچ M5", 2025, "iPadOS 26", "Apple M5", "Wi-Fi 7", 12,
          "Apple Pencil Pro", "M5، OLED دولایه و Wi-Fi 7",
          "آیپد پرو ۱۳ اینچی با تراشهٔ M5 در ۲۰۲۵ عرضه شد؛ نمایشگر OLED دولایه، تراشهٔ بی‌سیم Apple N1 با Wi-Fi 7 و iPadOS 26 از ویژگی‌های آن است.",
          ("نمایشگر: ۱۳ اینچ Ultra Retina XDR (OLED دولایه)", "تراشه: Apple M5", "تراشهٔ بی‌سیم: Apple N1 (Wi-Fi 7)",
           "دوربین پشت: ۱۲ مگاپیکسل", "احراز هویت: Face ID", "درگاه: USB-C با Thunderbolt / USB 4", "مدل: Wi-Fi",
           "پشتیبانی: Apple Pencil Pro و Magic Keyboard", "سیستم‌عامل هنگام عرضه: iPadOS 26"),
          APPLE_IPAD, (256, 512, 1024, 2048)),
    Model("apple-ipad-pro-11-m5", "ipad-pro-11", APPLE, TABLET, "iPad Pro 11 اینچ M5", 2025, "iPadOS 26", "Apple M5", "Wi-Fi 7", 12,
          "Apple Pencil Pro", "M5، OLED دولایه و Wi-Fi 7",
          "آیپد پرو ۱۱ اینچی با تراشهٔ M5 در ۲۰۲۵ عرضه شد؛ نمایشگر OLED دولایه، تراشهٔ بی‌سیم Apple N1 با Wi-Fi 7 و iPadOS 26 از ویژگی‌های آن است.",
          ("نمایشگر: ۱۱ اینچ Ultra Retina XDR (OLED دولایه)", "تراشه: Apple M5", "تراشهٔ بی‌سیم: Apple N1 (Wi-Fi 7)",
           "دوربین پشت: ۱۲ مگاپیکسل", "احراز هویت: Face ID", "درگاه: USB-C با Thunderbolt / USB 4", "مدل: Wi-Fi",
           "پشتیبانی: Apple Pencil Pro و Magic Keyboard", "سیستم‌عامل هنگام عرضه: iPadOS 26"),
          APPLE_IPAD, (256, 512, 1024, 2048)),
    Model("apple-ipad-air-11-m3", "ipad-air-11", APPLE, TABLET, "iPad Air 11 اینچ M3", 2025, "iPadOS 18", "Apple M3", "Wi-Fi 6E", 12,
          "Apple Pencil Pro", "M3، نمایشگر Liquid Retina ۱۱ اینچ",
          "آیپد ایر ۱۱ اینچی با تراشهٔ M3 در ۲۰۲۵ عرضه شد و از Apple Pencil Pro و Magic Keyboard پشتیبانی می‌کند.",
          ("نمایشگر: ۱۱ اینچ Liquid Retina", "تراشه: Apple M3", "دوربین پشت: ۱۲ مگاپیکسل", "دوربین جلو: ۱۲ مگاپیکسل",
           "احراز هویت: Touch ID", "درگاه: USB-C", "مدل: Wi-Fi", "پشتیبانی: Apple Pencil Pro و Magic Keyboard",
           "سیستم‌عامل هنگام عرضه: iPadOS 18"),
          APPLE_IPAD, (128, 256, 512, 1024)),
    Model("apple-ipad-mini-a17-pro", "ipad-mini", APPLE, TABLET, "iPad mini A17 Pro", 2024, "iPadOS 18", "Apple A17 Pro", "Wi-Fi 6E", 12,
          "Apple Pencil Pro", "A17 Pro، نمایشگر ۸٫۳ اینچی و Apple Pencil Pro",
          "آیپد مینی با تراشهٔ A17 Pro در ۲۰۲۴ عرضه شد؛ نمایشگر Liquid Retina ۸٫۳ اینچی، درگاه USB-C و پشتیبانی از Apple Pencil Pro و Apple Intelligence دارد.",
          ("نمایشگر: ۸٫۳ اینچ Liquid Retina", "تراشه: Apple A17 Pro", "دوربین پشت: ۱۲ مگاپیکسل", "دوربین جلو: ۱۲ مگاپیکسل",
           "احراز هویت: Touch ID", "درگاه: USB-C", "مدل: Wi-Fi", "پشتیبانی: Apple Pencil Pro و Apple Intelligence",
           "سیستم‌عامل هنگام عرضه: iPadOS 18"),
          APPLE_IPAD, (128, 256, 512)),
    Model("apple-ipad-a16", "ipad", APPLE, TABLET, "iPad A16", 2025, "iPadOS 18", "Apple A16", "Wi-Fi 6", 12,
          "Apple Pencil USB-C", "A16، نمایشگر Liquid Retina ۱۱ اینچ",
          "آیپد با تراشهٔ A16 در ۲۰۲۵ عرضه شد؛ نمایشگر Liquid Retina ۱۱ اینچی، درگاه USB-C و دوربین‌های ۱۲ مگاپیکسلی دارد.",
          ("نمایشگر: ۱۱ اینچ Liquid Retina", "تراشه: Apple A16", "دوربین پشت: ۱۲ مگاپیکسل", "دوربین جلو: ۱۲ مگاپیکسل",
           "احراز هویت: Touch ID", "درگاه: USB-C", "مدل: Wi-Fi", "پشتیبانی: Apple Pencil (USB-C)",
           "سیستم‌عامل هنگام عرضه: iPadOS 18"),
          APPLE_IPAD, (128, 256, 512)),
    # ------------------------------------------------------------------ AirPods
    Model("apple-airpods-pro-3", "airpods-pro-3", APPLE, AUDIO, "AirPods Pro 3", 2025, "iOS 26 / iPadOS 26", "H2", "Bluetooth", 0,
          "حذف نویز فعال", "H2، حذف نویز فعال و حسگر ضربان قلب",
          "ایرپاد پرو ۳ با تراشهٔ H2، حذف نویز فعال، مقاومت IP57، حسگر ضربان قلب و نوک‌های سیلیکونی فوم‌دار در پنج اندازه در ۲۰۲۵ عرضه شد.",
          ("تراشه: Apple H2", "ویژگی: حذف نویز فعال", "حسگر: ضربان قلب", "مقاومت: IP57",
           "نوک گوشی: سیلیکونی با فوم، در پنج اندازه", "کیس شارژ: USB-C",
           "سیستم‌عامل هنگام عرضه: iOS 26 / iPadOS 26"),
          APPLE_AIRPODS, has_colors=False),
    Model("apple-airpods-pro-2-usb-c", "airpods-pro-2", APPLE, AUDIO, "AirPods Pro 2 USB-C", 2023, "iOS 17 / iPadOS 17", "H2", "Bluetooth", 0,
          "حذف نویز فعال", "H2، حذف نویز فعال و کیس USB-C",
          "ایرپاد پرو ۲ با کیس شارژ USB-C در ۲۰۲۳ عرضه شد؛ تراشهٔ H2، حذف نویز فعال، حالت Adaptive Audio و مقاومت IP54 دارد.",
          ("تراشه: Apple H2", "ویژگی: حذف نویز فعال، حالت Transparency و Adaptive Audio", "مقاومت: IP54 برای گوشی‌ها و کیس",
           "کیس شارژ: USB-C، قابل شارژ با MagSafe، Apple Watch یا Qi",
           "باتری: تا ۶ ساعت شنیدن با یک بار شارژ و تا ۳۰ ساعت با کیس", "کنترل: لمسی روی ساقه",
           "سیستم‌عامل هنگام عرضه: iOS 17 / iPadOS 17"),
          APPLE_AIRPODS, has_colors=False),
    Model("apple-airpods-4", "airpods-4", APPLE, AUDIO, "AirPods 4", 2024, "iOS 18 / iPadOS 18", "H2", "Bluetooth", 0,
          "Spatial Audio", "H2، طراحی جدید و کیس USB-C",
          "ایرپاد ۴ با طراحی جدید و بدون نوک سیلیکونی و تراشهٔ H2 در ۲۰۲۴ عرضه شد؛ کیس آن USB-C است و گوشی‌ها مقاومت IP54 دارند.",
          ("تراشه: Apple H2", "طراحی: بدون نوک سیلیکونی", "ویژگی: Personalized Spatial Audio", "مقاومت: IP54",
           "کیس شارژ: USB-C", "سیستم‌عامل هنگام عرضه: iOS 18 / iPadOS 18"),
          APPLE_AIRPODS, has_colors=False),
    Model("apple-airpods-4-anc", "airpods-4-anc", APPLE, AUDIO, "AirPods 4 با حذف نویز", 2024, "iOS 18 / iPadOS 18", "H2", "Bluetooth", 0,
          "حذف نویز فعال", "حذف نویز فعال، H2 و کیس شارژ بی‌سیم",
          "نسخهٔ ایرپاد ۴ با حذف نویز فعال، حالت Adaptive Audio و Transparency و کیس USB-C با شارژ بی‌سیم در ۲۰۲۴ عرضه شد.",
          ("تراشه: Apple H2", "طراحی: بدون نوک سیلیکونی", "ویژگی: حذف نویز فعال، Adaptive Audio و حالت Transparency",
           "مقاومت: IP54", "کیس شارژ: USB-C با شارژ بی‌سیم", "سیستم‌عامل هنگام عرضه: iOS 18 / iPadOS 18"),
          APPLE_AIRPODS, has_colors=False),
    Model("apple-airpods-max-usb-c", "airpods-max", APPLE, AUDIO, "AirPods Max USB-C", 2024, "iOS 18 / iPadOS 18", "H1", "Bluetooth", 0,
          "حذف نویز فعال", "H1، حذف نویز فعال و درگاه USB-C",
          "ایرپاد مکس با درگاه USB-C در ۲۰۲۴ عرضه شد؛ هدفون روگوشی با حذف نویز فعال، Adaptive EQ، Spatial Audio و باتری تا ۲۰ ساعت (با حذف نویز).",
          ("تراشه: Apple H1 در هر گوشی", "ویژگی: حذف نویز فعال و حالت Transparency",
           "صدا: Adaptive EQ و Spatial Audio با ردیابی حرکت سر", "درگاه: USB-C",
           "باتری: تا ۲۰ ساعت با حذف نویز فعال", "کنترل: Digital Crown", "سیستم‌عامل هنگام عرضه: iOS 18 / iPadOS 18"),
          APPLE_AIRPODS),
]}

# Persian names of the colors.  They describe the look of the picture; they are not the
# manufacturers' marketing names.
COLORS = {
    "white": "سفید", "black": "مشکی", "space-black": "مشکی", "midnight": "مشکی", "silver": "نقره‌ای",
    "cosmic-orange": "نارنجی", "orange": "نارنجی", "deep-blue": "آبی سرمه‌ای", "sky-blue": "آبی آسمانی",
    "mist-blue": "آبی روشن", "blue": "آبی", "ultramarine": "آبی کبالتی", "light-gold": "طلایی",
    "lavender": "یاسی", "purple": "بنفش", "pink": "صورتی", "teal": "سبزآبی", "green": "سبز",
    "yellow": "زرد", "starlight": "کرم", "natural-titanium": "تیتانیوم طبیعی", "white-titanium": "تیتانیوم سفید",
    "black-titanium": "تیتانیوم مشکی", "blue-titanium": "تیتانیوم آبی", "desert-titanium": "تیتانیوم شنی",
    "titanium-gray": "تیتانیوم خاکستری", "titanium-black": "تیتانیوم مشکی", "titanium-silverblue": "آبی نقره‌ای",
}


@dataclass(frozen=True)
class Variant:
    """One sellable product: a model in one storage size and color, with its demo commerce data."""

    model: str
    storage: int | None  # GB, None for products without storage
    color: str
    price: int  # toman
    offer: int  # percent
    stock: int
    rate: str


def _variant(brand_prefix, model, storage, color, price, offer, stock, rate):
    return Variant(f"{brand_prefix}-{model}", storage, color, price, offer, stock, rate)


def _v(model, *details):
    """A variant of an Apple product line (the model name is written without the brand prefix)."""
    return _variant("apple", model, *details)


def _samsung(model, *details):
    return _variant("samsung", model, *details)


M = 1_000_000  # one million toman

# The newest products come first.  Every price grows with the storage size and with the generation.
VARIANTS = [
    # 2025
    _v("iphone-17-pro-max", 256, "cosmic-orange", 189 * M, 5, 12, "4.9"),
    _v("iphone-17-pro-max", 512, "deep-blue", 214 * M, 0, 8, "4.9"),
    _v("iphone-17-pro-max", 1024, "silver", 249 * M, 0, 4, "4.8"),
    _v("iphone-17-pro", 256, "silver", 168 * M, 0, 14, "4.9"),
    _v("iphone-17-pro", 512, "deep-blue", 192 * M, 0, 9, "4.8"),
    _v("iphone-air", 256, "sky-blue", 139 * M, 5, 11, "4.8"),
    _v("iphone-air", 512, "space-black", 162 * M, 0, 6, "4.8"),
    _v("iphone-air", 256, "light-gold", 139 * M, 0, 7, "4.7"),
    _v("iphone-17", 256, "lavender", 112 * M, 6, 18, "4.8"),
    _v("iphone-17", 256, "black", 112 * M, 0, 20, "4.8"),
    _v("iphone-17", 512, "mist-blue", 134 * M, 0, 10, "4.7"),
    _v("iphone-16e", 128, "black", 62 * M, 8, 16, "4.6"),
    _v("iphone-16e", 256, "white", 74 * M, 0, 9, "4.5"),
    _samsung("galaxy-s25-ultra", 256, "titanium-silverblue", 118 * M, 6, 10, "4.8"),
    _samsung("galaxy-s25-ultra", 512, "titanium-black", 134 * M, 0, 5, "4.7"),
    _v("ipad-pro-13-m5", 256, "space-black", 138 * M, 0, 6, "4.9"),
    _v("ipad-pro-11-m5", 256, "silver", 108 * M, 0, 8, "4.8"),
    _v("ipad-air-11-m3", 128, "blue", 52 * M, 7, 13, "4.7"),
    _v("ipad-air-11-m3", 256, "purple", 61 * M, 0, 9, "4.6"),
    _v("ipad-a16", 128, "yellow", 29 * M, 10, 19, "4.4"),
    _v("ipad-a16", 256, "pink", 37 * M, 0, 12, "4.3"),
    _v("airpods-pro-3", None, "white", 21_500_000, 0, 15, "4.9"),
    # 2024
    _v("iphone-16-pro-max", 256, "desert-titanium", 142 * M, 10, 7, "4.7"),
    _v("iphone-16-pro", 128, "natural-titanium", 108 * M, 0, 10, "4.7"),
    _v("iphone-16-pro", 256, "white-titanium", 121 * M, 0, 6, "4.6"),
    _v("iphone-16-plus", 128, "ultramarine", 84 * M, 0, 11, "4.5"),
    _v("iphone-16", 128, "pink", 73 * M, 12, 15, "4.6"),
    _v("iphone-16", 256, "teal", 86 * M, 0, 9, "4.5"),
    _samsung("galaxy-s24-ultra", 256, "titanium-gray", 92 * M, 14, 5, "4.5"),
    _v("ipad-pro-13-m4", 256, "silver", 118 * M, 9, 5, "4.7"),
    _v("ipad-pro-11-m4", 256, "space-black", 92 * M, 0, 6, "4.6"),
    _v("ipad-mini-a17-pro", 128, "starlight", 41 * M, 0, 10, "4.6"),
    _v("ipad-mini-a17-pro", 256, "blue", 49 * M, 0, 7, "4.5"),
    _v("airpods-4", None, "white", 11_900_000, 10, 20, "4.5"),
    _v("airpods-4-anc", None, "white", 14_900_000, 0, 14, "4.6"),
    _v("airpods-max-usb-c", None, "midnight", 36 * M, 8, 6, "4.5"),
    _v("airpods-max-usb-c", None, "orange", 36 * M, 0, 4, "4.4"),
    # 2023
    _v("iphone-15-pro-max", 256, "natural-titanium", 112 * M, 12, 6, "4.6"),
    _v("iphone-15-pro-max", 512, "blue-titanium", 131 * M, 0, 4, "4.5"),
    _v("iphone-15-pro", 128, "black-titanium", 88 * M, 0, 7, "4.5"),
    _v("iphone-15-plus", 128, "green", 68 * M, 0, 8, "4.3"),
    _v("iphone-15", 128, "blue", 58 * M, 15, 14, "4.4"),
    _v("airpods-pro-2-usb-c", None, "white", 16_800_000, 12, 18, "4.6"),
]
