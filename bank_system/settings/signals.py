from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserPreferences, OTPVerification

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    """Automatically create UserPreferences when a new user is created"""
    if created:
        UserPreferences.objects.get_or_create(user=instance)
        OTPVerification.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_preferences(sender, instance, **kwargs):
    """Ensure UserPreferences exists for the user"""
    UserPreferences.objects.get_or_create(user=instance)
    OTPVerification.objects.get_or_create(user=instance)
