import pika
import json
import sys
from rabbitmq_config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_EXCHANGE, RABBITMQ_QUEUE, RABBITMQ_ROUTING_KEY
from email_sender import send_email

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        subject = f"Reorder Request for Item ID {data['item_id']}"
        body = f"Placing request for {data['quantity']} units of {data['item_name']} (Item ID: {data['item_id']})."
        send_email(subject, body, data['supplier_email'])
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON message.")
    except KeyError as e:
        print(f"Error: Missing key in message - {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='direct')
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=RABBITMQ_QUEUE, routing_key=RABBITMQ_ROUTING_KEY)

        channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except pika.exceptions.ConnectionClosedByBroker:
        print("Connection closed by broker.")
    except pika.exceptions.AMQPChannelError as e:
        print(f"AMQP Channel Error: {e}")
    except pika.exceptions.AMQPConnectionError:
        print("AMQP Connection Error")
    except KeyboardInterrupt:
        print("Consumer stopped manually.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

if __name__ == '__main__':
    main()
