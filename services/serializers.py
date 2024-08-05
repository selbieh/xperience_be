from rest_framework import serializers
from .models import CarService, SubscriptionOption, HotelService, HotelServiceFeature, CarImage, HotelImage, ServiceOption, CarMake, CarModel


class CarServiceMinimalSerializer(serializers.ModelSerializer):
    make = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    
    def get_make(self, obj):
        return obj.make.name if obj.make else None
    
    def get_model(self, obj):
        return obj.model.name if obj.model else None
    
    class Meta:
        model = CarService
        fields = ['id', 'model', 'make', 'number_of_seats', 'year', 'type']


class SubscriptionOptionSerializer(serializers.ModelSerializer):
    car_service = CarServiceMinimalSerializer()
    class Meta:
        model = SubscriptionOption
        fields = ['id', 'duration_hours', 'price', 'car_service', "type", "points", "points_price", "dollar_price"]

class SubscriptionOptionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionOption
        fields = ['id', 'duration_hours', 'price', 'car_service', "type", "points", "points_price", "dollar_price"]


class CarServiceListSerializer(serializers.ModelSerializer):
    make_name = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField()
    class Meta:
        model = CarService
        fields = ['id', 'model', 'make', 'model_name', 'make_name', 'description', 'number_of_seats', 'year', 'color', 'type', 'cool', 'image']

    def get_make_name(self, obj):
        return obj.make.name if obj.make else None
    
    def get_model_name(self, obj):
        return obj.model.name if obj.model else None

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'car_service']

class CarServiceDetailSerializer(serializers.ModelSerializer):
    subscription_options = serializers.SerializerMethodField()
    images = CarImageSerializer(many=True, read_only=True)
    make_name = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField()
    
    def get_make_name(self, obj):
        return obj.make.name if obj.make else None
    
    def get_model_name(self, obj):
        return obj.model.name if obj.model else None

    class Meta:
        model = CarService
        fields = ['id', 'model', 'make', 'model_name', 'make_name', 'description', 'number_of_seats', 'year', 'color', 'type', 'cool', 'image', 'subscription_options', 'images']
        read_only_fields = ['model_name', 'make_name']

    def get_subscription_options(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_staff:
            active_options = obj.subscription_options.all()
        else:
            active_options = obj.subscription_options.filter(active=True)
        return SubscriptionOptionSerializer(active_options, many=True).data


class HotelServiceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelService
        fields = ['id', 'name', 'name_ar', 'name_en', 'description', 'view', 'number_of_rooms', 'number_of_beds', 'day_price', 'image', 'points', 'points_price', 'dollar_day_price']


class HotelServiceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelServiceFeature
        fields = ['id', 'name', 'description', 'image']

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['id', 'image', 'hotel_service']

class HotelServiceDetailSerializer(serializers.ModelSerializer):
    features = serializers.PrimaryKeyRelatedField(queryset=HotelServiceFeature.objects.all(), many=True)
    images = HotelImageSerializer(many=True, read_only=True)

    class Meta:
        model = HotelService
        fields = ['id', 'name', 'name_ar', 'name_en', 'description', 'view', 'number_of_rooms', 'number_of_beds', 'day_price', 'features', 'images', 'address', 'location_lat', 'location_long', 'location_url', 'points', 'points_price', 'dollar_day_price']
        read_only_fields = ['name']

    def update(self, instance, validated_data):
        features_data = validated_data.pop('features', None)
        instance = super().update(instance, validated_data)
        if features_data is not None:
            instance.features.set(features_data)
        return instance
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['features'] = HotelServiceFeatureSerializer(instance.features.all(), many=True).data
        return ret
    

class HotelServiceMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelService
        fields = ['id', 'name', 'address']


class ServiceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOption
        fields = '__all__'


class CarMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = '__all__'
        read_only_fields = ['name']

class CarModelSerializer(serializers.ModelSerializer):
    make = serializers.PrimaryKeyRelatedField(queryset=CarMake.objects.all())
    make_name = serializers.SerializerMethodField()

    def get_make_name(self, obj):
        return obj.make.name if obj.make else None
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'make', 'make_name', "active"]