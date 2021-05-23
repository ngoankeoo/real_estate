from django.db import models
from datetime import datetime
from realtors.models import Realtor


# Create your models here.

class Listing(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    price = models.FloatField(default=-1)
    bedrooms = models.IntegerField(default=-1)
    bathrooms = models.DecimalField(default=-1, max_digits=2, decimal_places=1)
    garage = models.IntegerField(default=-1)
    sqft = models.FloatField(default=-1)
    lot_size = models.DecimalField(default=-1, max_digits=5, decimal_places=1)
    image_link = models.TextField(default="https://file4.batdongsan.com.vn/crop/200x140/2021/05/03/20210503173512-1c8c_wm.jpg")
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    is_published = models.BooleanField(default=True)
    list_data = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title
