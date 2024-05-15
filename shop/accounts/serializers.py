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

from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
      user = CustomUser.objects.filter(username=attrs['username']).first()
      if user and user.check_password(attrs['password']):
        refresh = RefreshToken.for_user(user)
        new_access_token = str(refresh.access_token)
        new_refresh_token = str(refresh)
        if user.is_superuser:
          new_access_token = 'admin_' + new_access_token
          new_refresh_token = 'admin_' + new_refresh_token
        else : 
          new_access_token = str(refresh.access_token)
          new_refresh_token = str(refresh)
        return {
          'username': user.username,
          'email': user.email,
          'access_token': new_access_token,
          'refresh_token': new_refresh_token
        }
      raise serializers.ValidationError("Incorrect username or password")