from django.db import models
from django.utils.translation import gettext as _
from decimal import Decimal
from accounts.models import CustomUser


class Category(models.Model):
    category_name = models.CharField(_("دسته بندی"), max_length=50)
    category_code = models.IntegerField(_("کد دسته بندی"), unique=True)
    category_pic = models.ImageField(
        _("عکس دسته بندی"), upload_to="images/category/%Y/%m/%d", blank=True, null=True
    )
    category_slug = models.SlugField(_("یو ار ال دسته بندی"), unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Brand(models.Model):

    brand_name = models.CharField(_("نام برند"), max_length=50)
    category_brand = models.ManyToManyField(Category, verbose_name="دسته بندی برند ها")
    brand_code = models.IntegerField(_("کد برند"))
    brand_pic = models.ImageField(
        _("عکس برند"), upload_to="images/brand/%Y/%m/%d", blank=True, null=True
    )

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"


class Offers(models.Model):
    offer_name = models.CharField(_("تخفیف"), max_length=50)
    offer_pic = models.ImageField(
        _("عکس تخفیف"), upload_to="images/offer/%Y/%m/%d", blank=True, null=True
    )

    def __str__(self):
        return self.offer_name

    class Meta:
        verbose_name = "تخفیف"
        verbose_name_plural = "تخفیفات"


class Info(models.Model):  # اطلاعیه محصول
    product_info = models.TextField(_("اطلاعیه محصول"))

    def __str__(self):
        return self.product_info

    class Meta:
        verbose_name = "اطلاعیه"
        verbose_name_plural = "اطلاعیه ها"


class Product(models.Model):
    bluetooth_choice = (
        ("دارد", "دارد"),
        ("ندارد", "ندارد"),
    )
    product_code = models.IntegerField(_("کد محصول"))  # کد محصول
    product_name = models.CharField(_("نام محصول"), max_length=50)  # نام محصول
    product_color = models.CharField(_("رنگ"), max_length=20)  # رنگ محصول
    product_category = models.ForeignKey(
        Category, verbose_name="دسته بندی", on_delete=models.CASCADE
    )  # دسته بندی محصول
    product_brand = models.ForeignKey(
        Brand, verbose_name="برند", on_delete=models.CASCADE
    )  # برند محصول
    product_number = models.PositiveIntegerField(
        _("تعداد موجود محصول در انبار")
    )  # تعداد محصول
    capability = models.CharField(_("قابلیت محصول"), max_length=20)  # قابلیت
    resolution = models.IntegerField(_("رزولوشون عکس"))  # رزولوشن عکس
    technology = models.CharField(_("تکنولوژی"), max_length=50)  # تکنولوژی
    platform_os = models.CharField(_("سیستم عامل"), max_length=50)  # سیستم عامل
    bluetooth = models.CharField(
        _("بلوتوث"), max_length=20, choices=bluetooth_choice, default=False
    )  # بلوتوث
    product_rate = models.DecimalField(
        _("امتیاز"), max_digits=3, decimal_places=1
    )  # یک رقم اعشار
    specifications = models.TextField(_("مشخصات فنی"))  # مشخصات فنی
    product_description = models.TextField(_("توضیحات تکمیلی"))  # توضیحات تکمیلی
    mini_description = models.CharField(_("توضیح کوتاه"), max_length=50)  # توضیح کوتاه
    price = models.DecimalField(
        _("قیمت محصول"), decimal_places=1, max_digits=10
    )  # قیمت
    offer = models.IntegerField(_("درصد تخفیف"), null=True, blank=True)  # تخفیف
    time_send = models.PositiveIntegerField(_("زمان ارسال"))  # زمان ارسال محصول
    product_offer = models.ForeignKey(
        Offers,
        verbose_name="دسته بندی تخفیفات",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )  # تخفیف عکس محصول
    product_inf = models.ForeignKey(
        Info, verbose_name="اطلاعیه", on_delete=models.CASCADE
    )  # اطلاعیه محصول
    pic = models.ImageField(
        _("عکس اصلی"), upload_to="images/product/%Y/%m/%d", blank=True, null=True
    )  # عکس اصلی
    pic2 = models.ImageField(
        _("عکس 2"),
        upload_to="images/product/productimage/%Y/%m/%d",
        blank=True,
        null=True,
    )  # عکس 1
    pic3 = models.ImageField(
        _("عکس 3"),
        upload_to="images/product/productimage/%Y/%m/%d",
        blank=True,
        null=True,
    )  # عکس 2
    pic4 = models.ImageField(
        _("عکس 4"),
        upload_to="images/product/productimage/%Y/%m/%d",
        blank=True,
        null=True,
    )  # عکس 3
    pic5 = models.ImageField(
        _("عکس 5"),
        upload_to="images/product/productimage/%Y/%m/%d",
        blank=True,
        null=True,
    )  # عکس 4
    create_date = models.DateTimeField(_("زمان ساخت"), auto_now_add=True)  # زمان ساخت
    update_date = models.DateTimeField(_("زمان ویرایش"), auto_now=True)
    slug = models.SlugField(_("یو ار ال محصول"))

    class Meta:
        ordering = ("create_date",)

    @property
    def discounted_price(self):
        if self.offer:
            discount_percent = Decimal(self.offer) / 100
            discount_amount = self.price * discount_percent
            discounted_price = self.price - discount_amount
            return discounted_price
        else:
            return self.price

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class Order(models.Model):
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="نام کاربری مشتری"
    )
    order_date = models.DateTimeField(_("زمان سفارش"), auto_now_add=True)

    def total_cost(self):
        order_items = self.orderitem_set.all()
        total = sum(item.product_cost for item in order_items)
        return total

    def __str__(self):
        return f"Order {self.id} - Customer {self.customer.username}"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="سفارش")
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="نام کاربری مشتری"
    )
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL, verbose_name="محصول"
    )
    product_price = models.DecimalField(
        _("قیمت محصول"), max_digits=10, decimal_places=1
    )
    product_count = models.PositiveIntegerField(_("تعداد محصول"))
    product_cost = models.DecimalField(
        _("هزینه محصول"), max_digits=10, decimal_places=1
    )
    discounted_price = models.DecimalField(
        _("تخفیف محصول"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if self.discounted_price is None:
            self.discounted_price = self.product_price
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "جزئیات سفارش"
        verbose_name_plural = "جزئیات سفارش ها"


class Invoice(models.Model):  # فاکتور

    order = models.ForeignKey(
        Order, null=True, on_delete=models.SET_NULL, verbose_name="اطلاعیه"
    )
    invoice_date = models.DateTimeField(
        _("تاریخ فاکتور"), auto_now_add=True
    )  # تاریخ فاکتور
    authority = models.CharField(_("Authority"), max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "صورت حساب"
        verbose_name_plural = "صورت حساب ها"


class Transaction(models.Model):
    STATUS_CHOICE = (
        ("pending", "انتظار"),
        ("failed", "ناموفق"),
        ("completed", "تکمیل شده"),
    )
    invoice = models.ForeignKey(
        Invoice, null=True, on_delete=models.SET_NULL, verbose_name="فاکتور"
    )  # فاکتور
    transaction_date = models.DateTimeField(
        _("تاریخ تراکنش"), auto_now_add=True
    )  # تاریخ تراکنش
    amount = models.DecimalField(_("مقدار"), max_digits=10, decimal_places=1)  # مقدار
    status = models.CharField(
        _("وضغیت"), max_length=50, choices=STATUS_CHOICE, default="pending"
    )  # وضعیت

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "وضعیت سفارش"
        verbose_name_plural = "وضعیت سفارش ها"


class Comment(models.Model):
    username = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="نام کاربری"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    comment = models.TextField(_("کامنت"))
    rate = models.PositiveIntegerField(_("امتیاز به محصول"), default=False)
    created_date = models.DateTimeField(_("تاریخ ساخت کامنت"), auto_now_add=False)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"


class Contact_product(models.Model):
    username = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="نام کاربری"
    )
    message_product = models.TextField(_("نظر در مورد محصول"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")

    def __str__(self):
        return self.message_product

    class Meta:
        verbose_name = "نظرات در محصولات"
        verbose_name_plural = "نظرات در مورد محصولات"
