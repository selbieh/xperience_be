from django.contrib import admin

# Register your models here.
from .models import CarMake, CarModel, CarService, HotelServiceFeature, HotelService

admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(CarService)
admin.site.register(HotelServiceFeature)
admin.site.register(HotelService)
