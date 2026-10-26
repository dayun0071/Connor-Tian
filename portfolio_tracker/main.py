"""Configure file logging once and provide the outermost application boundary."""

import logging

from .cli import run_cli

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        filename="portfolio_tracker.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        encoding="utf-8",
    )
    logger.info("Application started")
    try:
        run_cli()
    except (EOFError, KeyboardInterrupt):
        logger.info("Application closed by end of input or keyboard interruption")
        print("\nGoodbye!")
    except Exception:
        # The only broad catch lives at the outermost boundary and keeps the traceback.
        logger.exception("Unexpected application failure")
        print("An unexpected problem occurred. Details are in portfolio_tracker.log.")
        return 1
    logger.info("Application stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
