from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BillerCategory(models.Model):
    """Categories for bills"""
    CATEGORIES = (
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('internet', 'Internet & Telecom'),
        ('insurance', 'Insurance'),
        ('credit_card', 'Credit Card'),
        ('loan', 'Loan Payment'),
        ('shopping', 'Shopping'),
        ('utilities', 'Utilities'),
        ('subscription', 'Subscription'),
        ('other', 'Other'),
    )

    category = models.CharField(max_length=20, choices=CATEGORIES, unique=True)
    icon = models.CharField(max_length=50, default='fa-bill', help_text="Font Awesome icon class")
    color = models.CharField(max_length=20, default='#007bff')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_category_display()

    class Meta:
        verbose_name_plural = "Biller Categories"


class Biller(models.Model):
    """Bills and billing accounts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billers')
    name = models.CharField(max_length=100)
    category = models.ForeignKey(BillerCategory, on_delete=models.SET_NULL, null=True, related_name='billers')
    account_number = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    nickname = models.CharField(max_length=100, blank=True, help_text="Your nickname for this biller")
    due_date = models.IntegerField(default=15, help_text="Day of month when bill is due")
    reminder_days = models.IntegerField(default=3, help_text="Days before due date to send reminder")
    last_payment_date = models.DateTimeField(null=True, blank=True)
    last_amount_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.nickname or 'No nickname'})"

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'account_number')


class Bill(models.Model):
    """Individual bills to be paid"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    )

    biller = models.ForeignKey(Biller, on_delete=models.CASCADE, related_name='bills')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)
    transaction = models.OneToOneField('transactions.Transaction', on_delete=models.SET_NULL, null=True, blank=True, related_name='bill')
    paid_date = models.DateTimeField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_frequency = models.CharField(
        max_length=20,
        choices=(('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')),
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.biller.name} - {self.amount} ({self.status})"

    class Meta:
        ordering = ['due_date']

    @property
    def is_overdue(self):
        from datetime import date
        return self.status != 'paid' and self.due_date < date.today()


class BillReminder(models.Model):
    """Reminders for upcoming bills"""
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE, related_name='reminder')
    reminder_date = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.bill.biller.name}"
