from rest_framework import serializers
from .models import CarService, SubscriptionOption, HotelService, HotelServiceFeatures, CarImage, HotelImage, ServiceOption

class SubscriptionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionOption
        fields = ['id', 'duration_hours', 'price', 'car_service', "type"]

class CarServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarService
        fields = ['id', 'model', 'make', 'description', 'number_of_seats', 'year', 'color', 'type', 'cool', 'image']

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'car_service']

class CarServiceDetailSerializer(serializers.ModelSerializer):
    subscription_options = serializers.SerializerMethodField()
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = CarService
        fields = ['id', 'model', 'make', 'description', 'number_of_seats', 'year', 'color', 'type', 'cool', 'image', 'subscription_options', 'images']

    def get_subscription_options(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_staff:
            active_options = obj.subscription_options.all()
        else:
            active_options = obj.subscription_options.filter(active=True)
        return SubscriptionOptionSerializer(active_options, many=True).data


class HotelServiceListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HotelService
        fields = ['id', 'name', 'description', 'view', 'number_of_rooms', 'number_of_beds', 'day_price', 'image']

    def get_image(self, obj):
        image = obj.images.first()
        if image:
            return image.image.url
        return None


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


class ServiceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOption
        fields = '__all__'
