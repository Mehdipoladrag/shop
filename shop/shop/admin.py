from django.contrib import admin
from shop.models import Product, Category, Contact_product, Brand, Offers , Info, Invoice, Order , OrderItem, Comment, Transaction
from django.utils.html import format_html
# Register your models here.
class CategoryAdmin(admin.ModelAdmin) : 
    list_display = ['category_code', 'category_name', 'category_slug', 'slug_cat']
    list_display_links = ['category_code', 'category_name', 'slug_cat']
    def slug_cat(self, obj):
        url_cat = 'http://127.0.0.1:8000/shop/'
        return format_html("<a href='{url}{slug}'>{url}{slug}</a>", url=url_cat, slug=obj.category_slug)

    slug_cat.short_description = 'آدرس دسته بندی'


    
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ['product_code','product_name', 'product_brand','formatted_price', 'offer', 'discounted_price', 'slug_product']
    search_fields = ['product_name']
    list_display_links = ['product_name', 'product_brand']
    list_filter = ['product_brand','product_category']
    readonly_fields = ['create_date', 'update_date']
    list_per_page = 10
    fieldsets = (
        ("مشخصات محصول", {
            "fields": (
                'product_code' , 'product_name' , 'product_brand', 'product_category', 'product_color',
                'product_number', 'technology', 'resolution', 'capability', 'platform_os', 'bluetooth','product_rate',
                'slug','time_send', 'product_offer', 'product_inf'
            ), 
        }),
        ("قیمت محصول", {
            "fields": (
                'price' , 'offer' ,
            ),
        }),
        ("توضیحات محصول", {
            "fields": (
                'mini_description' , 'product_description' , 'specifications', 'create_date', 'update_date'
            ),
        }),
        ("عکس های محصول", {
            "fields": (
                'pic' , 'pic2' , 'pic3', 'pic4', 'pic5',
            ),
        }),
    )
    def slug_product(self, obj):
        url_product = 'http://127.0.0.1:8000/shop/product/'
        return format_html("<a href='{url}{slug}'>{url}{slug}</a>", url=url_product, slug=obj.slug)

    slug_product.short_description = 'آدرس محصول'
    def formatted_price(self, obj):
        return '{:,.0f}'.format(obj.price)

    # عنوان فیلد نمایش داده شده در صفحه ادمین
    formatted_price.short_description = 'قیمت اصلی'

    def discounted_price(self, obj):
        return '{:,.0f}'.format(obj.discounted_price)

    discounted_price.short_description = 'قیمت با تخفیف'
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0
    readonly_fields = ('custom_pk', 'invoice_date')

    def custom_pk(self, obj):
        return obj.pk

    custom_pk.short_description = 'شماره صورت حساب'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date')
    readonly_fields = ('order_date',)
    inlines = [OrderItemInline, InvoiceInline]


class BrandsAdmin(admin.ModelAdmin) : 
    list_display = ['brand_code', 'brand_name']
    filter_horizontal = ['category_brand']
    list_display_links =  ['brand_code', 'brand_name']




admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandsAdmin)
admin.site.register(Offers)
admin.site.register(Info)
admin.site.register(Invoice)
admin.site.register(Transaction)
admin.site.register(Contact_product)
admin.site.register(Comment)

