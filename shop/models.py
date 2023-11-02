from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from decimal import Decimal

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_code = models.IntegerField(_("Code"))
    first_name = models.CharField(_("Name"), max_length=20)
    last_name = models.CharField(_("last name"), max_length=20)
    address = models.TextField(_("Address"))
    zipcode = models.CharField(_("Zip Code"), max_length=20)
    state = models.CharField(_("State"), max_length=20)
    city = models.CharField(_("City"), max_length=20)
    mobile = models.CharField(_("Mobile"), max_length=20)
    email = models.EmailField(_("Email"), max_length=254)
    age = models.PositiveIntegerField(_("Age"))
    gender = models.BooleanField(_("Gender"), default=False)
    shomare_shaba = models.IntegerField(_("shomare_shaba"))
    shomare_cart = models.IntegerField(_("shomare_cart"))
    back_money = models.CharField(
        _("Back money"), max_length=50, default='شماره شبا')
    customer_image = models.ImageField(
        _("User Image"), upload_to='images/userimage/%Y/%m/%d', blank=True, null=True)  # عکس یوزر

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(_("Category"), max_length=50)
    category_code = models.IntegerField(_("Category Code"))
    category_pic = models.ImageField(_("Category Image"), upload_to='images/category/%Y/%m/%d', blank=True, null=True)
    category_slug = models.SlugField(_("Category slug"), unique=True)

    def __str__(self):
        return self.category_name


class Brand(models.Model):

    brand_name = models.CharField(_("Brand Name"), max_length=50)
    category_barnd = models.ManyToManyField(
        Category)
    brand_code = models.IntegerField(_("Brand_code"))
    brand_pic = models.ImageField(
        _("Brand Image"), upload_to='images/brand/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.brand_name
class Offers(models.Model) :
    offer_name = models.CharField(_("Offer Name"), max_length=50)
    offer_pic = models.ImageField(_("Offer Image"), upload_to='images/offer/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.offer_name
class Info(models.Model) : # اطلاعیه محصول
    product_info = models.TextField(_("Info Product"))

    def __str__(self):
        return self.product_info
class Product(models.Model):
    bluetooth_choice = (
        ('دارد', 'دارد'),
        ('ندارد', 'ندارد'),
    )
    product_code = models.IntegerField(_("Product Code"))  # کد محصول
    product_name = models.CharField(_("Product Name"), max_length=20)  # نام محصول
    product_color = models.CharField(_("Color"), max_length=20)  # رنگ محصول
    product_category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)  # دسته بندی محصول
    product_brand = models.ForeignKey(Brand, verbose_name='Brand', on_delete=models.CASCADE)  # برند محصول
    product_number = models.PositiveIntegerField(_("Product Number"))  # تعداد محصول
    capability = models.CharField(_("capability Name"), max_length=20)  # قابلیت
    resolution = models.IntegerField(_("Resolution"))  # رزولوشن عکس
    technology = models.CharField(_("technology"), max_length=50)  # تکنولوژی
    platform_os = models.CharField(_("Os"), max_length=50)  # سیستم عامل
    bluetooth = models.CharField(_("Bluetooth"), max_length=20, choices=bluetooth_choice, default=False)  # بلوتوث
    product_rate = models.IntegerField(_("Rate"))
    specifications = models.TextField(_("Specifictaion"))  # مشخصات فنی
    product_description = models.TextField(_("Description"))  # توضیحات تکمیلی
    mini_description = models.CharField(_("Mini Description"), max_length=50)  # توضیح کوتاه
    price = models.DecimalField(_("Product Price"), decimal_places=1, max_digits=10)  # قیمت
    offer = models.IntegerField(_('offer'),null=True, blank=True)  # تخفیف
    time_send = models.PositiveIntegerField(_("Time Send")) # زمان ارسال محصول
    product_offer = models.ForeignKey(Offers, verbose_name='Offers', on_delete=models.CASCADE, null=True, blank=True)     # تخفیف عکس محصول
    product_inf = models.ForeignKey(Info, verbose_name='Info', on_delete=models.CASCADE) # اطلاعیه محصول
    pic = models.ImageField(_("Image"), upload_to='images/product/%Y/%m/%d', blank=True, null=True)  # عکس اصلی
    pic2 = models.ImageField(_("Image2"), upload_to='images/product/productimage/%Y/%m/%d', blank=True, null=True)  # عکس 1
    pic3 = models.ImageField(_("Image3"), upload_to='images/product/productimage/%Y/%m/%d', blank=True, null=True)  # عکس 2
    pic4 = models.ImageField(_("Image4"), upload_to='images/product/productimage/%Y/%m/%d', blank=True, null=True)  # عکس 3
    pic5 = models.ImageField(_("Image5"), upload_to='images/product/productimage/%Y/%m/%d', blank=True, null=True)  # عکس 4
    create_date = models.DateTimeField(_("Created At"), auto_now_add=True)  # زمان ساخت
    update_date = models.DateTimeField(_("Update At"), auto_now=True)
    slug = models.SlugField(_("slug"))

    class Meta:
        ordering = ('create_date',)

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
    


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(_("Order Date"), auto_now_add=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    product_price = models.DecimalField(
        _("Product Price"), max_digits=10, decimal_places=1)
    product_count = models.PositiveIntegerField(_("Product Count"))
    product_cost = models.DecimalField(
        _("Product cost"), max_digits=10, decimal_places=1)

    def __str__(self):
        return str(self.id)


class Invoice(models.Model):  # فاکتور
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    invoice_date = models.DateTimeField(auto_now_add=True)  # تاریخ فاکتور
    authority = models.CharField(
        _("Authority"), max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Transaction(models.Model):
    STATUS_CHOICE = (
        ('pending', 'انتظار'),
        ('failed', 'ناموفق'),
        ('completed', 'تکمیل شده')
    )
    invoice = models.ForeignKey(
        Invoice, null=True, on_delete=models.SET_NULL)  # فاکتور
    transaction_date = models.DateTimeField(auto_now_add=True)  # تاریخ تراکنش
    amount = models.DecimalField(
        _("amount"), max_digits=10, decimal_places=1)  # مقدار
    status = models.CharField(
        _("Status"), max_length=50, choices=STATUS_CHOICE, default='pending')  # وضعیت

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=False)
    created_date = models.DateTimeField(auto_now_add=False)
    def __str__(self):
        return self.comment
    
    



class Contact_product(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    message_product = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.message_product
