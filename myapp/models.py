
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.search)

    class Meta:
        verbose_name_plural = 'Searches'

class Property(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    Country = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    Post_Code = models.CharField(max_length=10)
    Description = models.CharField(max_length=200)
    Image = models.ImageField(upload_to='images/', null=True, blank=True)
    Price = models.FloatField(max_length=20, null=True, blank=True)
    Area = models.IntegerField(null=True, blank=True)
    Garages = models.IntegerField(null=True, blank=True)
    Baths = models.IntegerField(null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.Country, self. City, self.Address, self.Description

    class Meta:
        db_table = "Properties"

class Details(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, primary_key=True, related_name='details')
    Floors = models.IntegerField(default=0)
    Garden = models.BooleanField(default=False)
    Furnised = models.BooleanField(default=False)
    View = models.CharField(max_length=30)
    Altitude = models.IntegerField(default=0)
    Near_places = models.CharField(max_length=100)
    Balconies = models.IntegerField(default=0)
    Windows = models.IntegerField(default=0)
    Light = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        db_table = "Details"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='Profile')
    Phone_number = models.CharField(max_length=10, null=True, blank=True)
    objects = models.Manager()

    class Meta:
        db_table = "Profile"


class Message(models.Model):
     sender = models.ForeignKey(get_user_model(), related_name="sender", on_delete=models.CASCADE)
     receiver = models.ForeignKey(get_user_model(), related_name="receiver", on_delete=models.CASCADE)
     message = models.CharField(max_length=150)
     timestamp = models.DateTimeField(auto_now_add=True)
     unread = models.BooleanField(default = True)
     objects = models.Manager()

     class Meta:
         db_table = "Messages"