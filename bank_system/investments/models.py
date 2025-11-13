from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

User = get_user_model()


class InvestmentPlatform(models.Model):
    """Investment platforms or brokerages"""
    PLATFORM_TYPES = (
        ('stocks', 'Stocks'),
        ('bonds', 'Bonds'),
        ('mutual_funds', 'Mutual Funds'),
        ('etf', 'ETF'),
        ('crypto', 'Cryptocurrency'),
        ('real_estate', 'Real Estate'),
        ('commodities', 'Commodities'),
    )

    name = models.CharField(max_length=100)
    platform_type = models.CharField(max_length=20, choices=PLATFORM_TYPES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, default='#0066CC', help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_platform_type_display()})"

    class Meta:
        ordering = ['name']


class InvestmentProduct(models.Model):
    """Investment products available on platforms"""
    RISK_LEVELS = (
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('very_high', 'Very High Risk'),
    )

    platform = models.ForeignKey(InvestmentPlatform, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=20, unique=True, help_text="Ticker symbol or product code")
    description = models.TextField(blank=True)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    min_investment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expected_return = models.DecimalField(max_digits=5, decimal_places=2, help_text="Expected annual return in %")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

    class Meta:
        ordering = ['symbol']


class Portfolio(models.Model):
    """User's investment portfolio"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    total_invested = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_return = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']

    @property
    def return_percentage(self):
        """Calculate return percentage"""
        if self.total_invested <= 0:
            return Decimal('0.00')
        return ((self.current_value - self.total_invested) / self.total_invested * 100).quantize(Decimal('0.01'))

    @property
    def profit_loss(self):
        """Calculate profit or loss"""
        return self.current_value - self.total_invested

    def update_portfolio_value(self):
        """Recalculate portfolio value based on holdings"""
        holdings = self.holdings.filter(status='active')
        total_value = sum(holding.current_value for holding in holdings)
        self.current_value = total_value
        self.total_return = self.profit_loss
        self.save()


class InvestmentHolding(models.Model):
    """Individual investment holdings in a portfolio"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('partial_sold', 'Partially Sold'),
    )

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='holdings')
    product = models.ForeignKey(InvestmentProduct, on_delete=models.PROTECT, related_name='holdings')
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.product.symbol} x {self.quantity} - {self.portfolio.name}"

    class Meta:
        ordering = ['-purchase_date']

    @property
    def purchase_value(self):
        """Total purchase value"""
        return self.quantity * self.purchase_price

    @property
    def current_value(self):
        """Current market value"""
        return self.quantity * self.current_price

    @property
    def profit_loss(self):
        """Calculate profit or loss"""
        return self.current_value - self.purchase_value

    @property
    def return_percentage(self):
        """Calculate return percentage"""
        if self.purchase_value <= 0:
            return Decimal('0.00')
        return ((self.current_value - self.purchase_value) / self.purchase_value * 100).quantize(Decimal('0.01'))


class InvestmentTransaction(models.Model):
    """Track investment buy/sell transactions"""
    TRANSACTION_TYPES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('dividend', 'Dividend'),
    )

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    product = models.ForeignKey(InvestmentProduct, on_delete=models.PROTECT, related_name='transactions')
    holding = models.ForeignKey(InvestmentHolding, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    account_transaction = models.OneToOneField('transactions.Transaction', on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.transaction_type.upper()} {self.quantity} x {self.product.symbol} @ ${self.price}"

    class Meta:
        ordering = ['-transaction_date']

    def save(self, *args, **kwargs):
        # Calculate total amount if not set
        if not self.total_amount:
            self.total_amount = self.quantity * self.price
        super().save(*args, **kwargs)
