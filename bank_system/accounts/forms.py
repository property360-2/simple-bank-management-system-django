from django import forms
from .models import Account
import random

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type']
        widgets = {
            'account_type': forms.Select(attrs={'class': 'form-select'})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        account = super().save(commit=False)
        if self.user:
            account.user = self.user
        if not account.account_number:
            account.account_number = f"ACC{random.randint(1000000000, 9999999999)}"
        if commit:
            account.save()
        return account