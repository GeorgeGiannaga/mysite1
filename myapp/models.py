
from django.db import models
from django.contrib.auth.models import User

class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.search)

    class Meta:
        verbose_name_plural = 'Searches'

class Property(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    Last_name = models.CharField(max_length=50)
    First_name =models.CharField(max_length=50)
    Country = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    Post_Code = models.CharField(max_length=10)
    Description = models.CharField(max_length=200)
    Image = models.ImageField(upload_to='images/', null=True, blank=True)
    Price = models.FloatField(max_length=20, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.Last_name, self.First_name, self.Country, self. City, self.Address, self.Description

    class Meta:
        db_table = "Properties"

class Details(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, primary_key=True, related_name='details')
    Floors = models.IntegerField(default=0)
    Garden = models.BooleanField(default=False)
    Furnised = models.BooleanField(default=False)
    View = models.CharField(max_length=30)
    Altitude = models.IntegerField(default=0)
    Near_places = models.CharField(max_length=50)
    Balconies = models.IntegerField(default=0)
    Windows = models.IntegerField(default=0)
    Light = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        db_table = "Details"