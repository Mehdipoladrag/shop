from rest_framework import serializers
from accounts.models import CustomProfileModel, CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
#

class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    Serializer for Login for token.
    Checks a username and password.
    If the username exists in Users and the user is a superuser or admin,
    the user can access the token.
    """
    username = serializers.CharField(required=False)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not password:
            raise serializers.ValidationError("Please enter a valid password")

        if not username:
            raise serializers.ValidationError("Please enter a username")

        user = None
        if username:
            user = authenticate(username=username, password=password)
        

        if user and (user.is_staff or user.is_superuser):
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
            }
            return data
        raise serializers.ValidationError("You are not authorized to access this page")
    
class UserSerializer(serializers.ModelSerializer):
    """Serializer For User"""

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "last_login",
            "date_joined",
            "groups",
            "is_superuser",
            "is_staff",
            "is_active",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """Nested Serializer For Profile and Users"""

    user = UserSerializer()

    class Meta:
        model = CustomProfileModel
        fields = [
            "user",
            "mobile",
            "national_code",
            "address",
            "zipcode",
            "street",
            "city",
            "age",
            "gender",
            "card_number",
            "iban",
            "back_money",
            "customer_image",
            "is_complete",
        ]


class UserDataSerializer(serializers.ModelSerializer):
    """Serializer For Create User and Update User"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "last_login",
            "date_joined",
            "groups",
        ]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class UserProfileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomProfileModel
        fields = [
            "user",
            "mobile",
            "national_code",
            "address",
            "zipcode",
            "street",
            "city",
            "age",
            "gender",
            "card_number",
            "iban",
            "back_money",
            "customer_image",
            "is_complete",
        ]
