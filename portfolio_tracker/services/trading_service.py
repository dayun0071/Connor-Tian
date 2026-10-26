"""Whole-share trading and weighted-average cost calculations."""

import logging
from decimal import Decimal

from ..domain.portfolio import Position, Trade
from ..errors import InsufficientSharesError, InvalidPriceError
from ..validation import require_number, require_quantity
from . import cash_service
from .asset_service import get_asset
from .portfolio_service import get_selected_portfolio

logger = logging.getLogger(__name__)


def buy(ticker, quantity, price):
    portfolio = get_selected_portfolio()
    asset = get_asset(ticker)
    require_quantity(quantity)
    require_number(price, "Buy price", InvalidPriceError, allow_zero=False)
    position = portfolio.positions.get(asset.ticker)
    old_quantity = position.quantity if position else Decimal("0")
    old_average = position.average_cost if position else Decimal("0")
    cost = quantity * price
    new_quantity = old_quantity + quantity
    new_average = (old_quantity * old_average + cost) / new_quantity
    # Complete checks and arithmetic before changing cash or holdings.
    cash_service.spend_on_purchase(cost)
    portfolio.positions[asset.ticker] = Position(asset.ticker, new_quantity, new_average)
    trade = Trade("BUY", asset.ticker, quantity, price)
    portfolio.trades.append(trade)
    logger.info("Bought %s %s at %s in %s", quantity, asset.ticker, price, portfolio.name)
    return trade


def sell(ticker, quantity, price):
    portfolio = get_selected_portfolio()
    asset = get_asset(ticker)
    require_quantity(quantity)
    require_number(price, "Sell price", InvalidPriceError)
    position = portfolio.positions.get(asset.ticker)
    if position is None or quantity > position.quantity:
        raise InsufficientSharesError("Not enough shares in the selected portfolio.")
    proceeds = quantity * price
    gain = (price - position.average_cost) * quantity
    remaining = position.quantity - quantity
    new_realized_gain = portfolio.realized_gain + gain
    cash_service.receive_sale_proceeds(proceeds)
    portfolio.realized_gain = new_realized_gain
    # Realized gains and trades belong to the portfolio, not to the remaining position.
    if remaining == 0:
        del portfolio.positions[asset.ticker]
    else:
        position.quantity = remaining
    trade = Trade("SELL", asset.ticker, quantity, price, gain)
    portfolio.trades.append(trade)
    logger.info("Sold %s %s at %s in %s; realized gain %s", quantity, asset.ticker,
                price, portfolio.name, gain)
    return trade
