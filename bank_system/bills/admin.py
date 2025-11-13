from django.contrib import admin
from .models import BillerCategory, Biller, Bill, BillReminder

@admin.register(BillerCategory)
class BillerCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'icon', 'color')
    search_fields = ('category',)


@admin.register(Biller)
class BillerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'nickname', 'is_active', 'is_favorite')
    list_filter = ('category', 'is_active', 'is_favorite')
    search_fields = ('name', 'nickname', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Basic Info', {
            'fields': ('name', 'category', 'nickname')
        }),
        ('Contact', {
            'fields': ('account_number', 'phone', 'email')
        }),
        ('Settings', {
            'fields': ('due_date', 'reminder_days', 'is_active', 'is_favorite')
        }),
        ('Last Payment', {
            'fields': ('last_payment_date', 'last_amount_paid')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'biller', 'amount', 'due_date', 'status', 'is_recurring')
    list_filter = ('status', 'is_recurring', 'due_date')
    search_fields = ('biller__name', 'biller__user__username')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Biller', {
            'fields': ('biller',)
        }),
        ('Bill Details', {
            'fields': ('amount', 'due_date', 'status', 'description')
        }),
        ('Payment', {
            'fields': ('transaction', 'paid_date')
        }),
        ('Recurring', {
            'fields': ('is_recurring', 'recurrence_frequency')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BillReminder)
class BillReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'bill', 'reminder_date', 'is_sent')
    list_filter = ('is_sent', 'reminder_date')
    search_fields = ('bill__biller__name',)
    readonly_fields = ('created_at',)
