from django.contrib import admin
from .models import LoanProduct, Loan, LoanPayment

@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'loan_type', 'min_amount', 'max_amount', 'interest_rate', 'is_active')
    list_filter = ('loan_type', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'loan_type', 'description')
        }),
        ('Amount Range', {
            'fields': ('min_amount', 'max_amount')
        }),
        ('Terms', {
            'fields': ('interest_rate', 'min_term', 'max_term')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'principal_amount', 'status', 'created_at')
    list_filter = ('status', 'product', 'created_at')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('created_at', 'updated_at', 'application_date')

    fieldsets = (
        ('User & Account', {
            'fields': ('user', 'account')
        }),
        ('Loan Product', {
            'fields': ('product',)
        }),
        ('Loan Details', {
            'fields': ('principal_amount', 'interest_rate', 'loan_term', 'monthly_payment', 'remaining_balance', 'total_paid')
        }),
        ('Status', {
            'fields': ('status', 'application_date', 'approval_date', 'disbursement_date', 'maturity_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LoanPayment)
class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan', 'amount', 'is_paid', 'payment_date')
    list_filter = ('is_paid', 'payment_date')
    search_fields = ('loan__id', 'loan__user__username')
    readonly_fields = ('payment_date',)
