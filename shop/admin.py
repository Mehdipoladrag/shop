from django.contrib import admin
import locale
from shop.models import Product, Category, Contact_product, Brand, Offers , Info, Invoice, Order , OrderItem, Comment, Transaction
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    # فیلدهایی که می‌خواهید در صفحه ادمین نمایش داده شوند
    # فیلدهایی که می‌خواهید در صفحه ادمین نمایش داده شوند
    list_display = ('product_name', 'product_brand',
                    'formatted_price', 'offer', 'discounted_price', 'slug')

    def formatted_price(self, obj):
        return '{:,.2f}'.format(obj.price)

    # عنوان فیلد نمایش داده شده در صفحه ادمین
    formatted_price.short_description = 'Price'

    def discounted_price(self, obj):
        return '{:,.2f}'.format(obj.discounted_price)

    discounted_price.short_description = 'Discounted Price'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date')
    readonly_fields = ('order_date',) 



class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Offers)
admin.site.register(Info)
admin.site.register(Invoice)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Transaction)
admin.site.register(Contact_product)
admin.site.register(Comment)

