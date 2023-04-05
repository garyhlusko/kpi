from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from kpi.api.views import UserAPIView, PING, DogBreedDetail,DogBreedList, DogPhotoList, DogPhotoDetail, PhotoClickDetail, PhotoClickList

urlpatterns = [
    path('ping/', PING.as_view(), name="ping"),
    path('user/',UserAPIView.as_view(),name="users"),
    path('dog/breeds',DogBreedList.as_view(),name="dog_breeds"),
    path('dog/breeds/<int:id>',DogBreedDetail.as_view(),name="dog_breed"),
    path('dog/photos',DogPhotoList.as_view(),name="dog_breeds"),
    path('dog/photos/<int:id>',DogPhotoDetail.as_view(),name="dog_breed"),
    path('photo/clicks',PhotoClickList.as_view(),name="dog_breeds"),
    path('photo/clicks/<int:id>',PhotoClickDetail.as_view(),name="dog_breed"),
]
