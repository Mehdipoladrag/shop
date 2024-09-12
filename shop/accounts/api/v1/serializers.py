from rest_framework import serializers
from accounts.models import CustomProfileModel, CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from jalali_date import datetime2jalali
from shop.models import Order
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


class UserOrderSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(slug_field="username", read_only=True)
    order_persian_date = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    street = serializers.SerializerMethodField()
    def get_order_persian_date(self, obj):
        return datetime2jalali(obj.order_date).strftime("%Y/%m/%d %H:%M")
    
    def get_first_name(self, obj):
        return obj.customer.first_name
    
    def get_last_name(self, obj):
        return obj.customer.last_name
    
    def get_city(self, obj):
        return getattr(obj.customer.customprofilemodel, 'city', 'N/A') 
    
    def get_street(self, obj): 
        return getattr(obj.customer.customprofilemodel, 'street', 'N/A')

    class Meta:
        model = Order
        fields = [
            "customer",
            "order_persian_date",
            "first_name",
            "last_name",
            "city",
            "street"
        ]
    
class UserCompleteSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name') 
    last_name = serializers.CharField(source='user.last_name')  
    username = serializers.CharField(source ='user.username' )
    uuid = serializers.CharField(source='user.uuid')

    class Meta:
        model = CustomProfileModel  # The serializer should work with CustomProfileModel
        fields = [
            "username",
            "uuid",
            "first_name",
            "last_name",
        ]