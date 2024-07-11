from rest_framework import serializers
from shop.models import (
    Category, 
    Brand,
)


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