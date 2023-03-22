from datetime import datetime
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.serializers import ModelSerializer

from kpi.models import DogBreed, Department, DogPhoto, PhotoClick, InfoRequest, User
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class DogBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogBreed
        exclude = []

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = []

class DogPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogPhoto
        exclude = []

class PhotoClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoClick 
        exclude = []


class InfoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoRequest
        exclude = []


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]

class LoginSerializer(TokenObtainPairSerializer):
    
    def validate(self,attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["username"] = UserSerializer(self.user).data 
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data 