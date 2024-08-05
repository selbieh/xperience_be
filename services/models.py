from django.db import models
from base.models import AbstractBaseModel


from django.db import models
from base.models import AbstractBaseModel

class CarMake(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CarModel(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True, default="model")
    make = models.ForeignKey(CarMake, related_name='car_model', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class CarService(AbstractBaseModel):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_services', null=True)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_services', null=True) 
    description = models.TextField()
    number_of_seats = models.IntegerField()
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    cool = models.BooleanField(default=False)
    image = models.ImageField(upload_to='car_image/', blank=True, null=True)


class SubscriptionOption(AbstractBaseModel):
    type = models.CharField(max_length=50, choices=[('RIDE', 'Ride'), ('TRAVEL', 'Travel'), ('AIRPORT', 'Airport')])
    car_service = models.ForeignKey(CarService, on_delete=models.CASCADE, related_name='subscription_options')
    duration_hours = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.IntegerField(null=True, blank=True, default=0)
    points_price = models.IntegerField(null=True, blank=True, default=None)
    dollar_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class CarImage(models.Model):
    image = models.FileField(upload_to='car_images/')
    car_service = models.ForeignKey(CarService, on_delete=models.CASCADE, related_name='images')


class HotelServiceFeature(AbstractBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='feat_icon/', blank=True, null=True)

class HotelService(AbstractBaseModel):
    name = models.CharField(max_length=254)
    description = models.TextField()
    view = models.CharField(max_length=254)
    number_of_rooms = models.IntegerField()
    number_of_beds = models.IntegerField()
    day_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255, default="Cairo", null=True, blank=True )
    location_lat = models.FloatField(null=True, blank=True)
    location_long = models.FloatField(null=True, blank=True)
    location_url = models.URLField(max_length=500, null=True, blank=True)
    features = models.ManyToManyField(HotelServiceFeature)
    availability_start = models.DateField(null=True, blank=True)
    availability_end = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='hotel_image/', blank=True, null=True)
    points = models.IntegerField(null=True, blank=True, default=0)
    points_price = models.IntegerField(null=True, blank=True, default=None)
    dollar_day_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class HotelImage(models.Model):
    image = models.FileField(upload_to='hotel_images/')
    hotel_service = models.ForeignKey(HotelService, on_delete=models.CASCADE, related_name='images')


class ServiceOption(AbstractBaseModel):
    SERVICE_TYPE_CHOICES = [('Car', 'Car'), ('HOTEL', 'Hotel')]
    TYPE_CHOICES = [('Extras', 'Extras'), ("Scent Service", "Scent Service"), ("Beverages", "Beverages"), ("Snacks", "Snacks")]
    
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100)
    max_free = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    points_price = models.IntegerField(null=True, blank=True, default=None)
    dollar_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

