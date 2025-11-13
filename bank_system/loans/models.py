from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class LoanProduct(models.Model):
    """Types of loans available"""
    LOAN_TYPES = (
        ('personal', 'Personal Loan'),
        ('auto', 'Auto Loan'),
        ('home', 'Home Loan'),
        ('education', 'Education Loan'),
        ('business', 'Business Loan'),
    )

    name = models.CharField(max_length=100)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual interest rate in %")
    min_term = models.IntegerField(help_text="Minimum loan term in months")
    max_term = models.IntegerField(help_text="Maximum loan term in months")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name']


class Loan(models.Model):
    """Loan instances for users"""
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('defaulted', 'Defaulted'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    product = models.ForeignKey(LoanProduct, on_delete=models.PROTECT, related_name='loans')
    account = models.ForeignKey('accounts.Account', on_delete=models.SET_NULL, null=True, related_name='loans')
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_term = models.IntegerField(help_text="Loan term in months")
    monthly_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    application_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    disbursement_date = models.DateTimeField(null=True, blank=True)
    maturity_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan #{self.id} - {self.user.username}"

    class Meta:
        ordering = ['-application_date']

    def calculate_monthly_payment(self):
        """Calculate EMI (Equated Monthly Installment)"""
        if self.principal_amount and self.loan_term and self.interest_rate:
            monthly_rate = self.interest_rate / 12 / 100
            n = self.loan_term
            if monthly_rate == 0:
                return self.principal_amount / n
            else:
                return self.principal_amount * (monthly_rate * (1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)
        return 0


class LoanPayment(models.Model):
    """Track loan payments"""
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(null=True, blank=True)
    transaction = models.OneToOneField('transactions.Transaction', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Payment for Loan #{self.loan.id}"

    class Meta:
        ordering = ['payment_date']
