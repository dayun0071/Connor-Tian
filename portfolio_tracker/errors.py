"""Expected failures that the command-line interface can explain to the user."""


class PortfolioTrackerError(Exception):
    """Base class for all expected application errors."""


class DuplicateAssetError(PortfolioTrackerError):
    pass


class AssetNotFoundError(PortfolioTrackerError):
    pass


class DuplicatePortfolioError(PortfolioTrackerError):
    pass


class PortfolioNotFoundError(PortfolioTrackerError):
    pass


class NoPortfolioSelectedError(PortfolioTrackerError):
    pass


class PortfolioNotEmptyError(PortfolioTrackerError):
    pass


class InvalidTextError(PortfolioTrackerError):
    pass


class InvalidNumberError(PortfolioTrackerError):
    pass


class InvalidPriceError(InvalidNumberError):
    pass


class InvalidQuantityError(InvalidNumberError):
    pass


class InvalidDepositError(InvalidNumberError):
    pass


class InsufficientFundsError(PortfolioTrackerError):
    pass


class InsufficientSharesError(PortfolioTrackerError):
    pass
