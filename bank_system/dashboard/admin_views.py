from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import timedelta

from accounts.models import Account
from transactions.models import Transaction, FraudDetection
from savings.models import SavingsProduct, SavingsAccount
from investments.models import InvestmentProduct, Portfolio
from users.models import User


def admin_required(user):
    """Check if user is staff/admin"""
    return user.is_staff


@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    """Admin dashboard with business analytics"""
    # User analytics
    total_users = User.objects.count()
    active_users = User.objects.filter(last_login__isnull=False).count()
    new_users_this_month = User.objects.filter(
        date_joined__gte=timezone.now() - timedelta(days=30)
    ).count()

    # Account analytics
    total_accounts = Account.objects.count()
    total_balance = Account.objects.aggregate(total=Sum('balance'))['total'] or 0
    avg_balance = Account.objects.aggregate(avg=Avg('balance'))['avg'] or 0

    # Transaction analytics
    total_transactions = Transaction.objects.count()
    this_month_transactions = Transaction.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=30)
    ).count()
    total_transaction_volume = Transaction.objects.aggregate(total=Sum('amount'))['total'] or 0

    # Fraud alerts
    pending_fraud = FraudDetection.objects.filter(status='pending').count()
    critical_fraud = FraudDetection.objects.filter(
        risk_level='critical',
        status='pending'
    ).count()
    fraud_alerts = FraudDetection.objects.filter(status='pending')[:10]

    # Savings analytics
    total_savings_products = SavingsProduct.objects.count()
    active_savings_accounts = SavingsAccount.objects.filter(status='active').count()
    total_savings_balance = SavingsAccount.objects.aggregate(total=Sum('balance'))['total'] or 0

    # Investment analytics
    total_investment_products = InvestmentProduct.objects.count()
    active_portfolios = Portfolio.objects.filter(status='active').count()
    total_portfolio_value = Portfolio.objects.aggregate(total=Sum('current_value'))['total'] or 0

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'new_users_this_month': new_users_this_month,
        'total_accounts': total_accounts,
        'total_balance': total_balance,
        'avg_balance': avg_balance,
        'total_transactions': total_transactions,
        'this_month_transactions': this_month_transactions,
        'total_transaction_volume': total_transaction_volume,
        'pending_fraud': pending_fraud,
        'critical_fraud': critical_fraud,
        'fraud_alerts': fraud_alerts,
        'total_savings_products': total_savings_products,
        'active_savings_accounts': active_savings_accounts,
        'total_savings_balance': total_savings_balance,
        'total_investment_products': total_investment_products,
        'active_portfolios': active_portfolios,
        'total_portfolio_value': total_portfolio_value,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
@user_passes_test(admin_required)
def fraud_detection_list(request):
    """List and manage fraud alerts"""
    status_filter = request.GET.get('status', 'pending')
    risk_filter = request.GET.get('risk')

    frauds = FraudDetection.objects.all()

    if status_filter:
        frauds = frauds.filter(status=status_filter)
    if risk_filter:
        frauds = frauds.filter(risk_level=risk_filter)

    # Get statistics
    pending_count = FraudDetection.objects.filter(status='pending').count()
    critical_count = FraudDetection.objects.filter(risk_level='critical', status='pending').count()

    context = {
        'frauds': frauds,
        'pending_count': pending_count,
        'critical_count': critical_count,
        'current_status': status_filter,
        'current_risk': risk_filter,
    }
    return render(request, 'admin/fraud_detection_list.html', context)


@login_required
@user_passes_test(admin_required)
def fraud_detection_detail(request, pk):
    """View and review fraud alert details"""
    fraud = get_object_or_404(FraudDetection, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')

        if action == 'approve':
            fraud.status = 'approved'
            fraud.notes = notes
            fraud.reviewed_by = request.user
            fraud.reviewed_at = timezone.now()
            fraud.save()
            messages.success(request, 'Fraud alert approved')
        elif action == 'reject':
            fraud.status = 'rejected'
            fraud.notes = notes
            fraud.reviewed_by = request.user
            fraud.reviewed_at = timezone.now()
            fraud.save()
            messages.success(request, 'Fraud alert rejected')

        return redirect('admin:fraud_detection_list')

    context = {
        'fraud': fraud,
    }
    return render(request, 'admin/fraud_detection_detail.html', context)
