from django import forms
from .models import Transaction
from accounts.models import Account

class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TransferForm(forms.ModelForm):
    to_account_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter account number'})
    )
    
    class Meta:
        model = Transaction
        fields = ['amount', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_to_account_number(self):
        account_number = self.cleaned_data['to_account_number']
        try:
            account = Account.objects.get(account_number=account_number, is_active=True)
            return account
        except Account.DoesNotExist:
            raise forms.ValidationError("Invalid or inactive account number.")