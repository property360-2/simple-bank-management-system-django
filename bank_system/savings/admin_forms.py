from django import forms
from .models import SavingsProduct


class SavingsProductForm(forms.ModelForm):
    class Meta:
        model = SavingsProduct
        fields = ['name', 'description', 'interest_rate', 'compounding_frequency', 'min_balance', 'max_balance', 'withdrawal_limit', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-dark', 'rows': 4, 'placeholder': 'Description'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control form-control-dark', 'step': '0.01', 'placeholder': '0.00'}),
            'compounding_frequency': forms.Select(attrs={'class': 'form-control form-control-dark'}),
            'min_balance': forms.NumberInput(attrs={'class': 'form-control form-control-dark', 'step': '0.01', 'placeholder': '0.00'}),
            'max_balance': forms.NumberInput(attrs={'class': 'form-control form-control-dark', 'step': '0.01', 'placeholder': '0.00'}),
            'withdrawal_limit': forms.NumberInput(attrs={'class': 'form-control form-control-dark', 'step': '0.01', 'placeholder': '0.00'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
