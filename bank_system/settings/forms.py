from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserPreferences

User = get_user_model()

# Currency choices with major and crypto currencies
CURRENCY_CHOICES = [
    ('USD', '💵 USD - US Dollar'),
    ('PHP', '₱ PHP - Philippine Peso'),
    ('EUR', '€ EUR - Euro'),
    ('GBP', '£ GBP - British Pound'),
    ('JPY', '¥ JPY - Japanese Yen'),
    ('AUD', 'A$ AUD - Australian Dollar'),
    ('CAD', 'C$ CAD - Canadian Dollar'),
    ('SGD', 'S$ SGD - Singapore Dollar'),
    ('HKD', 'HK$ HKD - Hong Kong Dollar'),
    ('INR', '₹ INR - Indian Rupee'),
    ('MYR', 'RM MYR - Malaysian Ringgit'),
    ('THB', '฿ THB - Thai Baht'),
    ('VND', '₫ VND - Vietnamese Dong'),
    ('IDR', 'Rp IDR - Indonesian Rupiah'),
    ('BTC', '₿ BTC - Bitcoin'),
    ('ETH', 'Ξ ETH - Ethereum'),
    ('USDT', '₮ USDT - Tether (USD Equivalent)'),
]


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

    class Meta:
        model = UserPreferences
        fields = ['currency', 'show_balance']
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
