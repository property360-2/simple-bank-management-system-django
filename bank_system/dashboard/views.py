from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from transactions.models import Transaction
from savings.models import SavingsAccount, SavingsGoal
from investments.models import Portfolio
from django.db.models import Sum, Q

@login_required
def dashboard(request):
    accounts = Account.objects.filter(user=request.user, is_active=True)
    total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0

    # Get recent transactions for user's accounts
    recent_transactions = Transaction.objects.filter(
        Q(from_account__in=accounts) | Q(to_account__in=accounts)
    ).distinct().order_by('-created_at')[:5]

    # Savings data
    savings_accounts = SavingsAccount.objects.filter(user=request.user, status='active')
    total_savings = savings_accounts.aggregate(total=Sum('balance'))['total'] or 0
    total_interest_earned = savings_accounts.aggregate(total=Sum('interest_earned'))['total'] or 0

    # Savings goals
    active_goals = SavingsGoal.objects.filter(user=request.user, status='active')

    # Investment data
    portfolios = Portfolio.objects.filter(user=request.user, status='active')
    total_invested = portfolios.aggregate(total=Sum('total_invested'))['total'] or 0
    total_investment_value = portfolios.aggregate(total=Sum('current_value'))['total'] or 0
    investment_return = total_investment_value - total_invested

    # Calculate total net worth
    total_net_worth = total_balance + total_savings + total_investment_value

    context = {
        'accounts': accounts,
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'account_count': accounts.count(),

        # Savings
        'savings_accounts': savings_accounts[:3],
        'total_savings': total_savings,
        'total_interest_earned': total_interest_earned,
        'savings_count': savings_accounts.count(),
        'active_goals': active_goals[:3],

        # Investments
        'portfolios': portfolios[:3],
        'total_invested': total_invested,
        'total_investment_value': total_investment_value,
        'investment_return': investment_return,
        'portfolio_count': portfolios.count(),

        # Overall
        'total_net_worth': total_net_worth,
    }
    return render(request, 'dashboard/dashboard.html', context)