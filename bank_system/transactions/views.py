from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from accounts.models import Account

@login_required
def transaction_list(request):
    accounts = request.user.accounts.all()
    transactions = Transaction.objects.filter(
        from_account__in=accounts
    ) | Transaction.objects.filter(
        to_account__in=accounts
    )
    transactions = transactions.distinct().order_by('-created_at')
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})

@login_required
@transaction.atomic
def deposit(request, account_pk):
    account = get_object_or_404(Account, pk=account_pk, user=request.user)
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            trans = form.save(commit=False)
            trans.transaction_type = 'deposit'
            trans.to_account = account
            trans.save()
            
            account.balance += trans.amount
            account.save()
            
            messages.success(request, f'Successfully deposited ${trans.amount} to account {account.account_number}')
            return redirect('account_detail', pk=account.pk)
    else:
        form = DepositForm()
    
    return render(request, 'transactions/deposit.html', {'form': form, 'account': account})

@login_required
@transaction.atomic
def withdraw(request, account_pk):
    account = get_object_or_404(Account, pk=account_pk, user=request.user)
    
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > account.balance:
                messages.error(request, 'Insufficient balance!')
            else:
                trans = form.save(commit=False)
                trans.transaction_type = 'withdrawal'
                trans.from_account = account
                trans.save()
                
                account.balance -= trans.amount
                account.save()
                
                messages.success(request, f'Successfully withdrew ${trans.amount} from account {account.account_number}')
                return redirect('account_detail', pk=account.pk)
    else:
        form = WithdrawForm()
    
    return render(request, 'transactions/withdraw.html', {'form': form, 'account': account})

@login_required
@transaction.atomic
def transfer(request, account_pk):
    from_account = get_object_or_404(Account, pk=account_pk, user=request.user)
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            to_account = form.cleaned_data['to_account_number']
            
            if from_account == to_account:
                messages.error(request, 'Cannot transfer to the same account!')
            elif amount > from_account.balance:
                messages.error(request, 'Insufficient balance!')
            else:
                trans = form.save(commit=False)
                trans.transaction_type = 'transfer'
                trans.from_account = from_account
                trans.to_account = to_account
                trans.save()
                
                from_account.balance -= trans.amount
                to_account.balance += trans.amount
                from_account.save()
                to_account.save()
                
                messages.success(request, f'Successfully transferred ${trans.amount} to account {to_account.account_number}')
                return redirect('account_detail', pk=from_account.pk)
    else:
        form = TransferForm()
    
    return render(request, 'transactions/transfer.html', {'form': form, 'account': from_account})