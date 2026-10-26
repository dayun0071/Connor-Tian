"""Read-only report objects returned by the valuation service."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PositionView:
    ticker: str
    quantity: Decimal
    average_cost: Decimal
    current_price: Decimal | None
    market_value: Decimal | None
    unrealized_gain: Decimal | None


@dataclass(frozen=True)
class PortfolioView:
    name: str
    strategy: str
    positions: tuple[PositionView, ...]
    market_value: Decimal
    unrealized_gain: Decimal
    realized_gain: Decimal
    missing_prices: tuple[str, ...]
