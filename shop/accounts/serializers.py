from rest_framework import serializers 
from accounts.models import CustomProfileModel , CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class ProfileSerializer(serializers.ModelSerializer) :
  class Meta : 
    model = CustomProfileModel
    fields = '__all__'

class UserSerializer(serializers.ModelSerializer) : 
  class Meta : 
    model = CustomUser
    fields = '__all__'
