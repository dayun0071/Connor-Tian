import logging
from .cli import run_cli
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        filename="portfolio_tracker.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        encoding="utf-8",
    )
    logger.info("Application started")
    run_cli()