import logging
logger = logging.getLogger(__name__)
def show_welcome():
    print("welcome portfolio tracker")

def show_menu():
    print("please take a choose: ")
    print("1. check assets")
    print("0. quit")

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
            print("Asset viewing is not implemented yet")
        else:
            logger.warning("Invalid menu choice: %r", choice)
            print("Invalid option. Please choose 0 or 1")