from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserPreferences, OTPVerification

User = get_user_model()


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = ['theme', 'font_size', 'language', 'currency', 'notifications_email', 'notifications_sms', 'show_balance']
        widgets = {
            'theme': forms.RadioSelect(choices=UserPreferences.THEME_CHOICES),
            'font_size': forms.Select(),
            'language': forms.Select(),
            'notifications_email': forms.CheckboxInput(),
            'notifications_sms': forms.CheckboxInput(),
            'show_balance': forms.CheckboxInput(),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '3'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }


class OTPVerificationForm(forms.ModelForm):
    class Meta:
        model = OTPVerification
        fields = ['otp_code']
        widgets = {
            'otp_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000000',
                'maxlength': '6',
                'inputmode': 'numeric',
                'pattern': '[0-9]{6}',
                'autocomplete': 'off',
            })
        }

    def clean_otp_code(self):
        otp_code = self.cleaned_data.get('otp_code', '')
        if not otp_code.isdigit() or len(otp_code) != 6:
            raise forms.ValidationError("OTP must be 6 digits.")
        return otp_code


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
