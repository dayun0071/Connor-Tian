"""The single cash balance shared by every portfolio."""

import logging
from decimal import Decimal

from ..errors import InsufficientFundsError, InvalidDepositError
from ..validation import require_number

logger = logging.getLogger(__name__)
_balance = Decimal("0")


def get_balance():
    return _balance


def deposit(amount):
    global _balance
    require_number(amount, "Deposit", InvalidDepositError, allow_zero=False)
    _balance = _balance + amount
    logger.info("Deposited %s; cash balance %s", amount, _balance)
    return _balance


def spend_on_purchase(amount):
    global _balance
    require_number(amount, "Purchase cost", allow_zero=False)
    if amount > _balance:
        raise InsufficientFundsError("Not enough cash for this purchase.")
    _balance = _balance - amount


def receive_sale_proceeds(amount):
    global _balance
    require_number(amount, "Sale proceeds")
    _balance = _balance + amount
