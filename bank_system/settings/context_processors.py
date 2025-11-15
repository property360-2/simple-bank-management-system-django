"""
Context processors for settings app
Provides currency and personalization data to templates
"""

from core.currency import CurrencyFormatter, get_currency_symbol, CURRENCY_CHOICES as AVAILABLE_CURRENCIES


def currency_context(request):
    """
    Add currency-related utilities to template context
    Available in all templates as:
    - currency_formatter: CurrencyFormatter class
    - user_currency: User's preferred currency code
    - currency_symbol: User's preferred currency symbol
    """
    context = {
        'currency_formatter': CurrencyFormatter,
        'currency_choices': AVAILABLE_CURRENCIES,
    }

    if request.user.is_authenticated:
        try:
            if hasattr(request.user, 'preferences'):
                user_currency = request.user.preferences.currency
                context['user_currency'] = user_currency
                context['currency_symbol'] = get_currency_symbol(user_currency)
        except Exception:
            pass

    return context
