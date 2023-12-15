## DCSC - Project Report - Fall 2023

### Title: (Restaurant) Inventory Management System

#### Participants: Paresha Farastu

#### Project Goals:

The main aim is to develop an Efficient Inventory Management System suitable for businesses like restaurants, retail stores, warehouses, and e-commerce platforms. The key objectives are:

a. Real-Time Inventory Tracking: To maintain accurate and real-time records of stock levels, avoiding overstocking or stockouts.

b. Automated Reordering and Email Updates to Supplier: Implement an automated system for replenishing inventory, reducing manual intervention. Supplier will be sent an email to place a reorder. Some suppliers can be marked if their performance has been subpar, and manual intervention will be needed before sending the reorder request. 

#### Software Components:

Servers:
Utilize REST servers for handling inventory updates, stock level queries, and automated reorder requests.
Order Creation - REST Apis
Inventory Status Updates - REST Apis
Stock Checker - Workers
Reorder Requests - Workers

Frontend: 
Developed using Python Flask, and HTML.

Order creation, inventory status updates, stock level queries, and reorder requests - Python Flask and HTML templates

#### Database:
The application is configured to use SQLite as the database. Used for storing structured data such as inventory details, order details, supplier information. 

Inventory data: contains data about the different items, their costs, their stock level, item id, supplier id, supplier contact info, a flag column to identify if stock levels are low
Orders: contains order and product details
Supplier data: contains the supplier information
Inventory Table
+---------+-----------+------+-------------+------------+---------------+
| ItemID  | ItemName  | Cost | StockLevel  | SupplierID | LowStockFlag  |
+---------+-----------+------+-------------+------------+---------------+

Order Table
+----------+------------+--------+----------+------------+
| OrderID  | SupplierID | ItemID | Quantity | Date       |
+----------+------------+--------+----------+------------+

Supplier Table
+------------+---------------+--------------+--------+
| SupplierID | SupplierName  | ContactInfo  | Rating |
+------------+---------------+--------------+--------+

Relationships:
- Inventory.SupplierID -> Supplier.SupplierID
- Order.SupplierID -> Supplier.SupplierID
- Order.ItemID -> Inventory.ItemID

#### Message Queues: 
Integrate RabbitMQ for handling asynchronous tasks such as sending reorder requests and updating stock levels.

Email Reorder Requests: supplier will receive notification about order via email
Worker jobs: takes jobs from server using Rabbitmq

#### Interaction Between Components:


Backend and Frontend Communication: The backend uses REST APIs to provide inventory data to the frontend. The frontend, in turn, allows users to perform inventory-related actions (create order/inventory, edit inventory, delete inventory) which are processed by the backend. The frontend client makes RESTful calls to the backend server with an appropriate method to fetch and render a response. The backend server uses workers to send email reorder requests to the supplier. It uses RabbitMQ to publish messages to workers, each of which is created to generate emails, persists them in the database, fetch supplier details to place a reorder request.

Workers:

 email_sender.py
This script contains the functionality to send emails. It defines a send_email function that takes in recipient details, a subject, and a body to send an email. This function can be used by other parts of the system to send notifications to suppliers.

stock_checker.py
This module contains logic to check the inventory for items that have low stock. It interacts with the database to find items where the stock level is below a certain threshold (e.g., 100) and the low_stock_flag is 'Yes'. When such items are found, it calls the send_email function defined in email_sender.py to notify the relevant supplier that a reorder is needed.

reorder_worker.py
This script acts as a background process or worker that periodically triggers the stock checking process. It runs continuously, invoking the stock_checker.py functions at regular intervals to ensure that the inventory is checked and suppliers are notified i

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


#### Database Interactions: 
The backend regularly interacts with MySQL databases for retrieving and updating inventory data. A worker fetches and persists to the MySQL database the data related to the reorder.


#### Asynchronous Task Handling: 
Utilize RabbitMQ for queuing tasks like reorder requests and stock level updates, ensuring efficient background processing. A worker subscribes to the RabbitMQ queue where the server produces data whenever the reorder changes state.The RabbitMQ queue pushes data into the queue for the email client to send out an email as a notification to the supplier whenever this change in status occurs.

#### Debugging and Testing:

Logging and Monitoring: Implement basic logging approach of logging exceptions, error and important events for tracking system behavior and identifying issues.

Exception Handling: Utilize try-catch blocks extensively to manage and resolve exceptions effectively on the frontend to prevent accidental and unhandled exceptions occuring due to null pointers or any other issues.

#### Workflow:

Order Placement:
The flow starts when a restaurant/platform places an order through the system’s frontend interface
Inventory Check and Reorder Scheduling:
The server checks the current stock levels against the order and schedule tasks to handle inventory updates

If any item’s stock level is low, an automated task is scheduled for reordering. This involves a check for suppliers marked as subpar (requires manual intervention).

Automated reorder and supplier notification:
Through a worker job, the server processes reorder requests. The reorder details(quantity, item, supplier information) are sent to the RabbitMQ queue. If the supplier is not marked as subpar, an automated email notification is sent to the supplier to place the reorder.

Stock Level updates and Database interaction:”
As orders are processed, the system updates the stock levels in the database. The database then maintains a record of all the transactions, stock levels, product and supplier details. 

 
#### Further Work:
 
Authentication and Authorization: There is no apparent implementation of authentication and authorization. Implementing user authentication and authorization would be crucial for a product

Unit and Integration Testing:. Implementing a suite of unit and integration tests would help ensure the reliability and robustness of the application.

Scalability: To scale this project a more robust database needs to be implemented

Deployment: The server will need to be containerized and hosted on Kubernetes – we can create multiple pods to ensure maximum availability
