from django.contrib import admin
from .models import CarMake, CarModel, CarService, HotelServiceFeature, HotelService, SubscriptionOption, CarImage, HotelImage, ServiceOption

admin.site.register(CarMake)
admin.site.register(CarModel)
admin.site.register(CarService)
admin.site.register(SubscriptionOption)
admin.site.register(CarImage)
admin.site.register(HotelServiceFeature)
admin.site.register(HotelService)
admin.site.register(HotelImage)
admin.site.register(ServiceOption)