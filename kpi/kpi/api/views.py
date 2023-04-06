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
from django.utils import timezone
from kpi.api.serializers import *

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
from django.contrib.auth import get_user_model
User = get_user_model()


class DogBreedList(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    

    def get_object():
        return DogBreed.objects.all()

    def get(self,request):
        dog_breed = self.get_object()
        serializer = DogBreedSerializer(dog_breed,many=True)
        return Response(serializer.data)
        
    @action(detail=False,methods=["post"])
    def post(self,request):
        cleaned_data = request.data
        dog_breed = cleaned_data.get("breed",None)
        if dog_breed is not None:
            dog_breed = dog_breed.lower()
            dog_breed,created = DogBreed.objects.get_or_create(breed=dog_breed,created_at=timezone.now())
            serializer = DogBreedSerializer(dog_breed)
            return Response(serializer.data)
        else:
            return Response("dog breed is none")

    class Meta:
        fields = "__all__"


class DogBreedDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]

    def get_object(self, pk):
        try:
            return DogBreed.objects.get(pk=pk)
        except DogBreed.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        dog_breed = self.get_object(pk)
        serializer = DogBreedSerializer(dog_breed)
        return Response(serializer.data)

    def put(self, request, pk):
        dog_breed = self.get_object(pk)
        breed = request.data.get("breed",None)
        if dog_breed is not None and dog_breed.breed != breed:
            dog_breed.breed = breed
            dog_breed.save()
        serializer = DogBreedSerializer(dog_breed, data=request.data)
        return Response(serializer.data)

    def delete(self, request, pk):
        pass

class DogList(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object():
        return Dog.objects.all()

    def get(self,request):
        dog = self.get_object()
        serializer = DogSerializer(dog,many=True)
        return Response(serializer.data)
        
    @action(detail=False,methods=["post"])
    def post(self,request):
        cleaned_data = request.data
        dog_id = cleaned_data.get("dog_id",None)
        dog_breed = cleaned_data.get("dog_breed",None)
        dog_name = cleaned_data.get("dog_name",None)
        dog_weight_lbs = cleaned_data.get("dog_weight_lbs",None)
        dog_shelter_date_enter = cleaned_data.get("dog_shelter_date_enter",timezone.now())
        dog_adoption_date = cleaned_data.get("dog_adoption_date",None)
        dog_bio = cleaned_data.get("dog_bio",None)
        if dog_breed is not None:
            dog_breed = dog_breed.lower()
            dog_breed,created = DogBreed.objects.get_or_create(dog_breed=dog_breed)
        dog = Dog.objects.create(dog_id=dog_id,dog_breed=dog_breed,dog_name=dog_name,dog_weight_lbs=dog_weight_lbs,
                                 dog_shelter_date_enter=dog_shelter_date_enter,dog_adoption_date=dog_adoption_date,
                                 dog_bio=dog_bio)
        dog.save()
        serializer = DogSerializer(dog)
        return Response(serializer.data)


    class Meta:
        fields = "__all__"


class DogDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object(self, pk=None,dog_id=None):
        if pk is not None:
            try:
                return DogBreed.objects.get(pk=pk)
            except DogBreed.DoesNotExist:
                raise Http404
        elif dog_id is not None:
            try:
                return DogBreed.objects.get(dog_id=dog_id)
            except DogBreed.DoesNotExist:
                raise Http404
        else:
            return HTTP404

    def get(self, request, pk=None,dog_id=None):
        dog = self.get_object(pk=pk,dog_id=dog_id)
        serializer = DogSerializer(dog)
        return Response(serializer.data)

    def put(self, request, pk=None,dog_id=None):
        dog = self.get_object(pk=pk,dog_id=dog_id)
        cleaned_data = request.data
        dog_breed = cleaned_data.get("dog_breed",None)
        dog_name = cleaned_data.get("dog_name",dog.dog_name)
        dog_weight_lbs = cleaned_data.get("dog_weight_lbs",dog.dog_weight_lbs)
        dog_shelter_date_enter = cleaned_data.get("dog_shelter_date_enter",dog.dog_shelter_date_enter)
        dog_adoption_date = cleaned_data.get("dog_adoption_date",dog.dog_adoption_date)
        dog_bio = cleaned_data.get("dog_bio",dog.dog_bio)
        if dog_breed is not None:
            dog_breed = dog_breed.lower()
            dog_breed,created = DogBreed.objects.get_or_create(dog_breed=dog_breed)
        else:
            dog_breed = dog.dog_breed


        dog.dog_breed = dog_breed
        dog.dog_name = dog_name
        dog.dog_weight_lbs = dog_weight_lbs
        dog.dog_shelter_date_enter = dog_shelter_date_enter
        dog.dog_adoption_date = dog_adoption_date
        dog.dog_bio=dog_bio
        dog.save()
        serializer = DogSerializer(dog)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pass



class DogPhotoList(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object():
        return DogPhoto.objects.all()

    def get(self,request):
        dog_photos = self.get_object()
        serializer = DogPhotoSerializer(dog_photos,many=True)
        return Response(serializer.data)
        
    @action(detail=False,methods=["post"])
    def post(self,request):
        cleaned_data = request.data
        dog_id = cleaned_data.get("dog_id",None)
        if dog_id is not None:
            dog = Dog.objects.get(dog_id=dog_id)
            photo = cleaned_data.get("photo",None)
            dog_photo = DogPhoto.objects.create(dog=dog,photo=photo)
            dog_photo.save()
            serializer = DogPhotoSerializer(dog_photo)
            return Response(serializer.data)


    class Meta:
        fields = "__all__"

class DogPhotoDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object(self,pk=None):
        return DogPhoto.objects.get(pk=pk)

    def get(self,request):
        dog_breed = self.get_object()
        serializer = DogPhotoSerializer(dog_breed,many=True)
        return Response(serializer.data)
        
    @action(detail=False,methods=["post"])
    def put(self,request):
        cleaned_data = request.data
        dog_photo_id = cleaned_data.get("dog_photo_id",None)
        
        if dog_photo_id is not None:
            dog_photo = DogPhoto.objects.get(dog_photo_id=dog_photo_id)
            photo = cleaned_data.get("photo",dog.photo)
            dog = cleaned_data.get("dog",dog.dog)

            dog_photo.photo = photo
            dog_photo.dog = dog 
            dog_photo.save()
        serializer = DogPhotoSerializer(dog_photo)
        return Response(serializer.data)


    class Meta:
        fields = "__all__"



class PhotoClickList(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object():
        return PhotoClickList.objects.all()

    def get(self,request):
        photo_clicks = self.get_object()
        serializer = PhotoClickSerializer(photo_clicks,many=True)
        return Response(serializer.data)
        
    @action(detail=False,methods=["post"])
    def post(self,request):
        cleaned_data = request.data
        dog_photo_id = cleaned_data.get("dog_photo_id",None)
        click_date = cleaned_data.get("click_date",timezone.now)
        user_info = cleaned_data.get("user_info",None)
        if dog_photo_id is not None:
            dog_photo = DogPhoto.objects.get(dog_photo_id=dog_photo_id)
            photo_click = PhotoClick.objects.create(dogo_photo=dog_photo,click_date=click_date,user_info=user_info)
            photo_click.save()
            serializer = PhotoClickSerializer(photo_click)
            return Response(serializer.data)


    class Meta:
        fields = "__all__"


class PhotoClickDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object(self, pk):
        try:
            return PhotoClick.objects.get(pk=pk)
        except PhotoClick.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        photo_click = self.get_object(pk)
        serializer = PhotoClickSerializer(photo_click)
        return Response(serializer.data)


    def put(self, request, pk):
        # for now i don't see a reason to have a put request for photo click
        pass 


    def delete(self, request, pk):
        pass
    


class InfoRequestList(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object():
        return InfoRequest.objects.all()

    def get(self,request):
        info_requested = self.get_object()
        serializer = InfoRequestSerializer(info_requested,many=True)
        return Response(serializer.data)
        
    @action(detail=False,methods=["post"])
    def post(self,request):
        cleaned_data = request.data
        dog_id = cleaned_data.get("dog_id",None)
        request_time = cleaned_data.get("request_time",timezone.now)
        dog_adopted = cleaned_data.get("dog_adopted",False)
        if dog_id is not None:
            dog = Dog.objects.get(dog_id=dog_id)
            info_requested  = InfoRequest.objects.create(dog=dog,request_time=request_time,dog_adopted=dog_adopted)
            info_requested.save()

            serializer = InfoRequestSerializer(info_requested)
            return Response(serializer.data)


    class Meta:
        fields = "__all__"


class InfoRequestkDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object(self, pk):
        try:
            return InfoRequest.objects.get(pk=pk)
        except InfoRequest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        info_requested = self.get_object(pk)
        serializer = InfoRequestSerializer(info_requested)
        return Response(serializer.data)

    def put(self, request, pk):
        cleaned_data = request.data
        info_requested = self.get_object(pk)
        dog_id = cleaned_data.get("dog_id",None)
        request_time = cleaned_data.get("request_time",dog.request_time)
        dog_adopted = cleaned_data.get("dog_adopted",dog.dog_adopted)
        if dog_id is not None:
            dog = Dog.objects.get(dog_id=dog_id)
        else:
            dog = info_requested.dog 

        info_requested.dog=dog
        info_requested.request_time=request_time
        info_requested.dog_adopted=dog_adopted
        info_requested.save()

        serializer = InfoRequestSerializer(info_requested)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pass
    

class BillTypeList(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object():
        return BillType.objects.all()

    def get(self,request):
        bill_type = self.get_object()
        serializer = BillType(bill_type,many=True)
        return Response(serializer.data)
        
    @action(detail=False,methods=["post"])
    def post(self,request):
        cleaned_data = request.data
        bill_type = cleaned_data.get("bill_type",None)
        if bill_type is not None:
            bill_type = bill_type.lower()
            bill_type,created = BillType.objects.get_or_create(bill_type=bill_type)
            serializer = BillTypeSerializer(bill_type)
            return Response(serializer.data)


    class Meta:
        fields = "__all__"


class BillDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object(self, pk):
        try:
            return Bill.objects.get(pk=pk)
        except Bill.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        bill = self.get_object(pk)
        serializer = BillSerializer(bill)
        return Response(serializer.data)

    def put(self, request, pk):
        bill = self.get_object(pk)
        cleaned_data = request.data 
        bill_type = cleaned_data.get("bill_type",None)
        dog_id = cleaned_data.get("dog_id",None)
        bill_amount = cleaned_data.get("bill_amount",None)
        bill_date = cleaned_data.get("bill_date")
        if bill_type is not None:
            bill_type = BillType.objects.get(bill_type=bill_type.lower())
        else:
            bill_type = bill.bill_type
        if dog_id is not None:
            dog = Dog.objects.get(dog_id = dog_id)
        else:
            dog = bill.dog 
        
        bill.bill_type = bill_type
        bill.dog = dog 
        bill.bill_amount = bill_amount
        bill.bill_date = bill_date
        bill.save()
        serializer = BillSerializer(bill)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pass
    

class BillList(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object():
        return Bill.objects.all()

    def get(self,request):
        bill = self.get_object()
        serializer = BillSerializer(bill,many=True)
        return Response(serializer.data)
        
    @action(detail=False,methods=["post"])
    def post(self,request):
        cleaned_data = request.data 
        bill_type = cleaned_data.get("bill_type",None)
        dog_id = cleaned_data.get("dog_id",None)
        bill_amount = cleaned_data.get("bill_amount",None)
        bill_date = cleaned_data.get("bill_date")
        if bill_type is not None:
            bill_type = BillType.objects.get(bill_type=bill_type.lower())
        if dog_id is not None:
            dog = Dog.objects.get(dog_id = dog_id)
        bill = Bill.objects.create(bill_type=bill_type,dog=dog,bill_amount=bill_amount,bill_date=bill_date)
        bill.save()
        serializer = BillSerializer(bill)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    class Meta:
        fields = "__all__"




class DonationList(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object():
        return Donation.objects.all()

    def get(self,request):
        donation = self.get_object()
        serializer = DonationSerializer(donation,many=True)
        return Response(serializer.data)
        
    @action(detail=False,methods=["post"])
    def post(self,request):
        cleaned_data = request.data
        dog_id = cleaned_data.get("dog_id",None)
        amount = cleaned_data.get("amount",None)
        donation_date = cleaned_data.get("donation_date",timezone.now())
        if dog_id is not None:
            dog = Dog.objects.get(dog_id=dog_id)
        else:
            dog = None
        donation = Donation.objects.create(dog=dog,amount=amount,donation_date=donation_date)
        donation.save()
        serializer = DonationSerializer(donation)
        return Response(serializer.data)


    class Meta:
        fields = "__all__"


class DonationDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
    def get_object(self, pk):
        try:
            return Donation.objects.get(pk=pk)
        except Donation.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        donation = self.get_object(pk)
        serializer = DonationSerializer(donation)
        return Response(serializer.data)

    def put(self, request, pk):
        cleaned_data = request.data
        donation = self.get_object(pk)
        dog_id = cleaned_data.get("dog_id",None)
        amount = cleaned_data.get("amount",donation.amount)
        donation_date = cleaned_data.get("donation_date",donation.date)
        if dog_id is not None:
            dog = Dog.objects.get(dog_id=dog_id)
        else:
            dog = None

        donation.dog=dog
        donation.amount=amount
        donation.donation_date=donation_date
        donation.save()
        serializer = DonationSerializer(donation)

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
    authentication_classes = [authentication.TokenAuthentication,authentication.BasicAuthentication,authentication.SessionAuthentication]
    
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
        pass

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
