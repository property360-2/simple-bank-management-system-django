from django import forms
from .models import InvestmentProduct, InvestmentPlatform


class InvestmentProductForm(forms.ModelForm):
    class Meta:
        model = InvestmentProduct
        fields = ['platform', 'name', 'symbol', 'description', 'risk_level', 'current_price', 'min_investment', 'expected_return', 'is_active']
        widgets = {
            'platform': forms.Select(attrs={'class': 'form-control form-control-dark'}),
            'name': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Product Name'}),
            'symbol': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Symbol (e.g., AAPL)'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-dark', 'rows': 4, 'placeholder': 'Description'}),
            'risk_level': forms.Select(attrs={'class': 'form-control form-control-dark'}),
            'current_price': forms.NumberInput(attrs={'class': 'form-control form-control-dark', 'step': '0.01', 'placeholder': '0.00'}),
            'min_investment': forms.NumberInput(attrs={'class': 'form-control form-control-dark', 'step': '0.01', 'placeholder': '0.00'}),
            'expected_return': forms.NumberInput(attrs={'class': 'form-control form-control-dark', 'step': '0.01', 'placeholder': '0.00'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class InvestmentPlatformForm(forms.ModelForm):
    class Meta:
        model = InvestmentPlatform
        fields = ['name', 'platform_type', 'description', 'icon', 'color', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Platform Name'}),
            'platform_type': forms.Select(attrs={'class': 'form-control form-control-dark'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-dark', 'rows': 3, 'placeholder': 'Platform description'}),
            'icon': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'placeholder': 'Font Awesome Icon (e.g., fa-chart-line)'}),
            'color': forms.TextInput(attrs={'class': 'form-control form-control-dark', 'type': 'color'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
