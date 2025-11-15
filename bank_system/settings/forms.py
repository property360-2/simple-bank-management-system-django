from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserPreferences
from core.currency import CURRENCY_CHOICES

User = get_user_model()


class UserPreferencesForm(forms.ModelForm):
    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-select',
            'aria-label': 'Select Currency'
        }),
        label='Preferred Currency',
        help_text='Select your preferred currency for displaying account values'
    )

    theme = forms.ChoiceField(
        choices=UserPreferences.THEME_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        }),
        label='Theme',
        help_text='Choose your preferred theme'
    )

    font_size = forms.ChoiceField(
        choices=UserPreferences.FONT_SIZE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-select',
            'aria-label': 'Select Font Size'
        }),
        label='Font Size',
        help_text='Choose your preferred font size'
    )

    class Meta:
        model = UserPreferences
        fields = ['currency', 'theme', 'font_size', 'show_balance']
        widgets = {
            'show_balance': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'show_balance': 'Show balance on dashboard',
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


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
