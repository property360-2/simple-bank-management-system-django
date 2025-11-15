"""
Template tags and filters for currency conversion and formatting
"""

from django import template
from django.utils.safestring import mark_safe
from core.currency import (
    convert_currency,
    format_currency,
    convert_and_format_currency,
    get_currency_symbol
)

register = template.Library()


@register.filter
def currency(value, currency_code='USD'):
    """
    Format a number as currency with the specified code
    Usage: {{ amount|currency:"PHP" }}
    """
    try:
        return mark_safe(format_currency(value, currency_code))
    except Exception:
        return value


@register.filter
def convert_curr(value, currencies):
    """
    Convert currency and format
    Usage: {{ amount|convert_curr:"USD,PHP" }}
    """
    try:
        from_curr, to_curr = currencies.split(',')
        return mark_safe(convert_and_format_currency(value, from_curr.strip(), to_curr.strip()))
    except Exception:
        return value


@register.filter
def currency_symbol(currency_code='USD'):
    """
    Get the symbol for a currency
    Usage: {{ "PHP"|currency_symbol }}
    """
    return get_currency_symbol(currency_code)


@register.simple_tag
def format_amount(amount, user=None, base_currency='USD'):
    """
    Format an amount in user's preferred currency
    Usage: {% format_amount amount user=request.user %}
    """
    try:
        if user and hasattr(user, 'preferences'):
            preferred_currency = user.preferences.currency
        else:
            preferred_currency = base_currency

        return mark_safe(convert_and_format_currency(amount, base_currency, preferred_currency))
    except Exception:
        return format_currency(amount, base_currency)


@register.simple_tag
def user_currency_symbol(user=None, default='USD'):
    """
    Get user's preferred currency symbol
    Usage: {% user_currency_symbol user=request.user %}
    """
    try:
        if user and hasattr(user, 'preferences'):
            return get_currency_symbol(user.preferences.currency)
        return get_currency_symbol(default)
    except Exception:
        return get_currency_symbol(default)
