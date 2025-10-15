from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'amount', 'from_account', 'to_account', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['from_account__account_number', 'to_account__account_number']