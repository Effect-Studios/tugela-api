from decimal import Decimal

from django.conf import settings
from djmoney.contrib.exchange.backends import OpenExchangeRatesBackend
from djmoney.contrib.exchange.exceptions import MissingRate
from djmoney.contrib.exchange.models import get_rate as rates


# update rates
def update_rates(currency=None):
    backend = OpenExchangeRatesBackend()
    if currency and currency not in settings.SYMBOLS:
        settings.SYMBOLS += f",{currency}"
    backend.update_rates(symbols=settings.SYMBOLS)


def get_rate(currency="GHS", base_currency=settings.BASE_CURRENCY):
    try:
        return rates(base_currency, currency, backend=OpenExchangeRatesBackend.name)
    except MissingRate:
        update_rates(currency=currency)
        return get_rate(currency=currency, base_currency=base_currency)


# This is kind of reversed because base currency is constant (USD)
def rate_conversion(amount: int, currency="GHS", base_currency=settings.BASE_CURRENCY):
    rate = get_rate(currency=currency, base_currency=base_currency)

    conv_amt = Decimal(amount / rate)
    return round(conv_amt, 2)


def currency_conversion(
    amount: int, currency="GHS", base_currency=settings.BASE_CURRENCY
):
    rate = get_rate(currency=currency, base_currency=base_currency)

    conv_amt = Decimal(amount * rate)
    return round(conv_amt, 2)
