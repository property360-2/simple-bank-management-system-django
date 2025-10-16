from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Account
from .forms import AccountForm

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})

@login_required
def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    
    # Get all transactions related to this account
    from transactions.models import Transaction
    transactions = Transaction.objects.filter(
        Q(from_account=account) | Q(to_account=account)
    ).order_by('-created_at')[:10]
    
    # Calculate statistics
    total_deposits = account.incoming_transactions.filter(transaction_type='deposit').count()
    total_withdrawals = account.outgoing_transactions.filter(transaction_type='withdrawal').count()
    total_transfers = account.outgoing_transactions.filter(transaction_type='transfer').count()
    
    return render(request, 'accounts/account_detail.html', {
        'account': account,
        'transactions': transactions,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'total_transfers': total_transfers,
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
        # Check if account has balance
        if account.balance > 0:
            messages.error(request, 'Cannot delete account with non-zero balance!')
            return redirect('account_detail', pk=account.pk)
        
        account_number = account.account_number
        account.delete()
        messages.success(request, f'Account {account_number} deleted successfully!')
        return redirect('account_list')
    return render(request, 'accounts/account_confirm_delete.html', {'account': account})