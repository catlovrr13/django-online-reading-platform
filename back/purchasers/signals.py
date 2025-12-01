from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, SubscriptionType

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        free_sub, _ = SubscriptionType.objects.get_or_create(
            name='free',
            defaults={
                'duration_days': 0,
                'price': 0.00,
                'benefits': 'Preview up to 2 chapters per premium book. Full access to free books.',
                'is_active': True
            }
        )
        UserProfile.objects.create(user=instance, subscription_type=free_sub)