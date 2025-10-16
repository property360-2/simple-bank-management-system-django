from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from transactions.models import Transaction
from django.db.models import Sum, Q

@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user, is_active=True)
    total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0
    
    # Get recent transactions for user's accounts
    recent_transactions = Transaction.objects.filter(
        Q(from_account__in=accounts) | Q(to_account__in=accounts)
    ).distinct().order_by('-created_at')[:5]
    
    context = {
        'accounts': accounts,
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'account_count': accounts.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)