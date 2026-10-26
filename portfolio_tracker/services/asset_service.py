import logging
from ..domain.asset import Asset
from ..errors import DuplicateAssetError
logger = logging.getLogger(__name__)
assets = {}
def add_asset(ticker, name):
    ticker = ticker.strip().upper()
    if ticker in assets:
        raise DuplicateAssetError(f"Asset {ticker} already exists")
    asset = Asset(ticker, name)
    assets[ticker] = asset
    logger.info("Added asset: %s", ticker)
    return asset