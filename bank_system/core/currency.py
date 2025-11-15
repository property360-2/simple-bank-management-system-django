"""
Currency conversion and formatting utilities
Handles currency conversion, exchange rates, and formatting
"""

from decimal import Decimal
from django.core.cache import cache

# Exchange rates relative to USD (base currency)
# These are approximate rates - in production, you'd fetch from an API like:
# - Open Exchange Rates (openexchangerates.org)
# - Fixer.io (fixer.io)
# - CoinGecko API for crypto
# - Alpha Vantage
EXCHANGE_RATES = {
    'USD': Decimal('1.00'),
    'PHP': Decimal('56.50'),      # 1 USD = ~56.50 PHP
    'EUR': Decimal('0.92'),        # 1 USD = ~0.92 EUR
    'GBP': Decimal('0.79'),        # 1 USD = ~0.79 GBP
    'JPY': Decimal('149.50'),      # 1 USD = ~149.50 JPY
    'AUD': Decimal('1.52'),        # 1 USD = ~1.52 AUD
    'CAD': Decimal('1.36'),        # 1 USD = ~1.36 CAD
    'SGD': Decimal('1.34'),        # 1 USD = ~1.34 SGD
    'HKD': Decimal('7.85'),        # 1 USD = ~7.85 HKD
    'INR': Decimal('83.12'),       # 1 USD = ~83.12 INR
    'MYR': Decimal('4.75'),        # 1 USD = ~4.75 MYR
    'THB': Decimal('35.40'),       # 1 USD = ~35.40 THB
    'VND': Decimal('24700.00'),    # 1 USD = ~24700 VND
    'IDR': Decimal('15800.00'),    # 1 USD = ~15800 IDR
    'BTC': Decimal('0.000024'),    # 1 USD = ~0.000024 BTC
    'ETH': Decimal('0.00055'),     # 1 USD = ~0.00055 ETH
    'USDT': Decimal('1.00'),       # USDT is pegged to USD
}

# Currency symbols for display
CURRENCY_SYMBOLS = {
    'USD': '$',
    'PHP': '₱',
    'EUR': '€',
    'GBP': '£',
    'JPY': '¥',
    'AUD': 'A$',
    'CAD': 'C$',
    'SGD': 'S$',
    'HKD': 'HK$',
    'INR': '₹',
    'MYR': 'RM',
    'THB': '฿',
    'VND': '₫',
    'IDR': 'Rp',
    'BTC': '₿',
    'ETH': 'Ξ',
    'USDT': '₮',
}

# Decimal places for each currency
DECIMAL_PLACES = {
    'USD': 2,
    'PHP': 2,
    'EUR': 2,
    'GBP': 2,
    'JPY': 0,      # Japanese Yen doesn't use decimals
    'AUD': 2,
    'CAD': 2,
    'SGD': 2,
    'HKD': 2,
    'INR': 2,
    'MYR': 2,
    'THB': 2,
    'VND': 0,      # Vietnamese Dong doesn't use decimals
    'IDR': 0,      # Indonesian Rupiah doesn't use decimals
    'BTC': 8,      # Bitcoin uses up to 8 decimal places
    'ETH': 8,      # Ethereum uses up to 8 decimal places
    'USDT': 2,
}


def convert_currency(amount, from_currency='USD', to_currency='USD'):
    """
    Convert an amount from one currency to another

    Args:
        amount (Decimal or float): The amount to convert
        from_currency (str): Source currency code (default: USD)
        to_currency (str): Target currency code (default: USD)

    Returns:
        Decimal: Converted amount
    """
    if from_currency == to_currency:
        return Decimal(str(amount))

    # Convert amount to USD first (base currency)
    amount_decimal = Decimal(str(amount))
    if from_currency in EXCHANGE_RATES:
        amount_in_usd = amount_decimal / EXCHANGE_RATES[from_currency]
    else:
        # If currency not found, return original amount
        return amount_decimal

    # Convert from USD to target currency
    if to_currency in EXCHANGE_RATES:
        converted_amount = amount_in_usd * EXCHANGE_RATES[to_currency]
    else:
        # If currency not found, return original amount
        return amount_decimal

    return converted_amount


def format_currency(amount, currency='USD'):
    """
    Format an amount in a specific currency with proper symbol and decimal places

    Args:
        amount (Decimal or float): The amount to format
        currency (str): Currency code (default: USD)

    Returns:
        str: Formatted currency string (e.g., "$1,234.56")
    """
    symbol = CURRENCY_SYMBOLS.get(currency, currency)
    decimal_places = DECIMAL_PLACES.get(currency, 2)

    amount_decimal = Decimal(str(amount))

    # Format the number with proper decimal places and thousand separators
    format_string = f'{{:,.{decimal_places}f}}'
    formatted_number = format_string.format(amount_decimal)

    return f'{symbol}{formatted_number}'


def convert_and_format_currency(amount, from_currency='USD', to_currency='USD'):
    """
    Convert and format an amount in one operation

    Args:
        amount (Decimal or float): The amount to convert
        from_currency (str): Source currency code (default: USD)
        to_currency (str): Target currency code (default: USD)

    Returns:
        str: Formatted converted currency string
    """
    converted = convert_currency(amount, from_currency, to_currency)
    return format_currency(converted, to_currency)


def get_currency_symbol(currency='USD'):
    """Get the symbol for a currency"""
    return CURRENCY_SYMBOLS.get(currency, currency)


def get_decimal_places(currency='USD'):
    """Get the number of decimal places for a currency"""
    return DECIMAL_PLACES.get(currency, 2)


def get_exchange_rate(from_currency='USD', to_currency='USD'):
    """
    Get the exchange rate between two currencies

    Returns:
        Decimal: Exchange rate (how much of to_currency equals 1 from_currency)
    """
    if from_currency == to_currency:
        return Decimal('1.00')

    if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
        return None

    from_rate = EXCHANGE_RATES[from_currency]
    to_rate = EXCHANGE_RATES[to_currency]

    return to_rate / from_rate


# Example usage in templates via context processors or custom template filters
class CurrencyFormatter:
    """Utility class for currency operations"""

    @staticmethod
    def convert(amount, from_currency='USD', to_currency='USD'):
        return convert_currency(amount, from_currency, to_currency)

    @staticmethod
    def format(amount, currency='USD'):
        return format_currency(amount, currency)

    @staticmethod
    def convert_and_format(amount, from_currency='USD', to_currency='USD'):
        return convert_and_format_currency(amount, from_currency, to_currency)

    @staticmethod
    def get_symbol(currency='USD'):
        return get_currency_symbol(currency)
