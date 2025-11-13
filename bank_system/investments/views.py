from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from decimal import Decimal

from .models import InvestmentPlatform, InvestmentProduct, Portfolio, InvestmentHolding, InvestmentTransaction
from accounts.models import Account
from transactions.models import Transaction


@login_required
def portfolio_list(request):
    """List all portfolios for the user"""
    portfolios = Portfolio.objects.filter(user=request.user)
    platforms = InvestmentPlatform.objects.filter(is_active=True)

    # Calculate totals
    total_invested = sum(p.total_invested for p in portfolios)
    total_value = sum(p.current_value for p in portfolios)
    total_return = total_value - total_invested

    context = {
        'portfolios': portfolios,
        'platforms': platforms,
        'total_invested': total_invested,
        'total_value': total_value,
        'total_return': total_return,
    }
    return render(request, 'investments/portfolio_list.html', context)


@login_required
def portfolio_detail(request, pk):
    """Detail view for a portfolio"""
    portfolio = get_object_or_404(Portfolio, pk=pk, user=request.user)
    holdings = portfolio.holdings.filter(status='active')
    transactions = portfolio.transactions.all()[:10]

    context = {
        'portfolio': portfolio,
        'holdings': holdings,
        'transactions': transactions,
    }
    return render(request, 'investments/portfolio_detail.html', context)


@login_required
@transaction.atomic
def create_portfolio(request):
    """Create a new portfolio"""
    if request.method == 'POST':
        account_id = request.POST.get('account')
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        try:
            account = Account.objects.get(pk=account_id, user=request.user)

            portfolio = Portfolio.objects.create(
                user=request.user,
                account=account,
                name=name,
                description=description
            )

            messages.success(request, f'Portfolio "{name}" created successfully!')
            return redirect('investments:portfolio_detail', pk=portfolio.pk)

        except Exception as e:
            messages.error(request, f'Error creating portfolio: {str(e)}')
            return redirect('investments:portfolio_list')

    accounts = Account.objects.filter(user=request.user, is_active=True)
    context = {
        'accounts': accounts,
    }
    return render(request, 'investments/create_portfolio.html', context)


@login_required
def products_list(request):
    """List all investment products"""
    platform_filter = request.GET.get('platform')
    risk_filter = request.GET.get('risk')

    products = InvestmentProduct.objects.filter(is_active=True)

    if platform_filter:
        products = products.filter(platform_id=platform_filter)
    if risk_filter:
        products = products.filter(risk_level=risk_filter)

    platforms = InvestmentPlatform.objects.filter(is_active=True)

    context = {
        'products': products,
        'platforms': platforms,
    }
    return render(request, 'investments/products_list.html', context)


@login_required
@transaction.atomic
def buy_investment(request, portfolio_id):
    """Buy an investment product"""
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id, user=request.user)

    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = Decimal(request.POST.get('quantity'))

        try:
            product = InvestmentProduct.objects.get(pk=product_id, is_active=True)
            total_cost = quantity * product.current_price

            # Check account balance
            if portfolio.account.balance < total_cost:
                messages.error(request, 'Insufficient balance in account')
                return redirect('investments:buy_investment', portfolio_id=portfolio_id)

            # Deduct from account
            portfolio.account.balance -= total_cost
            portfolio.account.save()

            # Create or update holding
            holding, created = InvestmentHolding.objects.get_or_create(
                portfolio=portfolio,
                product=product,
                status='active',
                defaults={
                    'quantity': quantity,
                    'purchase_price': product.current_price,
                    'current_price': product.current_price,
                }
            )

            if not created:
                # Update existing holding
                total_quantity = holding.quantity + quantity
                weighted_avg_price = ((holding.quantity * holding.purchase_price) + (quantity * product.current_price)) / total_quantity
                holding.quantity = total_quantity
                holding.purchase_price = weighted_avg_price
                holding.save()

            # Create transaction record
            InvestmentTransaction.objects.create(
                portfolio=portfolio,
                product=product,
                holding=holding,
                transaction_type='buy',
                quantity=quantity,
                price=product.current_price,
                total_amount=total_cost
            )

            # Update portfolio
            portfolio.total_invested += total_cost
            portfolio.update_portfolio_value()

            # Create account transaction
            Transaction.objects.create(
                from_account=portfolio.account,
                transaction_type='withdrawal',
                amount=total_cost,
                description=f'Investment: Buy {quantity} x {product.symbol}'
            )

            messages.success(request, f'Successfully purchased {quantity} shares of {product.symbol}!')
            return redirect('investments:portfolio_detail', pk=portfolio_id)

        except Exception as e:
            messages.error(request, f'Error purchasing investment: {str(e)}')
            return redirect('investments:buy_investment', portfolio_id=portfolio_id)

    products = InvestmentProduct.objects.filter(is_active=True)
    context = {
        'portfolio': portfolio,
        'products': products,
    }
    return render(request, 'investments/buy_investment.html', context)


@login_required
@transaction.atomic
def sell_investment(request, holding_id):
    """Sell an investment holding"""
    holding = get_object_or_404(InvestmentHolding, pk=holding_id, portfolio__user=request.user)

    if request.method == 'POST':
        quantity = Decimal(request.POST.get('quantity'))

        try:
            if quantity > holding.quantity:
                messages.error(request, 'Cannot sell more than you own')
                return redirect('investments:sell_investment', holding_id=holding_id)

            sale_value = quantity * holding.current_price

            # Add to account
            holding.portfolio.account.balance += sale_value
            holding.portfolio.account.save()

            # Update holding
            if quantity == holding.quantity:
                holding.status = 'sold'
                holding.quantity = 0
            else:
                holding.quantity -= quantity
                holding.status = 'partial_sold'
            holding.save()

            # Create transaction record
            InvestmentTransaction.objects.create(
                portfolio=holding.portfolio,
                product=holding.product,
                holding=holding,
                transaction_type='sell',
                quantity=quantity,
                price=holding.current_price,
                total_amount=sale_value
            )

            # Update portfolio
            holding.portfolio.update_portfolio_value()

            # Create account transaction
            Transaction.objects.create(
                to_account=holding.portfolio.account,
                transaction_type='deposit',
                amount=sale_value,
                description=f'Investment Sale: {quantity} x {holding.product.symbol}'
            )

            messages.success(request, f'Successfully sold {quantity} shares of {holding.product.symbol}!')
            return redirect('investments:portfolio_detail', pk=holding.portfolio.pk)

        except Exception as e:
            messages.error(request, f'Error selling investment: {str(e)}')
            return redirect('investments:sell_investment', holding_id=holding_id)

    context = {
        'holding': holding,
    }
    return render(request, 'investments/sell_investment.html', context)
