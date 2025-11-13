from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
import random
import string

from .models import UserPreferences, OTPVerification, SecurityLog
from .forms import UserPreferencesForm, ProfileForm, OTPVerificationForm, CustomPasswordChangeForm

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
def preferences(request):
    """User preferences settings"""
    try:
        user_prefs = request.user.preferences
    except UserPreferences.DoesNotExist:
        user_prefs = UserPreferences.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=user_prefs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your preferences have been updated successfully!')
            return redirect('settings:preferences')
    else:
        form = UserPreferencesForm(instance=user_prefs)

    context = {
        'form': form,
        'page_title': 'Preferences',
        'active_tab': 'preferences'
    }
    return render(request, 'settings/preferences.html', context)


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
def profile_edit_otp(request):
    """Edit profile with OTP verification"""
    try:
        otp_obj = request.user.otp_verification
    except OTPVerification.DoesNotExist:
        otp_obj = OTPVerification.objects.create(user=request.user)

    if request.method == 'POST':
        if 'send_otp' in request.POST:
            # Generate and send OTP (demo - displayed on screen)
            otp_code = ''.join(random.choices(string.digits, k=6))
            otp_obj.otp_code = otp_code
            otp_obj.otp_verified = False
            otp_obj.otp_attempts = 0
            otp_obj.is_demo = True
            otp_obj.phone_number = request.user.phone or "Not set"
            otp_obj.save()

            # Log security activity
            SecurityLog.objects.create(
                user=request.user,
                activity='otp_verify',
                status='success',
                details=f"OTP sent for profile edit"
            )

            messages.success(request, f'OTP has been sent! (Demo: {otp_code})')
            return redirect('settings:profile_edit_otp')

        elif 'verify_otp' in request.POST:
            form = OTPVerificationForm(request.POST, instance=otp_obj)
            if form.is_valid():
                submitted_otp = form.cleaned_data['otp_code']
                if submitted_otp == otp_obj.otp_code:
                    otp_obj.otp_verified = True
                    otp_obj.save()
                    messages.success(request, 'OTP verified! You can now update your profile.')
                    return redirect('settings:profile_edit')
                else:
                    otp_obj.otp_attempts += 1
                    otp_obj.save()
                    if otp_obj.otp_attempts >= 3:
                        messages.error(request, 'Too many failed OTP attempts. Please try again later.')
                        return redirect('settings:profile_edit_otp')
                    messages.error(request, f'Invalid OTP. Attempts remaining: {3 - otp_obj.otp_attempts}')
        else:
            form = OTPVerificationForm(instance=otp_obj)
    else:
        form = OTPVerificationForm(instance=otp_obj)

    context = {
        'form': form,
        'otp_obj': otp_obj,
        'page_title': 'Profile Edit (OTP Verification)',
        'active_tab': 'profile_otp',
        'otp_sent': otp_obj.otp_code != ''
    }
    return render(request, 'settings/profile_edit_otp.html', context)


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

            return redirect('settings:preferences')
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
    try:
        user_prefs = request.user.preferences
    except UserPreferences.DoesNotExist:
        user_prefs = UserPreferences.objects.create(user=request.user)

    if request.method == 'POST':
        user_prefs.two_factor_enabled = request.POST.get('two_factor_enabled') == 'on'
        user_prefs.save()
        messages.success(request, 'Security settings updated!')
        return redirect('settings:security')

    security_logs = request.user.security_logs.all()[:20]

    context = {
        'user_prefs': user_prefs,
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


@login_required
def notifications(request):
    """Notification preferences"""
    try:
        user_prefs = request.user.preferences
    except UserPreferences.DoesNotExist:
        user_prefs = UserPreferences.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserPreferencesForm(request.POST, instance=user_prefs)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification preferences updated!')
            return redirect('settings:notifications')
    else:
        form = UserPreferencesForm(instance=user_prefs)

    context = {
        'form': form,
        'page_title': 'Notifications',
        'active_tab': 'notifications'
    }
    return render(request, 'settings/notifications.html', context)
