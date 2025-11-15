"""Business Intelligence views with SARIMA forecasting and descriptive analytics"""
from django.shortcuts import render
from django.db.models import Sum, Avg, Count, StdDev, Min, Max
from django.utils import timezone
from datetime import timedelta
import json
from decimal import Decimal
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from django.core.serializers.json import DjangoJSONEncoder

from accounts.models import Account
from transactions.models import Transaction
from users.models import User
from users.decorators import manager_required

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


def get_daily_transaction_data(days=90):
    """Get daily transaction data for the specified number of days"""
    try:
        data = {}
        for i in range(days):
            date = timezone.now() - timedelta(days=days-1-i)
            date_key = date.strftime('%Y-%m-%d')
            total = Transaction.objects.filter(
                created_at__date=date.date()
            ).aggregate(total=Sum('amount'))['total'] or 0
            data[date_key] = float(total)
        return data
    except:
        return {}


def get_descriptive_analytics():
    """Get descriptive statistics for transactions"""
    try:
        transactions = Transaction.objects.all()
        amounts = list(transactions.values_list('amount', flat=True))

        if not amounts:
            return {}

        amounts = [float(a) for a in amounts]
        amounts_array = np.array(amounts)

        return {
            'count': len(amounts),
            'mean': float(np.mean(amounts_array)),
            'median': float(np.median(amounts_array)),
            'std_dev': float(np.std(amounts_array)),
            'min': float(np.min(amounts_array)),
            'max': float(np.max(amounts_array)),
            'q25': float(np.percentile(amounts_array, 25)),
            'q75': float(np.percentile(amounts_array, 75)),
            'skewness': float(pd.Series(amounts).skew()),
            'kurtosis': float(pd.Series(amounts).kurtosis()),
        }
    except:
        return {}


def forecast_transaction_volume(data_dict, periods=30):
    """Forecast transaction volume using SARIMA model"""
    try:
        if not data_dict or len(data_dict) < 30:
            return {}

        # Prepare data as pandas Series
        dates = sorted(data_dict.keys())
        values = [data_dict[date] for date in dates]
        ts_data = pd.Series(values, index=pd.to_datetime(dates))

        # Handle zero or very small variance
        if ts_data.std() < 1:
            # Return simple forecast based on mean
            mean_val = ts_data.mean()
            future_dates = pd.date_range(start=ts_data.index[-1] + timedelta(days=1), periods=periods, freq='D')
            forecast = {date.strftime('%Y-%m-%d'): mean_val for date in future_dates}
            return forecast

        try:
            # Fit SARIMA model (simpler parameters for small datasets)
            # Parameters: (p, d, q) x (P, D, Q, s)
            # Using conservative parameters: (1,1,1) x (1,1,1,7) for weekly seasonality
            model = SARIMAX(
                ts_data,
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 7),
                enforce_stationarity=False,
                enforce_invertibility=False
            )

            results = model.fit(disp=False, maxiter=200)
            forecast_data = results.get_forecast(steps=periods)
            forecast_values = forecast_data.predicted_mean

            # Create forecast dictionary
            future_dates = pd.date_range(start=ts_data.index[-1] + timedelta(days=1), periods=periods, freq='D')
            forecast = {
                date.strftime('%Y-%m-%d'): max(0, float(value))  # Ensure non-negative values
                for date, value in zip(future_dates, forecast_values)
            }
            return forecast
        except Exception as e:
            # Fallback to simple exponential smoothing if SARIMA fails
            mean_val = ts_data.mean()
            trend = (ts_data.iloc[-1] - ts_data.iloc[0]) / len(ts_data)
            future_dates = pd.date_range(start=ts_data.index[-1] + timedelta(days=1), periods=periods, freq='D')
            forecast = {
                date.strftime('%Y-%m-%d'): max(0, mean_val + trend * i)
                for i, date in enumerate(future_dates, 1)
            }
            return forecast
    except:
        return {}


def get_account_balance_analytics():
    """Get analytics about account balances"""
    try:
        accounts = Account.objects.all()
        balances = list(accounts.values_list('balance', flat=True))

        if not balances:
            return {}

        balances = [float(b) for b in balances]
        balances_array = np.array(balances)

        return {
            'total_balance': float(sum(balances)),
            'average_balance': float(np.mean(balances_array)),
            'median_balance': float(np.median(balances_array)),
            'std_dev': float(np.std(balances_array)),
            'min_balance': float(np.min(balances_array)),
            'max_balance': float(np.max(balances_array)),
            'percentile_25': float(np.percentile(balances_array, 25)),
            'percentile_75': float(np.percentile(balances_array, 75)),
        }
    except:
        return {}


def get_user_activity_analytics():
    """Get analytics about user activity"""
    try:
        users = User.objects.all()

        total_users = users.count()
        active_users = users.filter(last_login__isnull=False).count()

        # Activity in last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        active_last_month = users.filter(last_login__gte=thirty_days_ago).count()

        # Transaction activity
        transactions = Transaction.objects.all()
        avg_transactions_per_user = transactions.count() / total_users if total_users > 0 else 0

        return {
            'total_users': total_users,
            'active_users': active_users,
            'active_last_month': active_last_month,
            'avg_transactions_per_user': float(avg_transactions_per_user),
            'activity_rate': float(active_users / total_users * 100) if total_users > 0 else 0,
        }
    except:
        return {}


@manager_required
def business_intelligence(request):
    """Business Intelligence dashboard with forecasting and analytics"""

    # Get transaction volume data
    transaction_data = get_daily_transaction_data(90)

    # Get forecast for next 30 days
    forecast_data = forecast_transaction_volume(transaction_data, 30)

    # Get descriptive analytics
    transaction_analytics = get_descriptive_analytics()
    account_analytics = get_account_balance_analytics()
    user_analytics = get_user_activity_analytics()

    # Combine historical and forecast data for visualization
    combined_data = {**transaction_data, **forecast_data}

    context = {
        'transaction_data_json': json.dumps(transaction_data, cls=DjangoJSONEncoder),
        'forecast_data_json': json.dumps(forecast_data, cls=DjangoJSONEncoder),
        'combined_data_json': json.dumps(combined_data, cls=DjangoJSONEncoder),
        'transaction_analytics': transaction_analytics,
        'account_analytics': account_analytics,
        'user_analytics': user_analytics,
    }

    return render(request, 'admin/business_intelligence.html', context)
