from django.contrib import admin
import locale
from shop.models import Product, Category, Contact_product, Brand, Offers , Info, Invoice, Order , OrderItem, Comment, Transaction
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    
    list_display = ['product_name', 'product_brand','formatted_price', 'offer', 'discounted_price', 'slug']
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
    
    def formatted_price(self, obj):
        return '{:,.2f}'.format(obj.price)

    # عنوان فیلد نمایش داده شده در صفحه ادمین
    formatted_price.short_description = 'Price'

    def discounted_price(self, obj):
        return '{:,.2f}'.format(obj.discounted_price)

    discounted_price.short_description = 'Discounted Price'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date')
    readonly_fields = ('order_date',) 
    inlines = [OrderItemInline]
    verbose_name = 'عمومی'
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Offers)
admin.site.register(Info)
admin.site.register(Invoice)
admin.site.register(Transaction)
admin.site.register(Contact_product)
admin.site.register(Comment)

