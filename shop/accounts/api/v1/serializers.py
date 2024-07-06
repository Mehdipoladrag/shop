from rest_framework import serializers 
from accounts.models import CustomProfileModel , CustomUser



class UserSerializer(serializers.ModelSerializer):
  """ Serializer For User """
  class Meta: 
    model = CustomUser
    fields = ['id', 'username', 'first_name', 'last_name', 'last_login', 'date_joined', 'groups']



class UserProfileSerializer(serializers.ModelSerializer):
  """ Nested Serializer For Profile and Users """
  user = UserSerializer()
  class Meta: 
    model = CustomProfileModel
    fields = ['user', 'mobile','national_code', 'address', 'zipcode', 'street', 'city', 'age','gender', 'card_number', 'iban', 'back_money', 'customer_image', 'is_complete']