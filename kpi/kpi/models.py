from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class DogBreed(models.Model):
    breed = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 


class Dog(models.Model):
    dog_id = models.CharField(max_length=50)
    dog_breed = models.ForeignKey(DogBreed,on_del=models.PROTECT)
    dog_name = models.CharField(max_length=25)
    dog_weight_lbs = models.DecimalField(max_digits=7,decimal_places=2,null=True) 
    dog_shelter_date_enter = models.DateTimeField(timezone.now)
    dog_adoption_date = models.DateTimeField(null=True)
    dog_bio = models.TextField()
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 


class DogPhoto(models.Model):
    dog_photo_id = models.CharField(max_length=200)
    dog = models.ForeignKey(Dog,on_delete=models.PROTECT)
    photo = models.CharField(Max_length=200)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 


class PhotoClick(models.Model):
    dog_photo = models.ForeignKey(DogPhoto,on_delete=models.PROTECT)
    click_date = models.DateTimeField(timezone.now)
    user_info = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 

  
class InfoRequest(models.Model):
    dog = models.ForeignKey(Dog)
    request_time = models.DateTimeField(timezone.now)
    dog_adopted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 

class BillType(models.Model):
    bill_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 

class Bill(models.Model):
    dog = models.ForeignKey(Dog,on_delete=models.PROTECT,null=True)
    bill_amount = models.DecimalField(max_digits=8,decimal_places=2)
    bill_type = models.ForeignKey(BillType,models.Model,on_delete=models.PROTECT)
    bill_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 

class Donation(models.Model):
    dog = models.ForeignKey(Dog,on_delete=models.PROTECT,null=True)
    amount = models.DecimalField(max_length=13,decimal=2)
    donation_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 

class Department(models.Model):
    department = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateField(auto_now=True) 

class User(AbstractUser):
    department = models.ForeignKey(Department,on_delete=models.PROTECT,null=True)