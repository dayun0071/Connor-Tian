"""Asset definitions and normalized lookups; prices live in price_service."""

import logging

from ..domain.asset import Asset
from ..errors import AssetNotFoundError, DuplicateAssetError
from ..validation import normalize_ticker, require_text

logger = logging.getLogger(__name__)
assets = {}


def add_asset(ticker, name):
    ticker = normalize_ticker(ticker)
    name = require_text(name, "Asset name")
    if ticker in assets:
        raise DuplicateAssetError(f"Asset {ticker} already exists.")
    asset = Asset(ticker, name)
    assets[ticker] = asset
    logger.info("Added asset: %s", ticker)
    return asset


def list_assets():
    return list(assets.values())


def get_asset(ticker):
    ticker = normalize_ticker(ticker)
    try:
        return assets[ticker]
    except KeyError as error:
        raise AssetNotFoundError(f"No asset with ticker {ticker}.") from error
