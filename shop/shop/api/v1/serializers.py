from rest_framework import serializers
from shop.models import (
    Category, 
    Brand,
    Product,
    Order,
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
    order_date_jalali = serializers.SerializerMethodField()
    class Meta: 
        model = Order 
        fields = [
            "customer", 
            "order_date",
            "order_date_jalali",
        ]
    def get_order_date_jalali(self, obj):
        return datetime2jalali(obj.order_date).strftime('%Y/%m/%d %H:%M')