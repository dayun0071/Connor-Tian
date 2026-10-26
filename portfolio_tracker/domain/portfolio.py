"""Portfolio, position and trade data, with no input/output or business logic."""

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Position:
    ticker: str
    quantity: Decimal
    average_cost: Decimal


@dataclass(frozen=True)
class Trade:
    side: str
    ticker: str
    quantity: Decimal
    price: Decimal
    realized_gain: Decimal = Decimal("0")


@dataclass
class Portfolio:
    name: str
    strategy: str
    positions: dict[str, Position] = field(default_factory=dict)
    trades: list[Trade] = field(default_factory=list)
    realized_gain: Decimal = Decimal("0")
