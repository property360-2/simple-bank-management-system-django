from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

User = get_user_model()


class SavingsProduct(models.Model):
    """Types of savings accounts with different interest rates"""
    COMPOUNDING_CHOICES = (
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual interest rate in %")
    min_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    compounding_frequency = models.CharField(max_length=20, choices=COMPOUNDING_CHOICES, default='monthly')
    withdrawal_limit = models.IntegerField(default=6, help_text="Number of withdrawals allowed per month")
    penalty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Penalty for early withdrawal in %")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.interest_rate}% APY"

    class Meta:
        ordering = ['-interest_rate']


class SavingsAccount(models.Model):
    """Savings account instance for users"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_accounts')
    product = models.ForeignKey(SavingsProduct, on_delete=models.PROTECT, related_name='accounts')
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='savings_account')
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interest_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    withdrawals_this_month = models.IntegerField(default=0)
    last_interest_date = models.DateField(null=True, blank=True)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"

    class Meta:
        ordering = ['-opened_at']

    def calculate_interest(self):
        """Calculate interest based on compounding frequency"""
        if self.status != 'active' or self.balance <= 0:
            return Decimal('0.00')

        rate = self.product.interest_rate / 100
        balance = self.balance

        # Simple interest calculation for now
        daily_rate = rate / 365
        interest = balance * daily_rate

        return interest.quantize(Decimal('0.01'))

    def apply_interest(self):
        """Apply calculated interest to the account"""
        interest = self.calculate_interest()
        if interest > 0:
            self.balance += interest
            self.interest_earned += interest
            self.last_interest_date = timezone.now().date()
            self.save()

            # Create interest transaction
            InterestTransaction.objects.create(
                savings_account=self,
                amount=interest,
                interest_rate=self.product.interest_rate
            )

        return interest


class SavingsGoal(models.Model):
    """Savings goals for users"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_goals')
    savings_account = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE, related_name='goals')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']

    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.target_amount <= 0:
            return 0
        return min(100, (self.current_amount / self.target_amount * 100))

    @property
    def is_achieved(self):
        """Check if goal is achieved"""
        return self.current_amount >= self.target_amount


class InterestTransaction(models.Model):
    """Track interest accrual transactions"""
    savings_account = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE, related_name='interest_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interest ${self.amount} - {self.savings_account.account_number}"

    class Meta:
        ordering = ['-transaction_date']
