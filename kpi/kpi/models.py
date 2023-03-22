from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class DogBreed(models.Model):
    breed = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 


class Dog(models.Model):
    dog_breed = models.ForeignKey(DogBreed,on_del=models.SET_NULL)
    dog_name = models.CharField(max_length=25)
    dog_weight = models.DecimalField(max_digits=7,decimal_places=2,null=True) # let's assume in lbs 
    dog_shelter_date_enter = models.DateTimeField(timezone.now)
    dog_adoption_date = models.DateTimeField(null=True)
    dog_bio = models.TextField()
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 


class DogPhoto(models.Model):
    dog = models.ForeignKey(Dog,on_delete=models.SET_NULL)
    photo = models.CharField(Max_length=200)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 


class PhotoClick(models.Model):
    dog_photo = models.ForeignKey(DogPhoto)
    click_date = models.DateTimeField(timezone.now)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 

  
class InfoRequest(models.Model):
    dog = models.ForeignKey(Dog)
    dog_photo = models.ForeignKey(DogPhoto)
    request_time = models.DateTimeField(timezone.now)
    dog_adopted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 

class Department(models.Model):
    department = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 

class User(AbstractUser):
    department = models.ForeignKey(Department,on_delete=models.SET_NULL)