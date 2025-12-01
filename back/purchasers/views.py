from django.shortcuts import render

# Create your views here.
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class SubscriptionTypeListView(generics.ListAPIView):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer

class SubscriptionTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer
    
class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserRegistrationSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User Created Successfully. Now perform Login to get your token.",
            },
            status=status.HTTP_201_CREATED,
        )
    
class SubscribeToPremiumView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile

    def update(self, request, *args, **kwargs):
        premium_subscription = SubscriptionType.objects.get(name=SubscriptionType.PREMIUM)
        user_profile = self.get_object()

        if user_profile.subscription_type == premium_subscription:
            return Response({"message": "You are already subscribed to Premium."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card_number = serializer.validated_data.get('card_number')
        
        user_profile.subscription_type = premium_subscription
        user_profile.save()

        return Response({"message": f"Successfully subscribed to Premium using card {card_number}!"}, status=status.HTTP_200_OK)

class UnsubscribeView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        free_subscription = SubscriptionType.objects.get(name=SubscriptionType.FREE)

        user_profile = self.get_object()

        if user_profile.subscription_type == free_subscription:
            return Response({"message": "You are already unsubscribed."}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.subscription_type = free_subscription
        user_profile.save()

        return Response({"message": "Successfully unsubscribed."}, status=status.HTTP_200_OK)