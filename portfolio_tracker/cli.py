"""Input, presentation and expected-error handling for the command-line app."""

import logging
from decimal import Decimal, DecimalException, InvalidOperation

from .errors import InvalidNumberError, PortfolioTrackerError
from .services import (
    asset_service,
    cash_service,
    portfolio_service,
    price_service,
    trading_service,
    valuation_service,
)

logger = logging.getLogger(__name__)


def _money(value):
    if value is None:
        return "N/A (no current price)"
    # Scientific notation avoids huge output for unusually large/small input.
    if value != 0 and not -6 <= value.copy_abs().adjusted() <= 12:
        return f"${value:.6E}"
    return f"${value:,.2f}"


def _read_decimal(prompt):
    text = input(prompt).strip()
    try:
        return Decimal(text)
    except InvalidOperation as error:
        raise InvalidNumberError("Enter a number such as 10 or 12.50, without a currency sign.") from error


def show_welcome():
    print("\nWelcome to Portfolio Tracker")
    print("Data is kept in memory for this session only. Prices are entered manually.")


def show_menu():
    selected = portfolio_service.selected_name() or "None"
    print(f"\nSelected portfolio: {selected} | Shared cash: {_money(cash_service.get_balance())}")
    for choice, (label, handler) in MENU.items():
        print(f"{choice}. {label}")
    print("0. Quit")


def handle_add_asset():
    ticker = input("Enter ticker: ")
    name = input("Enter asset name: ")
    asset = asset_service.add_asset(ticker, name)
    print(f"Asset {asset.ticker} added successfully.")


def handle_view_assets():
    assets = asset_service.list_assets()
    if not assets:
        print("No assets yet.")
        return
    for asset in assets:
        price = price_service.get_price(asset.ticker)
        price_text = "Not set" if price is None else _money(price)
        print(f"{asset.ticker} | {asset.name} | Current price: {price_text}")


def handle_set_price():
    ticker = input("Enter ticker: ")
    price = _read_decimal("Current price per share: ")
    price_service.set_price(ticker, price)
    print("Current price updated.")


def handle_create_portfolio():
    name = input("Portfolio name: ")
    strategy = input("Investment strategy: ")
    portfolio = portfolio_service.create_portfolio(name, strategy)
    print(f"Created '{portfolio.name}'. Use option 6 to select it before trading.")


def handle_list_portfolios():
    portfolios = portfolio_service.list_portfolios()
    if not portfolios:
        print("No portfolios yet.")
        return
    selected = portfolio_service.selected_name()
    for portfolio in portfolios:
        marker = " [selected]" if portfolio.name == selected else ""
        print(f"{portfolio.name}{marker} | Strategy: {portfolio.strategy}")


def handle_select_portfolio():
    portfolio = portfolio_service.select_portfolio(input("Portfolio name to select: "))
    print(f"Selected '{portfolio.name}'.")


def handle_delete_portfolio():
    name = input("Empty portfolio to delete: ")
    portfolio_service.delete_portfolio(name)
    print("Portfolio, its trade history and its realized gains removed. Cash is unchanged.")


def handle_view_portfolio():
    view = valuation_service.selected_portfolio_view()
    print(f"\nPortfolio: {view.name}\nStrategy: {view.strategy}")
    if not view.positions:
        print("No shares held.")
    for position in view.positions:
        print(f"\n{position.ticker} | Quantity: {position.quantity}")
        print(f"  Average cost: {_money(position.average_cost)}")
        print(f"  Current price: {_money(position.current_price)}")
        print(f"  Market value: {_money(position.market_value)}")
        print(f"  Unrealized gain/loss: {_money(position.unrealized_gain)}")
    if view.missing_prices:
        print("\nValuation INCOMPLETE: missing prices for " + ", ".join(view.missing_prices))
        print(f"Known-price market value subtotal: {_money(view.market_value)}")
        print(f"Known-price unrealized gain/loss subtotal: {_money(view.unrealized_gain)}")
    else:
        print(f"\nTotal market value: {_money(view.market_value)}")
        print(f"Total unrealized gain/loss: {_money(view.unrealized_gain)}")
    print(f"Total realized gain/loss: {_money(view.realized_gain)}")


def handle_deposit():
    balance = cash_service.deposit(_read_decimal("Deposit amount: "))
    print(f"Deposit accepted. Shared cash: {_money(balance)}")


def handle_cash_balance():
    print(f"Shared cash balance: {_money(cash_service.get_balance())}")


def _read_trade():
    ticker = input("Enter ticker: ")
    quantity = _read_decimal("Number of shares (whole shares only): ")
    price = _read_decimal("Trade price per share: ")
    return ticker, quantity, price


def handle_buy():
    trade = trading_service.buy(*_read_trade())
    print(f"Bought {trade.quantity} shares of {trade.ticker} at {_money(trade.price)} each.")
    handle_cash_balance()


def handle_sell():
    trade = trading_service.sell(*_read_trade())
    print(f"Sold {trade.quantity} shares of {trade.ticker} at {_money(trade.price)} each.")
    print(f"Realized gain/loss on this sale: {_money(trade.realized_gain)}")
    handle_cash_balance()


MENU = {
    "1": ("View assets", handle_view_assets),
    "2": ("Add asset", handle_add_asset),
    "3": ("Set current asset price", handle_set_price),
    "4": ("Create portfolio", handle_create_portfolio),
    "5": ("List portfolios", handle_list_portfolios),
    "6": ("Select portfolio", handle_select_portfolio),
    "7": ("Delete empty portfolio", handle_delete_portfolio),
    "8": ("View selected portfolio", handle_view_portfolio),
    "9": ("Deposit funds", handle_deposit),
    "10": ("View cash balance", handle_cash_balance),
    "11": ("Buy shares", handle_buy),
    "12": ("Sell shares", handle_sell),
}


def run_cli():
    show_welcome()
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            logger.info("User selected quit")
            print("Goodbye!")
            return
        if choice not in MENU:
            logger.warning("Invalid menu choice: %r", choice)
            print("Invalid option. Choose one of the displayed menu numbers.")
            continue
        label, handler = MENU[choice]
        try:
            handler()
        except PortfolioTrackerError as error:
            logger.warning("%s rejected: %s", label, error)
            print(f"Cannot complete this action: {error}")
        except DecimalException as error:
            logger.warning("%s rejected because of numeric range: %s", label, error)
            print("Numbers exceed the supported calculation range. Please use smaller values.")
