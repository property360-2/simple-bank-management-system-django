from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPreferences(models.Model):
    """User preferences for personalization"""
    THEME_CHOICES = (
        ('dark', 'Dark Mode'),
        ('light', 'Light Mode'),
    )
    FONT_SIZE_CHOICES = (
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    currency = models.CharField(max_length=3, default='USD')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='dark')
    font_size = models.CharField(max_length=10, choices=FONT_SIZE_CHOICES, default='medium')
    show_balance = models.BooleanField(default=True, help_text="Show account balance on dashboard")
    dashboard_cards = models.JSONField(default=dict, blank=True, help_text="JSON field for dashboard widget preferences")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Preferences"
        verbose_name_plural = "User Preferences"

    def __str__(self):
        return f"{self.user.username}'s preferences"


class SecurityLog(models.Model):
    """Log of security-related activities"""
    ACTIVITY_CHOICES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_change', 'Password Change'),
        ('profile_update', 'Profile Update'),
        ('failed_login', 'Failed Login'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='security_logs')
    activity = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='success', choices=(('success', 'Success'), ('failed', 'Failed')))
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.activity} ({self.timestamp})"
