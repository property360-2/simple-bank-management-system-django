"""
Context processors for settings app
Provides currency and personalization data to templates
"""

from core.currency import CurrencyFormatter, get_currency_symbol, CURRENCY_CHOICES as AVAILABLE_CURRENCIES


def currency_context(request):
    """
    Add currency-related utilities and personalization data to template context
    Available in all templates as:
    - currency_formatter: CurrencyFormatter class
    - user_currency: User's preferred currency code
    - currency_symbol: User's preferred currency symbol
    - user_theme: User's preferred theme ('dark' or 'light')
    - user_font_size: User's preferred font size ('small', 'medium', 'large')
    """
    context = {
        'currency_formatter': CurrencyFormatter,
        'currency_choices': AVAILABLE_CURRENCIES,
        'user_theme': 'dark',  # Default theme
        'user_font_size': 'medium',  # Default font size
    }

    if request.user.is_authenticated:
        try:
            if hasattr(request.user, 'preferences'):
                preferences = request.user.preferences
                user_currency = preferences.currency
                context['user_currency'] = user_currency
                context['currency_symbol'] = get_currency_symbol(user_currency)
                context['user_theme'] = preferences.theme
                context['user_font_size'] = preferences.font_size
        except Exception:
            pass

    return context
