from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from django.core.serializers.json import DjangoJSONEncoder
import json

from accounts.models import Account
from transactions.models import Transaction, FraudDetection
from savings.models import SavingsProduct, SavingsAccount
from investments.models import InvestmentProduct, Portfolio
from users.models import User
from users.decorators import manager_required


def get_transaction_chart_data():
    """Get transaction volume data for the last 30 days"""
    try:
        data = {}
        for i in range(30):
            date = timezone.now() - timedelta(days=29-i)
            date_key = date.strftime('%b %d')
            count = Transaction.objects.filter(
                created_at__date=date.date()
            ).count()
            data[date_key] = count
        return data
    except:
        return {}


def get_account_type_distribution():
    """Get distribution of account types"""
    try:
        distribution = Account.objects.values('account_type').annotate(
            count=Count('id')
        ).order_by('account_type')
        return {item['account_type']: item['count'] for item in distribution}
    except:
        return {}


def get_user_registration_trend():
    """Get new users registered in the last 30 days"""
    try:
        data = {}
        for i in range(30):
            date = timezone.now() - timedelta(days=29-i)
            date_key = date.strftime('%b %d')
            count = User.objects.filter(
                date_joined__date=date.date()
            ).count()
            data[date_key] = count
        return data
    except:
        return {}


def get_transaction_type_distribution():
    """Get distribution of transaction types"""
    try:
        distribution = Transaction.objects.values('transaction_type').annotate(
            count=Count('id')
        ).order_by('transaction_type')
        return {item['transaction_type']: item['count'] for item in distribution}
    except:
        return {}


def get_fraud_distribution():
    """Get distribution of fraud by risk level"""
    try:
        distribution = FraudDetection.objects.values('risk_level').annotate(
            count=Count('id')
        ).order_by('risk_level')
        return {item['risk_level']: item['count'] for item in distribution}
    except:
        return {}


@manager_required
def admin_dashboard(request):
    """Admin dashboard with business analytics"""
    # User analytics
    try:
        total_users = User.objects.count()
        active_users = User.objects.filter(last_login__isnull=False).count()
        new_users_this_month = User.objects.filter(
            date_joined__gte=timezone.now() - timedelta(days=30)
        ).count()
    except:
        total_users = active_users = new_users_this_month = 0

    # Account analytics
    try:
        total_accounts = Account.objects.count()
        total_balance = Account.objects.aggregate(total=Sum('balance'))['total'] or 0
        avg_balance = Account.objects.aggregate(avg=Avg('balance'))['avg'] or 0
    except:
        total_accounts = total_balance = avg_balance = 0

    # Transaction analytics
    try:
        total_transactions = Transaction.objects.count()
        this_month_transactions = Transaction.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()
        total_transaction_volume = Transaction.objects.aggregate(total=Sum('amount'))['total'] or 0
    except:
        total_transactions = this_month_transactions = total_transaction_volume = 0

    # Fraud alerts
    try:
        pending_fraud = FraudDetection.objects.filter(status='pending').count()
        critical_fraud = FraudDetection.objects.filter(
            risk_level='critical',
            status='pending'
        ).count()
        fraud_alerts = FraudDetection.objects.filter(status='pending')[:10]
    except:
        pending_fraud = critical_fraud = 0
        fraud_alerts = []

    # Savings analytics
    try:
        total_savings_products = SavingsProduct.objects.count()
        active_savings_accounts = SavingsAccount.objects.filter(status='active').count()
        total_savings_balance = SavingsAccount.objects.aggregate(total=Sum('balance'))['total'] or 0
    except:
        total_savings_products = active_savings_accounts = total_savings_balance = 0

    # Investment analytics
    try:
        total_investment_products = InvestmentProduct.objects.count()
        active_portfolios = Portfolio.objects.filter(status='active').count()
        total_portfolio_value = Portfolio.objects.aggregate(total=Sum('current_value'))['total'] or 0
    except:
        total_investment_products = active_portfolios = total_portfolio_value = 0

    # Get chart data
    transaction_chart_data = get_transaction_chart_data()
    account_type_data = get_account_type_distribution()
    user_registration_data = get_user_registration_trend()
    transaction_type_data = get_transaction_type_distribution()
    fraud_data = get_fraud_distribution()

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
        # Chart data as JSON
        'transaction_chart_data_json': json.dumps(transaction_chart_data, cls=DjangoJSONEncoder),
        'account_type_data_json': json.dumps(account_type_data, cls=DjangoJSONEncoder),
        'user_registration_data_json': json.dumps(user_registration_data, cls=DjangoJSONEncoder),
        'transaction_type_data_json': json.dumps(transaction_type_data, cls=DjangoJSONEncoder),
        'fraud_data_json': json.dumps(fraud_data, cls=DjangoJSONEncoder),
    }
    return render(request, 'admin/dashboard.html', context)


@manager_required
def fraud_detection_list(request):
    """List and manage fraud alerts"""
    status_filter = request.GET.get('status')
    risk_filter = request.GET.get('risk')

    try:
        frauds = FraudDetection.objects.all().order_by('-detected_at')

        if status_filter:
            frauds = frauds.filter(status=status_filter)
        if risk_filter:
            frauds = frauds.filter(risk_level=risk_filter)

        # Get statistics by status and risk
        pending_count = FraudDetection.objects.filter(status='pending').count()
        reviewing_count = FraudDetection.objects.filter(status='reviewed').count()
        resolved_count = FraudDetection.objects.filter(Q(status='approved') | Q(status='rejected')).count()
        high_risk_count = FraudDetection.objects.filter(risk_level='high').count()
    except:
        frauds = []
        pending_count = reviewing_count = resolved_count = high_risk_count = 0

    context = {
        'frauds': frauds,
        'pending_count': pending_count,
        'reviewing_count': reviewing_count,
        'resolved_count': resolved_count,
        'high_risk_count': high_risk_count,
        'current_status': status_filter,
        'current_risk': risk_filter,
    }
    return render(request, 'admin/fraud_detection_list.html', context)


@manager_required
def fraud_detection_detail(request, pk):
    """View and review fraud alert details"""
    try:
        fraud = get_object_or_404(FraudDetection, pk=pk)

        # Handle status changes via GET parameters for the template buttons
        if request.method == 'GET':
            action = request.GET.get('action')
            if action in ['review', 'approve', 'reject']:
                if action == 'review':
                    fraud.status = 'reviewed'
                    fraud.reviewed_by = request.user
                    fraud.reviewed_at = timezone.now()
                    fraud.save()
                    messages.success(request, 'Fraud case marked as reviewed')
                elif action == 'approve':
                    fraud.status = 'approved'
                    fraud.reviewed_by = request.user
                    fraud.reviewed_at = timezone.now()
                    fraud.save()
                    messages.success(request, 'Fraud alert approved')
                elif action == 'reject':
                    fraud.status = 'rejected'
                    fraud.reviewed_by = request.user
                    fraud.reviewed_at = timezone.now()
                    fraud.save()
                    messages.success(request, 'Fraud alert rejected')

                return redirect('admin_panel:fraud_detection_detail', pk=fraud.pk)

        context = {
            'fraud': fraud,
        }
        return render(request, 'admin/fraud_detection_detail.html', context)
    except:
        messages.error(request, 'Fraud detection data not available. Please run migrations.')
        return redirect('admin_panel:fraud_detection_list')
