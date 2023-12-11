# Inventory-Management-System


### utils & workers:
 The three Python files (email_sender.py, reorder_worker.py, and stock_checker.py) are part of a backend system that works together to monitor inventory levels and automate the process of reordering items when stock levels are low.

 email_sender.py
This script contains the functionality to send emails. It defines a send_email function that takes in recipient details, a subject, and a body to send an email. This function can be used by other parts of the system to send notifications to suppliers.

stock_checker.py
This module contains logic to check the inventory for items that have low stock. It interacts with the database to find items where the stock level is below a certain threshold (e.g., 100) and the low_stock_flag is 'Yes'. When such items are found, it calls the send_email function defined in email_sender.py to notify the relevant supplier that a reorder is needed.

reorder_worker.py
This script acts as a background process or worker that periodically triggers the stock checking process. It runs continuously, invoking the stock_checker.py functions at regular intervals to ensure that the inventory is checked and suppliers are notified in real-time or at the scheduled times.

How They Work Together:
Initial Setup: The inventory and supplier details are set up in the database with the correct stock levels and flags.

Stock Checking:

The stock_checker.py script runs either on a schedule or is triggered by the reorder_worker.py.
It checks the current stock levels against the set threshold and identifies items that need reordering. This script will check for low-stock items in the inventory and then use the RabbitMQ publisher to send messages for those items.
Notification:

For each item that requires reordering, stock_checker.py uses the send_email function from email_sender.py to send out an email to the respective supplier.
The email includes details about the item and the quantity required for reorder.
Background Processing:

The reorder_worker.py script is responsible for invoking the stock checking process at regular intervals.
It ensures that the inventory is monitored continuously or as per the defined schedule, without manual intervention.

Use publisher.py in the stock checking logic. Whenever a low-stock item is identified, publish_message() is called with the appropriate item details.
consumer.py is run as a separate, long-running process. It will continuously listen for messages on the RabbitMQ queue and trigger email notifications.
