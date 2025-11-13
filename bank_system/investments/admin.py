from django.contrib import admin
from .models import InvestmentPlatform, InvestmentProduct, Portfolio, InvestmentHolding, InvestmentTransaction


@admin.register(InvestmentPlatform)
class InvestmentPlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform_type', 'is_active', 'created_at']
    list_filter = ['platform_type', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    fieldsets = (
        ('Platform Information', {
            'fields': ('name', 'platform_type', 'description')
        }),
        ('Display Settings', {
            'fields': ('icon', 'color')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(InvestmentProduct)
class InvestmentProductAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'name', 'platform', 'current_price', 'expected_return', 'risk_level', 'is_active']
    list_filter = ['platform', 'risk_level', 'is_active']
    search_fields = ['symbol', 'name', 'description']
    list_editable = ['current_price', 'is_active']
    fieldsets = (
        ('Product Information', {
            'fields': ('platform', 'symbol', 'name', 'description')
        }),
        ('Investment Details', {
            'fields': ('current_price', 'min_investment', 'expected_return', 'risk_level')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'total_invested', 'current_value', 'return_percentage', 'profit_loss', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'user__username', 'description']
    readonly_fields = ['total_invested', 'current_value', 'total_return', 'return_percentage', 'profit_loss', 'created_at', 'updated_at']
    fieldsets = (
        ('Portfolio Information', {
            'fields': ('user', 'account', 'name', 'description', 'status')
        }),
        ('Financial Summary', {
            'fields': ('total_invested', 'current_value', 'total_return', 'return_percentage', 'profit_loss')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    actions = ['update_portfolio_values']

    def update_portfolio_values(self, request, queryset):
        """Admin action to recalculate portfolio values"""
        count = 0
        for portfolio in queryset:
            portfolio.update_portfolio_value()
            count += 1
        self.message_user(request, f'Portfolio values updated for {count} portfolio(s).')

    update_portfolio_values.short_description = "Update portfolio values"


@admin.register(InvestmentHolding)
class InvestmentHoldingAdmin(admin.ModelAdmin):
    list_display = ['product', 'portfolio', 'quantity', 'purchase_price', 'current_price', 'current_value', 'profit_loss', 'return_percentage', 'status']
    list_filter = ['status', 'purchase_date', 'product__platform']
    search_fields = ['product__symbol', 'product__name', 'portfolio__name', 'portfolio__user__username']
    readonly_fields = ['purchase_value', 'current_value', 'profit_loss', 'return_percentage', 'purchase_date']
    list_editable = ['current_price']
    fieldsets = (
        ('Holding Information', {
            'fields': ('portfolio', 'product', 'quantity', 'status')
        }),
        ('Purchase Details', {
            'fields': ('purchase_price', 'purchase_value', 'purchase_date')
        }),
        ('Current Valuation', {
            'fields': ('current_price', 'current_value')
        }),
        ('Performance', {
            'fields': ('profit_loss', 'return_percentage')
        }),
    )


@admin.register(InvestmentTransaction)
class InvestmentTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'product', 'portfolio', 'quantity', 'price', 'total_amount', 'transaction_date']
    list_filter = ['transaction_type', 'transaction_date', 'product__platform']
    search_fields = ['product__symbol', 'portfolio__name', 'portfolio__user__username', 'notes']
    readonly_fields = ['transaction_date']
    date_hierarchy = 'transaction_date'
    fieldsets = (
        ('Transaction Information', {
            'fields': ('portfolio', 'product', 'holding', 'transaction_type')
        }),
        ('Transaction Details', {
            'fields': ('quantity', 'price', 'total_amount', 'transaction_date')
        }),
        ('Additional Information', {
            'fields': ('account_transaction', 'notes')
        }),
    )
