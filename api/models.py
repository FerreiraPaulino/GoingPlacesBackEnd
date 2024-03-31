from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
# Create your models here.
class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profilepic = models.ImageField(null=True, blank=True, upload_to='images/')
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(null=True, blank=True, default=False)
    is_verified1 = models.BooleanField(null=True, blank=True, default=False)
    phone_number = models.IntegerField(null=True, blank=True, default=0)
    drivers_license = models.BooleanField(default=False, null=True, blank=True)
    license_images = ArrayField(models.CharField(max_length=300, null=True, blank=True), null=True, blank=True)
    ratings = ArrayField(models.IntegerField(), null=True, blank=True)
    star = models.BooleanField(default=False, null=True, blank=True)



    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return ({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

class Car(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    info = JSONField(null=True, blank=True)
    images = ArrayField(models.CharField(max_length=300, null=True, blank=True), null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
class CarImage(models.Model):
    file = models.ImageField(upload_to='images/', null=True, blank=True)

class Images(models.Model):
    file = models.ImageField(upload_to='images/', null=True, blank=True)


class ChatRoom(models.Model):
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(CustomUser)

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class MyTrips(models.Model):
    data = JSONField(null=True, blank=True)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='car_client')
    car_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='car_owner')
    images = ArrayField(models.CharField(max_length=300, null=True, blank=True), blank=True, null=True)

class Transaction(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    data = JSONField(null=True, blank=True)

