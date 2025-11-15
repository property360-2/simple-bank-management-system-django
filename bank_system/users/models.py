from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('manager', 'Manager/Staff'),
        ('admin', 'Administrator'),
    ]

    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer', help_text="User's role in the system")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_customer(self):
        return self.role == 'customer'

    def is_manager(self):
        return self.role == 'manager'

    def is_admin_user(self):
        return self.role == 'admin'