from lib2to3.pgen2.tokenize import TokenError
from xmlrpc.client import ResponseError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.http import HttpResponse

from kpi.api.serializers import *

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

User = get_user_model()

class DogBreedList(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get_object():
        return DogBreed.objects.all()

    def get(self,request):
        dog_breed = self.get_object()
        serializer = DogBreedSerializer(dog_breed,many=True)
        return Response(serializer.data)
        
    @action(detail=False,methods=["post"])
    def post(self,request):
        cleaned_data = request.cleaned_data
        dog_breed = cleaned_data.get("dog_breed",None)
        if dog_breed is not None:
            dog_breed = dog_breed.lower()
            dog_breed,created = DogBreed.objects.get_or_create(dog_breed=dog_breed)
            serializer = UserSerializer(serializer.data)
            return Response(serializer.data)


    class Meta:
        fields = "__all__"


class DogBreedDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self, pk):
        try:
            return DogBreed.objects.get(pk=pk)
        except DogBreed.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = DogBreedSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = DogBreedSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pass
    
class LoginViewSet(ModelViewSet,TokenObtainPairView):
    serializer_class = LoginSerializer 
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self,request, *args, **kwargs):
        logger.info(request.data)
        print(request.data)
        serializer = self.get_serializer(data=request.data,context={"request":request})
        print(serializer.is_valid())
        try:
            print("TRY")
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            print(e)
            raise InvalidToken(e.args[0])
        
        print("response")
        return Response(serializer.validated_data,status=status.HTTP_200_OK)


class RefreshViewSet(ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,context={"request":request})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        return Response(serializer.validated_data,status=status.HTTP_200_OK)


class UserAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    def get_object(self,pk):
        user = User.objects.get(pk = pk)
        if self.pk == user.pk:
            return user
        else: 
            return PermissionError

    def get(self,request):
        user = self.get_object(request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
    @action(detail=False,methods=["post"])
    def post(self,validated_data):
        logger.info("creating user validated data",validated_data)
        register_user_data = new_user(validated_data)
        if register_user_data:
           serializer = UserSerializer(serializer.data)
           return Response(serializer.data)

    def update(self, instance,validated_data):
        #user = get_object(validated_data)
        pass

    class Meta:
        fields = "__all__"



# PING SERVER 
class PING(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        return Response({"info":"Hello world"})