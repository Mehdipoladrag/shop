from rest_framework import serializers
from shop.models import (
    Category,
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
