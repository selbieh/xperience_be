from django.db import models
from base.models import AbstractBaseModel

class CarService(AbstractBaseModel):
    model = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    description = models.TextField()
    number_of_seats = models.IntegerField()
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    cool = models.BooleanField(default=False)
    image = models.ImageField(upload_to='car_image/', blank=True, null=True)


class DurationOption(AbstractBaseModel):
    car_service = models.ForeignKey(CarService, on_delete=models.CASCADE, related_name='duration_options')
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class CarImage(models.Model):
    image = models.ImageField(upload_to='car_images/')
    car_service = models.ForeignKey(CarService, on_delete=models.CASCADE, related_name='images')


class HotelService(AbstractBaseModel):
    name = models.CharField(max_length=254)
    description = models.TextField()
    view = models.CharField(max_length=254)
    number_of_rooms = models.IntegerField()
    number_of_beds = models.IntegerField()


class HotelServiceFeatures(AbstractBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    hotel_service = models.ForeignKey(HotelService, on_delete=models.CASCADE, related_name='features')


class HotelImage(models.Model):
    image = models.ImageField(upload_to='hotel_images/')
    hotel_service = models.ForeignKey(HotelService, on_delete=models.CASCADE, related_name='images')


class ServiceOption(AbstractBaseModel):
    SERVICE_TYPE_CHOICES = [('Car', 'Car'), ('HOTEL', 'Hotel')]
    
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    type = models.CharField(max_length=100)  # Additional type categorization
    sub_type = models.CharField(max_length=100)  # Additional sub-type categorization
    name = models.CharField(max_length=100)
    max_free = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

