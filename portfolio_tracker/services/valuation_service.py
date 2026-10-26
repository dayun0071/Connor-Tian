"""Portfolio calculations, including incomplete valuations when quotes are missing."""

from decimal import Decimal

from ..domain.valuation import PortfolioView, PositionView
from .portfolio_service import get_selected_portfolio
from .price_service import get_price


def _value_position(position):
    price = get_price(position.ticker)
    market_value = None if price is None else price * position.quantity
    gain = None if price is None else (price - position.average_cost) * position.quantity
    return PositionView(position.ticker, position.quantity, position.average_cost,
                        price, market_value, gain)


def selected_portfolio_view():
    portfolio = get_selected_portfolio()
    rows = tuple(_value_position(position) for position in portfolio.positions.values())
    market_value = sum((row.market_value for row in rows if row.market_value is not None),
                       Decimal("0"))
    gain = sum((row.unrealized_gain for row in rows if row.unrealized_gain is not None),
               Decimal("0"))
    missing = tuple(row.ticker for row in rows if row.current_price is None)
    return PortfolioView(portfolio.name, portfolio.strategy, rows, market_value,
                         gain, portfolio.realized_gain, missing)
