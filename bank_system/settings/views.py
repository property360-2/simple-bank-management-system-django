from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

from .models import UserPreferences, SecurityLog
from .forms import UserPreferencesForm, ProfileForm, CustomPasswordChangeForm

User = get_user_model()


@login_required
def settings_dashboard(request):
    """Main settings dashboard"""
    context = {
        'page_title': 'Settings',
        'active_tab': 'dashboard'
    }
    return render(request, 'settings/settings_dashboard.html', context)


@login_required
def profile_edit(request):
    """Edit user profile information"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('settings:profile_edit')
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'form': form,
        'page_title': 'Edit Profile',
        'active_tab': 'profile'
    }
    return render(request, 'settings/profile_edit.html', context)


@login_required
def change_password(request):
    """Change password"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password has been changed successfully!')

            # Log security activity
            SecurityLog.objects.create(
                user=request.user,
                activity='password_change',
                status='success'
            )

            return redirect('settings:dashboard')
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        'form': form,
        'page_title': 'Change Password',
        'active_tab': 'security'
    }
    return render(request, 'settings/change_password.html', context)


@login_required
def security_settings(request):
    """Security and privacy settings"""
    security_logs = request.user.security_logs.all()[:20]

    context = {
        'security_logs': security_logs,
        'page_title': 'Security & Privacy',
        'active_tab': 'security'
    }
    return render(request, 'settings/security_settings.html', context)


@login_required
def account_summary(request):
    """Account summary and linked accounts"""
    accounts = request.user.accounts.filter(is_active=True)

    context = {
        'accounts': accounts,
        'page_title': 'Account Summary',
        'active_tab': 'account_summary'
    }
    return render(request, 'settings/account_summary.html', context)
