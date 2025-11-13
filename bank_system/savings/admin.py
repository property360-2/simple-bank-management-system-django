from django.contrib import admin
from .models import SavingsProduct, SavingsAccount, SavingsGoal, InterestTransaction


@admin.register(SavingsProduct)
class SavingsProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'interest_rate', 'min_balance', 'compounding_frequency', 'withdrawal_limit', 'is_active']
    list_filter = ['is_active', 'compounding_frequency']
    search_fields = ['name', 'description']
    list_editable = ['interest_rate', 'is_active']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Interest Settings', {
            'fields': ('interest_rate', 'compounding_frequency', 'min_balance')
        }),
        ('Withdrawal Rules', {
            'fields': ('withdrawal_limit', 'penalty_rate')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(SavingsAccount)
class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'user', 'product', 'balance', 'interest_earned', 'status', 'withdrawals_this_month', 'opened_at']
    list_filter = ['status', 'product', 'opened_at']
    search_fields = ['account_number', 'user__username', 'user__email']
    readonly_fields = ['account_number', 'interest_earned', 'withdrawals_this_month', 'last_interest_date', 'opened_at']
    fieldsets = (
        ('Account Information', {
            'fields': ('user', 'product', 'account', 'account_number', 'status')
        }),
        ('Balance Information', {
            'fields': ('balance', 'interest_earned')
        }),
        ('Activity Tracking', {
            'fields': ('withdrawals_this_month', 'last_interest_date')
        }),
        ('Dates', {
            'fields': ('opened_at', 'closed_at')
        }),
    )

    actions = ['apply_interest_to_selected']

    def apply_interest_to_selected(self, request, queryset):
        """Admin action to apply interest to selected accounts"""
        count = 0
        for account in queryset:
            if account.status == 'active':
                account.apply_interest()
                count += 1
        self.message_user(request, f'Interest applied to {count} account(s).')

    apply_interest_to_selected.short_description = "Apply interest to selected active accounts"


@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'savings_account', 'target_amount', 'current_amount', 'progress_percentage', 'target_date', 'status']
    list_filter = ['status', 'target_date']
    search_fields = ['name', 'user__username', 'description']
    readonly_fields = ['created_at', 'completed_at', 'progress_percentage', 'is_achieved']
    fieldsets = (
        ('Goal Information', {
            'fields': ('user', 'savings_account', 'name', 'description')
        }),
        ('Target & Progress', {
            'fields': ('target_amount', 'current_amount', 'progress_percentage', 'is_achieved', 'target_date')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'completed_at')
        }),
    )


@admin.register(InterestTransaction)
class InterestTransactionAdmin(admin.ModelAdmin):
    list_display = ['savings_account', 'amount', 'interest_rate', 'transaction_date']
    list_filter = ['transaction_date']
    search_fields = ['savings_account__account_number', 'savings_account__user__username']
    readonly_fields = ['savings_account', 'amount', 'interest_rate', 'transaction_date']
    date_hierarchy = 'transaction_date'
