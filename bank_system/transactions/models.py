from django.db import models
from accounts.models import Account

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]

    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='outgoing_transactions', null=True, blank=True)
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='incoming_transactions', null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - ${self.amount} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-created_at']


class FraudDetection(models.Model):
    """Model to track and flag suspicious transactions for fraud detection"""
    RISK_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='fraud_detection', null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='fraud_detections')
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Flags
    unusual_amount = models.BooleanField(default=False, help_text="Amount is significantly higher than usual")
    rapid_transactions = models.BooleanField(default=False, help_text="Multiple transactions in short time")
    unusual_time = models.BooleanField(default=False, help_text="Transaction at unusual hours")
    new_recipient = models.BooleanField(default=False, help_text="First transaction to this recipient")
    geographic_anomaly = models.BooleanField(default=False, help_text="Transaction from unusual location")

    reason = models.TextField(blank=True, help_text="Detailed reason for flagging")
    notes = models.TextField(blank=True, help_text="Admin notes")

    detected_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='fraud_reviews')

    def __str__(self):
        return f"Fraud Alert - {self.account.user.username} - {self.get_risk_level_display()}"

    class Meta:
        ordering = ['-detected_at']
        verbose_name_plural = "Fraud Detections"