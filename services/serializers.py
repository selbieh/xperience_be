from rest_framework import serializers
from .models import CarService, DurationOption, HotelService, HotelServiceFeatures, CarImage, HotelImage

class DurationOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DurationOption
        fields = ['id', 'duration', 'price', 'car_service']

class CarServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarService
        fields = ['id', 'model', 'make', 'description', 'number_of_seats', 'year', 'color', 'type', 'cool']

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'car_service']

class CarServiceDetailSerializer(serializers.ModelSerializer):
    duration_options = serializers.SerializerMethodField()
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = CarService
        fields = ['id', 'model', 'make', 'description', 'number_of_seats', 'year', 'color', 'type', 'cool', 'image', 'duration_options', 'images']

    def get_duration_options(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_staff:
            active_options = obj.duration_options.all()
        else:
            active_options = obj.duration_options.filter(active=True)
        return DurationOptionSerializer(active_options, many=True).data

class HotelServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelService
        fields = ['id', 'name', 'description', 'view', 'number_of_rooms', 'number_of_beds', 'day_price']

class HotelServiceFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelServiceFeatures
        fields = ['id', 'name', 'description', 'hotel_service']

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['id', 'image', 'hotel_service']

class HotelServiceDetailSerializer(serializers.ModelSerializer):
    features = HotelServiceFeaturesSerializer(many=True, read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)

    class Meta:
        model = HotelService
        fields = ['id', 'name', 'description', 'view', 'number_of_rooms', 'number_of_beds', 'day_price', 'features', 'images']
