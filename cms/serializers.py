from rest_framework import serializers
from django.contrib.auth import get_user_model
from.models import CustomUser, UploadFile
  
User = get_user_model()
  

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ['type','filename','upload_at']


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password','email','user_type']
        