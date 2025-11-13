from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
import random

from .models import SavingsProduct, SavingsAccount, SavingsGoal, InterestTransaction
from accounts.models import Account


@login_required
def savings_list(request):
    """List all savings accounts for the user"""
    savings_accounts = SavingsAccount.objects.filter(user=request.user)
    products = SavingsProduct.objects.filter(is_active=True)

    context = {
        'savings_accounts': savings_accounts,
        'products': products,
    }
    return render(request, 'savings/savings_list.html', context)


@login_required
def savings_detail(request, pk):
    """Detail view for a savings account"""
    savings_account = get_object_or_404(SavingsAccount, pk=pk, user=request.user)
    interest_transactions = savings_account.interest_transactions.all()[:10]
    goals = savings_account.goals.filter(status='active')

    context = {
        'savings_account': savings_account,
        'interest_transactions': interest_transactions,
        'goals': goals,
    }
    return render(request, 'savings/savings_detail.html', context)


@login_required
@transaction.atomic
def create_savings_account(request):
    """Create a new savings account"""
    if request.method == 'POST':
        product_id = request.POST.get('product')
        account_id = request.POST.get('account')
        initial_deposit = request.POST.get('initial_deposit', 0)

        try:
            product = SavingsProduct.objects.get(pk=product_id, is_active=True)
            account = Account.objects.get(pk=account_id, user=request.user)
            initial_deposit = Decimal(initial_deposit)

            # Validate minimum balance
            if initial_deposit < product.min_balance:
                messages.error(request, f'Initial deposit must be at least ${product.min_balance}')
                return redirect('savings:savings_list')

            # Deduct from account if initial deposit
            if initial_deposit > 0:
                if account.balance < initial_deposit:
                    messages.error(request, 'Insufficient balance in account')
                    return redirect('savings:savings_list')
                account.balance -= initial_deposit
                account.save()

            # Generate account number
            account_number = f"SAV{random.randint(10000000, 99999999)}"
            while SavingsAccount.objects.filter(account_number=account_number).exists():
                account_number = f"SAV{random.randint(10000000, 99999999)}"

            # Create savings account
            savings_account = SavingsAccount.objects.create(
                user=request.user,
                product=product,
                account=account,
                account_number=account_number,
                balance=initial_deposit
            )

            messages.success(request, f'Savings account {account_number} created successfully!')
            return redirect('savings:savings_detail', pk=savings_account.pk)

        except Exception as e:
            messages.error(request, f'Error creating savings account: {str(e)}')
            return redirect('savings:savings_list')

    products = SavingsProduct.objects.filter(is_active=True)
    accounts = Account.objects.filter(user=request.user, is_active=True)

    context = {
        'products': products,
        'accounts': accounts,
    }
    return render(request, 'savings/create_savings_account.html', context)


@login_required
@transaction.atomic
def create_goal(request, savings_account_id):
    """Create a savings goal"""
    savings_account = get_object_or_404(SavingsAccount, pk=savings_account_id, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        target_amount = Decimal(request.POST.get('target_amount'))
        target_date = request.POST.get('target_date')

        SavingsGoal.objects.create(
            user=request.user,
            savings_account=savings_account,
            name=name,
            description=description,
            target_amount=target_amount,
            target_date=target_date
        )

        messages.success(request, f'Savings goal "{name}" created successfully!')
        return redirect('savings:savings_detail', pk=savings_account_id)

    context = {
        'savings_account': savings_account,
    }
    return render(request, 'savings/create_goal.html', context)


@login_required
def goals_list(request):
    """List all savings goals"""
    goals = SavingsGoal.objects.filter(user=request.user)
    context = {
        'goals': goals,
    }
    return render(request, 'savings/goals_list.html', context)
