"""Manually maintained market quotes, separate from asset definitions."""

import logging

from ..errors import InvalidPriceError
from ..validation import require_number
from .asset_service import get_asset

logger = logging.getLogger(__name__)
prices = {}


def set_price(ticker, price):
    asset = get_asset(ticker)
    require_number(price, "Current price", InvalidPriceError)
    prices[asset.ticker] = price
    logger.info("Set current price for %s to %s", asset.ticker, price)


def get_price(ticker):
    asset = get_asset(ticker)
    # None means no quote; zero is a valid quote for a worthless asset.
    return prices.get(asset.ticker)
