from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


class UserProfileRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('__all__')

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']

class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rules
        fields = ['rules_name']

class PropertyListSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    city = CitySerializer()
    class Meta:
        model = Property
        fields = ['images','property_type','city']

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','username', 'avatar']

class PropertyDetailSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    city = CitySerializer()
    rules = RulesSerializer(many=True)
    owner = OwnerSerializer()
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'price', 'city',
            'property_type', 'rules', 'max_guests','owner',
            'images','avg_rating','count_people'
        ]
    def get_avg_rating(self, obj):
        return obj.get_avg_rating()
    def get_count_people(self,obj):
        return obj.get_count_people()


class BookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField(format="%Y-%m-%d")
    check_out = serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = Booking
        fields = '__all__'


class ReviewCreateSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d.%m.%Y')
    class Meta:
        model = Review
        fields = ['rating', 'comment', 'user', 'property','created_date']

class UserProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar','first_name' ]

class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileReviewSerializer()
    created_date = serializers.DateTimeField(format='%d.%m.%Y')
    class Meta:
        model = Review
        fields = ('id','property','user','rating','comment','created_date')

