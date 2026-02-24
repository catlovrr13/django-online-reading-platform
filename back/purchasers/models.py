from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SubscriptionType(models.Model):
    FREE = 'free'
    PREMIUM = 'premium'
    
    SUBSCRIPTION_CHOICES = [
        (FREE, 'Free Account'),
        (PREMIUM, 'Premium Account'),
    ]

    MONTH = '30'
    YEAR = '356'

    SUBSCRIPTION_OPTION = [
        (MONTH, 'One Month'),
        (YEAR, 'One Year')
    ]

    name = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES)
    duration_days = models.CharField(max_length=20, default='0', choices=SUBSCRIPTION_OPTION, help_text="Duration in days. Use 0 for free/lifetime plans.")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    benefits = models.TextField(blank=True, help_text="Displayed to users (e.g., 'Read 2 chapters', 'Unlimited access')")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.duration_days}"

    class Meta:
        verbose_name = "Subscription Type"
        verbose_name_plural = "Subscription Types"
    
class UserProfile(models.Model):
    img = models.ImageField(upload_to='profile/', default='profile/default.jpeg')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username