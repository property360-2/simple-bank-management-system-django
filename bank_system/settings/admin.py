from django.contrib import admin
from .models import UserPreferences, SecurityLog

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'updated_at')
    list_filter = ('show_balance',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Preferences', {
            'fields': ('currency', 'show_balance')
        }),
        ('Display', {
            'fields': ('dashboard_cards',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
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
