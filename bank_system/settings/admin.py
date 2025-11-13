from django.contrib import admin
from .models import UserPreferences, OTPVerification, SecurityLog

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'font_size', 'language', 'updated_at')
    list_filter = ('theme', 'font_size', 'language')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Preferences', {
            'fields': ('theme', 'font_size', 'language', 'currency')
        }),
        ('Notifications', {
            'fields': ('notifications_email', 'notifications_sms')
        }),
        ('Display', {
            'fields': ('show_balance', 'dashboard_cards')
        }),
        ('Security', {
            'fields': ('two_factor_enabled',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_verified', 'otp_attempts', 'is_demo')
    list_filter = ('otp_verified', 'is_demo')
    search_fields = ('user__username', 'phone_number')
    readonly_fields = ('otp_created_at',)

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('OTP Details', {
            'fields': ('otp_code', 'otp_verified', 'otp_attempts', 'otp_created_at')
        }),
        ('Contact', {
            'fields': ('phone_number',)
        }),
        ('Demo', {
            'fields': ('is_demo',)
        }),
    )


@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'status', 'timestamp')
    list_filter = ('activity', 'status', 'timestamp')
    search_fields = ('user__username', 'activity')
    readonly_fields = ('timestamp',)

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Activity', {
            'fields': ('activity', 'status', 'details')
        }),
        ('System', {
            'fields': ('ip_address', 'user_agent', 'timestamp')
        }),
    )
