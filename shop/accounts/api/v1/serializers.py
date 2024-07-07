from rest_framework import serializers 
from accounts.models import CustomProfileModel , CustomUser
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
  """ Serializer For User """
  class Meta: 
    model = CustomUser
    fields = ['id', 'username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'groups', 'is_superuser', 'is_staff', 'is_active']


class UserProfileSerializer(serializers.ModelSerializer):
  """ Nested Serializer For Profile and Users """
  user = UserSerializer()
  class Meta: 
    model = CustomProfileModel
    fields = ['user', 'mobile','national_code', 'address', 'zipcode', 'street', 'city', 'age','gender', 'card_number', 'iban', 'back_money', 'customer_image', 'is_complete']



class UserDataSerializer(serializers.ModelSerializer): 

  """Serializer For Create User and Update User"""

  password = serializers.CharField(write_only=True)
  class Meta:
    model = CustomUser
    fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'last_login', 'date_joined', 'groups']

  def create(self, validated_data):
    validated_data['password'] = make_password(validated_data['password'])
    return super().create(validated_data)

  def update(self, instance, validated_data):
    if 'password' in validated_data:
      validated_data['password'] = make_password(validated_data['password'])
    return super().update(instance, validated_data)


class UserProfileDataSerializer(serializers.ModelSerializer): 
  class Meta: 
    model = CustomProfileModel
    fields = ['user', 'mobile','national_code', 'address', 'zipcode', 'street', 'city', 'age','gender', 'card_number', 'iban', 'back_money', 'customer_image', 'is_complete']