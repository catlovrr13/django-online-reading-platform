from django.contrib import admin
from .models import SubscriptionType, UserProfile

# Register your models here.
admin.site.register(SubscriptionType)
admin.site.register(UserProfile)