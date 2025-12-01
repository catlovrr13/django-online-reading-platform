from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = ['id','name', 'duration_days', 'price', 'benefits', 'is_active']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email")

    def create(self, validated_data):
        user = User.objects.create_user(
                    username=validated_data["username"],
                    password=validated_data["password"],
                    email=validated_data["email"],
                )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    card_number = serializers.CharField(write_only=True, min_length=10, max_length=10)
    subscription_type = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'card_number', 'subscription_type', 'img']

    def validate_card_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Card number must contain only digits.")
        return value