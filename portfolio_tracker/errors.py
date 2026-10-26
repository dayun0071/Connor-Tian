class PortfolioTrackerError(Exception):
    pass



class DuplicateAssetError(PortfolioTrackerError):
    pass



class AssetNotFoundError(PortfolioTrackerError):
    pass
