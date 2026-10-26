"""Shared value checks used by services, independent of any interface."""

from decimal import Decimal

from .errors import InvalidNumberError, InvalidQuantityError, InvalidTextError


def require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise InvalidTextError(f"{label} cannot be blank.")
    return value.strip()


def normalize_ticker(ticker):
    return require_text(ticker, "Ticker").upper()


def require_number(value, label, error_type=InvalidNumberError, allow_zero=True):
    if not isinstance(value, Decimal) or not value.is_finite():
        raise error_type(f"{label} must be a finite decimal number.")
    if value < 0 or (not allow_zero and value == 0):
        rule = "zero or greater" if allow_zero else "greater than zero"
        raise error_type(f"{label} must be {rule}.")
    return value


def require_quantity(quantity):
    require_number(quantity, "Quantity", InvalidQuantityError, allow_zero=False)
    if quantity != quantity.to_integral_value():
        raise InvalidQuantityError("Quantity must be a whole number of shares.")
    return quantity
