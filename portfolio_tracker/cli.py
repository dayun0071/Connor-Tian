import logging
from .services.asset_service import add_asset, list_assets
from .errors import DuplicateAssetError
logger = logging.getLogger(__name__)
def show_welcome():
    print("welcome portfolio tracker")

def show_menu():
    print("please take a choose: ")
    print("1. Check assets")
    print("2. Add asset")
    print("0. Quit")

def handle_add_asset():
    ticker = input("Enter ticker: ")
    name = input("Enter asset name: ")
    try:
        asset = add_asset(ticker, name)
    except DuplicateAssetError as error:
        logger.warning("Asset addition rejected: %s", error)
        print(error)
    else:
        print(f"Asset {asset.ticker} added successfully.")

def handle_view_assets():
    asset_list = list_assets()
    if not asset_list:
        print("No assets yet")
        return
    for asset in asset_list:
        print(f"{asset.ticker} | {asset.name} | Price: not set")


def run_cli():
    show_welcome()
    while True:
        show_menu()
        choice = input("Enter your choice: ")
        if choice == "0":
            print("Goodbye")
            logger.info("User selected quit")
            break
        elif choice == "1":
            handle_view_assets()
        elif choice == "2":
            handle_add_asset()
        else:
            logger.warning("Invalid menu choice: %r", choice)
            print("Invalid option. Please choose 0, 1 or 2")