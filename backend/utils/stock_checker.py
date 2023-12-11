from models.inventory import Inventory
from models.supplier import Supplier
from app import db
from messaging.publisher import publish_low_stock_message

def check_stock_levels():
    # Fetch all items where stock is below the threshold and the low_stock_flag is 'Yes'
    low_stock_items = Inventory.query.filter(Inventory.stock_level < 100, Inventory.low_stock_flag == 'Yes').all()

    for item in low_stock_items:
        supplier = Supplier.query.get(item.supplier_id)
        if supplier:
            # Publish a message to the RabbitMQ queue for each low-stock item
            publish_low_stock_message(item_id=item.item_id, item_name=item.item_name, supplier_email=supplier.contact_info)

def update_low_stock_flags():
    # Fetch all items and update the low_stock_flag as needed
    all_inventory_items = Inventory.query.all()
    for item in all_inventory_items:
        item.low_stock_flag = 'Yes' if item.stock_level < 100 else 'No'
    db.session.commit()

if __name__ == "__main__":
    # First, update the low stock flags based on current inventory levels
    update_low_stock_flags()
    # Then, check the stock levels and send messages for low stock items
    check_stock_levels()
