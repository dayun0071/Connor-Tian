"""Portfolio membership, selection and deletion rules."""

import logging

from ..domain.portfolio import Portfolio
from ..errors import (
    DuplicatePortfolioError,
    NoPortfolioSelectedError,
    PortfolioNotEmptyError,
    PortfolioNotFoundError,
)
from ..validation import require_text

logger = logging.getLogger(__name__)
portfolios = {}
_selected_key = None


def _name_key(name):
    return require_text(name, "Portfolio name").casefold()


def create_portfolio(name, strategy):
    name = require_text(name, "Portfolio name")
    strategy = require_text(strategy, "Strategy")
    key = _name_key(name)
    if key in portfolios:
        raise DuplicatePortfolioError(f"Portfolio '{name}' already exists.")
    portfolio = Portfolio(name, strategy)
    portfolios[key] = portfolio
    logger.info("Created portfolio: %s", name)
    return portfolio


def get_portfolio(name):
    key = _name_key(name)
    try:
        return portfolios[key]
    except KeyError as error:
        raise PortfolioNotFoundError(f"No portfolio named '{name.strip()}'.") from error


def list_portfolios():
    return list(portfolios.values())


def select_portfolio(name):
    global _selected_key
    portfolio = get_portfolio(name)
    _selected_key = _name_key(portfolio.name)
    logger.info("Selected portfolio: %s", portfolio.name)
    return portfolio


def selected_name():
    if _selected_key is None:
        return None
    return portfolios[_selected_key].name


def get_selected_portfolio():
    if _selected_key is None:
        raise NoPortfolioSelectedError("Select a portfolio first.")
    return portfolios[_selected_key]


def delete_portfolio(name):
    global _selected_key
    portfolio = get_portfolio(name)
    if any(position.quantity > 0 for position in portfolio.positions.values()):
        raise PortfolioNotEmptyError("Sell all shares before deleting this portfolio.")
    key = _name_key(portfolio.name)
    del portfolios[key]
    if _selected_key == key:
        _selected_key = None
    logger.info("Deleted portfolio and its trade history: %s", portfolio.name)
