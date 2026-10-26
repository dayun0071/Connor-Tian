# Portfolio Tracker — Command-Line Edition

An in-memory personal investment tracker with named portfolios, one shared cash
balance, manually entered market prices, and average-cost gain calculations.
All assets, quotes, portfolios and transactions disappear when the program exits.

## Setup and run

Use Python 3.13 (the program uses only the standard library). From the repository
root in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m portfolio_tracker.main
```

If PowerShell blocks activation, activation is optional. Run the environment's
interpreter directly instead:

```powershell
.\.venv\Scripts\python.exe -m portfolio_tracker.main
```

On macOS/Linux, create the environment with `python3 -m venv .venv`, activate it
with `source .venv/bin/activate`, then use the same `python -m` entry command.

There are no third-party dependencies. `requirements.txt` intentionally contains
only a comment. The virtual environment, Python caches and `*.log` files are
ignored by Git. Logs are written to `portfolio_tracker.log` in the directory from
which the app is launched.

## Using the menu

1. Add an asset with option 2; view assets with option 1.
2. Create a portfolio with option 4 and select it with option 6. Creating a
   portfolio does not automatically select it.
3. Deposit shared cash with option 9, then buy with option 11 or sell with option 12.
4. Set current market prices with option 3 and view the selected portfolio with
   option 8. Trade prices do not automatically update market quotes.
5. List portfolios with option 5, inspect cash with option 10, or delete an empty
   portfolio with option 7. Option 0 exits. Ctrl+C and end-of-input also exit cleanly.

## Package responsibilities

| Module | Responsibility |
| --- | --- |
| `portfolio_tracker/__init__.py` | Marks the application package. |
| `portfolio_tracker/main.py` | Configures file logging once, starts the CLI, and handles unexpected failures at the outermost boundary. |
| `portfolio_tracker/cli.py` | Displays menus and reports, parses numeric text, calls services, and explains expected errors. |
| `portfolio_tracker/errors.py` | Defines the common application error and specific validation, duplicate, lookup, selection, funds and share errors. |
| `portfolio_tracker/validation.py` | Shared business-value checks for nonempty text, finite decimal numbers and whole-share quantities. |
| `portfolio_tracker/domain/__init__.py` | Marks the domain package. |
| `portfolio_tracker/domain/asset.py` | Defines an asset's ticker and name, without a price. |
| `portfolio_tracker/domain/portfolio.py` | Defines portfolio, position and internal trade-record data. |
| `portfolio_tracker/domain/valuation.py` | Defines read-only position and portfolio report data. |
| `portfolio_tracker/services/__init__.py` | Marks the service package. |
| `portfolio_tracker/services/asset_service.py` | Adds, lists and finds normalized asset definitions. |
| `portfolio_tracker/services/price_service.py` | Keeps current market quotes separate from assets and validates quote changes. |
| `portfolio_tracker/services/portfolio_service.py` | Creates, lists, selects and deletes portfolios; owns the current selection. |
| `portfolio_tracker/services/cash_service.py` | Owns the single shared cash balance and validates deposits and purchase debits. |
| `portfolio_tracker/services/trading_service.py` | Validates buys/sells, computes weighted average cost and realized gains, and updates holdings and cash. |
| `portfolio_tracker/services/valuation_service.py` | Computes position values and portfolio totals, including explicitly incomplete valuations. |

The CLI contains presentation and input parsing, not trading calculations or
business eligibility rules. Services never call `input()` or `print()`. Business
rules can be reused by a future API without calling the CLI. Dictionaries and the
cash balance live in service modules; there is no database or separate storage layer.

## Five design decisions

1. **Whole shares only.** Quantities must be positive finite whole numbers. This
   keeps position quantities straightforward; a fractional quantity is rejected,
   never silently rounded.
2. **Tickers are case-insensitive.** Every asset lookup strips surrounding
   whitespace and uses uppercase, so `aapl`, ` AAPL ` and `AAPL` refer to the same
   asset. This prevents accidental duplicate definitions.
3. **Fully sold positions are hidden.** Selling the last share removes the current
   position, because there is no remaining holding to value. Realized gains and
   internal trade records remain on the portfolio. Buying the same asset again
   starts a fresh average cost. Deleting that empty portfolio discards its gains
   and history and clears selection if needed; cash is unchanged.
4. **Missing quotes are unknown, not zero.** Asset listings say `Not set`; position
   valuation fields say `N/A`. If any holding lacks a quote, the report prominently
   says `Valuation INCOMPLETE` and labels totals as known-price subtotals. Realized
   gains remain available. A quote of zero is valid and fully included in totals.
5. **Expected errors are visible and logged once where handled.** Invalid input
   and broken business rules show a plain-language explanation and a WARNING
   record in the CLI. Successful state-changing operations use INFO in their
   owning service. Unexpected failures are caught only in the entry point, which
   logs the full traceback, displays a friendly message and exits with status 1.
   Technical tracebacks are not shown to users. Normal exit and interrupted input
   use INFO; ordinary report viewing does not create extra log noise.

Portfolio names also ignore surrounding spaces and case for matching, while
preserving the display spelling. Names, tickers and strategy descriptions cannot
be blank. All portfolios share one cash balance but have independent positions.

## Calculation rules

- Buy average cost: `(old quantity * old average cost + bought quantity * buy price)
  / (old quantity + bought quantity)`.
- A sell changes the quantity but does not change the remaining average cost.
- Realized gain on a sale: `(sale price - average cost) * sold quantity`.
- Unrealized gain: `(current price - average cost) * quantity held`.
- Market value: `current price * quantity held`.
- Buy prices and deposits must be positive. Quotes and sale prices may be zero.
  Quantity cannot exceed the selected portfolio's holding on a sale, and a buy
  cannot exceed shared cash.

Prices and cash use `Decimal` created from text with Python's default 28-significant-
digit arithmetic. Display formatting normally uses two decimal places; it does
not round stored values. Very large/small displays use scientific notation.
NaN and infinity are rejected. Numeric operations outside Decimal's supported
range produce a friendly rejection. Validation and trading arithmetic are performed
before committing a trade so rejected operations do not partially update holdings.

## Manual verification walkthrough

No automated test suite is included in this milestone. Start a fresh process:

1. Add `AAPL` / `Apple`, create/select `Growth`, and deposit `1000`.
2. Buy 10 shares at 20, then 5 at 26. Expect 15 shares, average cost 22, cash 670.
3. Sell 4 at 25. Expect 11 shares, average cost still 22, realized gain 12, cash 770.
4. Set current price to 30. Expect market value 330 and unrealized gain 88.
5. Try deleting Growth: it must be refused while shares remain.
6. Sell the remaining 11 at zero. Expect no holdings, realized gain/loss -230,
   and cash still 770. Deleting Growth now succeeds and clears selection.

Also check invalid menu text, text in numeric prompts, blank names, duplicate
tickers/portfolio names, unknown tickers, negative/NaN/infinite prices, fractional
quantities, zero deposits, insufficient cash/shares, and trading with no selection.
Hold the same ticker in two portfolios at different costs to verify independence.
View a holding without a market quote, then set its quote to zero to see the
difference. Repeat rejected operations and confirm cash/holdings do not change.