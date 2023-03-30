import pytest 
from faker import Faker 
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory 
from rest_frame.test import force_authenticate 

from kpi.models import User, DogBreed

factory  = APIRequestFactory()
client = APIClient()
faker = Faker()

pytestmark = pytest.mark.django_db 

@pytest.fixture()
def createAdminUser():
    fullname = faker.name()
    first_name = fullname.split(" ")[0]
    last_name = fullname.split(" ")[1]
    email = f"{first_name}.{last_name}@{faker.domain_name()}"
    password = faker.pystr()
    user = User.objects.create(email=email,is_superuser=True)
    user.set_password(password)
    user.save()
    return user 

@pytest.mark.django_db 
def test_create_dog_breed(create_admin_user):
    dog_breed = faker.pystr() 
    payload = {
        "dog_breed":dog_breed
    }
    client.force_authenticate(user=create_admin_user)
    response = client.post("/api/v1/dog_breeds",payload=payload)
    data = response.data 
    assert dog_breed == data["dog_breed"]


@pytest.mark.django_db 
def test_get_dog_breed(create_admin_user):
    # i'm testing the get function
    dog_breed = DogBreed.objects.create(dog_breed = faker.pystr())

    client.force_authenticate(user=create_admin_user)
    response = client.get("/api/v1/dog_breeds")
    data = response.data 
    assert dog_breed == data["dog_breed"]

