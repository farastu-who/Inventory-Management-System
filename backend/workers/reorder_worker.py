import time
from stock_checker import check_stock_levels_and_notify, update_low_stock_flags

def reorder_task():
    while True:
        # Update flags before sending notifications
        update_low_stock_flags()
        # Check stock levels and notify if necessary
        check_stock_levels_and_notify()
        # Wait for the specified interval (e.g., 1 hour)
        time.sleep(3600)

if __name__ == "__main__":
    reorder_task()
