import pika
import json
from rabbitmq_config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_EXCHANGE, RABBITMQ_QUEUE, RABBITMQ_ROUTING_KEY

def publish_message(item_id, item_name, supplier_email):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='direct')

    message = json.dumps({
        'item_id': item_id,
        'item_name': item_name,
        'supplier_email': supplier_email,
        'quantity': 100  # Assuming a fixed reorder quantity
    })

    channel.basic_publish(exchange=RABBITMQ_EXCHANGE,
                          routing_key=RABBITMQ_ROUTING_KEY,
                          body=message)

    print(f" [x] Sent message for item ID {item_id}")
    connection.close()
