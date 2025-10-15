from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account
from .forms import AccountForm

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

@login_required
def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    transactions = account.incoming_transactions.all()[:10] | account.outgoing_transactions.all()[:10]
    transactions = sorted(transactions, key=lambda x: x.created_at, reverse=True)[:10]
    return render(request, 'accounts/account_detail.html', {
        'account': account,
        'transactions': transactions
    })

@login_required
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, user=request.user)
        if form.is_valid():
            account = form.save()
            messages.success(request, f'Account {account.account_number} created successfully!')
            return redirect('account_list')
    else:
        form = AccountForm(user=request.user)
    return render(request, 'accounts/account_form.html', {'form': form, 'action': 'Create'})

@login_required
def account_update(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully!')
            return redirect('account_detail', pk=account.pk)
    else:
        form = AccountForm(instance=account, user=request.user)
    return render(request, 'accounts/account_form.html', {'form': form, 'action': 'Update', 'account': account})

@login_required
def account_delete(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        account_number = account.account_number
        account.delete()
        messages.success(request, f'Account {account_number} deleted successfully!')
        return redirect('account_list')
    return render(request, 'accounts/account_confirm_delete.html', {'account': account})