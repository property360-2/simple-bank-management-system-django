from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from transactions.models import Transaction
from django.db.models import Sum

@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0
    
    recent_transactions = Transaction.objects.filter(
        from_account__in=accounts
    ) | Transaction.objects.filter(
        to_account__in=accounts
    )
    recent_transactions = recent_transactions.distinct().order_by('-created_at')[:5]
    
    context = {
        'accounts': accounts,
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'account_count': accounts.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)