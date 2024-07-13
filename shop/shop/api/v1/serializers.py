from rest_framework import serializers
from shop.models import (
    Category, 
    Brand,
    Product,
    Order,
    OrderItem, 
)
from jalali_date import datetime2jalali


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer For Category And Images """
    category_pic = serializers.ImageField()

    class Meta:
        model = Category
        fields = [
            "id",
            "category_name",
            "category_code",
            "category_pic",
            "category_slug",
        ]


class BrandSerializer(serializers.ModelSerializer): 
    """ Serializer For Brand And Images """
    brand_pic = serializers.ImageField()
    category_brand = serializers.SlugRelatedField(
        many=True,
        slug_field='category_name',
        queryset=Category.objects.all()
    )
    class Meta:
        model = Brand 
        fields = [
            "id",
            "brand_name", 
            "category_brand", 
            "brand_code", 
            "brand_pic"
        ]


class ProductSerializer(serializers.ModelSerializer):
    product_category = serializers.StringRelatedField()
    product_brand = serializers.StringRelatedField()
    
    class Meta: 
        model = Product
        fields = [
            "product_code", 
            "product_name",
            "product_category",
            "product_brand",
            "product_number",
            "capability",
            "resolution",
            "technology",
            "platform_os",
            "bluetooth",   
            "product_rate",
            "specifications",
            "mini_description",
            "product_description",
            "price",
            "offer", 
            "time_send",
            "product_offer",
            "product_inf", 
            "pic",
            "pic2",
            "pic3",
            "pic4",
            "pic5",
            "create_date",
            "update_date",
            "slug",
        ]


class ProductPostSerializer(serializers.ModelSerializer): 
    product_category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()),
    product_brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all()),
    pic = serializers.ImageField(required = True)
    class Meta: 
        model = Product
        fields = [
            "product_code",
            "product_name", 
            "product_color", 
            "product_category",
            "product_brand",
            "product_number", 
            "capability",
            "resolution", 
            "technology",
            "platform_os",
            "bluetooth",
            "product_rate",
            "specifications", 
            "product_description", 
            "mini_description", 
            "price", 
            "offer",
            "time_send", 
            "pic", 
            "slug",
            "product_inf",
        ]


class OrderSerializer(serializers.ModelSerializer): 
    customer = serializers.SlugRelatedField(
        slug_field= 'username',
        read_only = True
    )
    order_persian_date = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    class Meta: 
        model = Order 
        fields = [
            "customer", 
            "order_date",
            "order_persian_date",
            "total_cost",
        ]
    def get_order_persian_date(self, obj):
        return datetime2jalali(obj.order_date).strftime('%Y/%m/%d %H:%M')
    
    def get_total_cost(self, obj):
        order_items = obj.orderitem_set.all()
        total = sum(item.product_cost for item in order_items)  
        return '{:,.0f}'.format(total)

class OrderItemSerializer(serializers.ModelSerializer): 
    order = OrderSerializer()
    product = serializers.SlugRelatedField(
        slug_field='product_name',
        read_only= True, 
    )
    class Meta: 
        model = OrderItem
        fields = [
            "order", 
            "product",
            "product_price", 
            "product_count", 
            "product_cost",
            "discounted_price",
        ]
