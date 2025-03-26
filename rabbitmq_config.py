import pika
import json
import logging
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RabbitMQ connection parameters
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASSWORD = 'guest'

# Exchange and queue names
EXCHANGE_NAME = 'warehouse_exchange'
QUEUE_NAME = 'stock_updates'

def get_connection():
    """Create and return a RabbitMQ connection"""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )
    return pika.BlockingConnection(parameters)

def setup_exchange_and_queue():
    """Setup the exchange and queue for stock updates"""
    try:
        connection = get_connection()
        channel = connection.channel()
        
        # Declare exchange
        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type='direct',
            durable=True
        )
        
        # Declare queue
        channel.queue_declare(
            queue=QUEUE_NAME,
            durable=True
        )
        
        # Bind queue to exchange
        channel.queue_bind(
            exchange=EXCHANGE_NAME,
            queue=QUEUE_NAME,
            routing_key=QUEUE_NAME
        )
        
        logger.info("Successfully set up RabbitMQ exchange and queue")
        connection.close()
        
    except Exception as e:
        logger.error(f"Error setting up RabbitMQ: {str(e)}")
        raise

def publish_stock_update(warehouse_id, old_stock, new_stock):
    """Publish stock update message to RabbitMQ"""
    try:
        connection = get_connection()
        channel = connection.channel()
        
        message = {
            'warehouse_id': warehouse_id,
            'old_stock': old_stock,
            'new_stock': new_stock,
            'timestamp': str(datetime.datetime.now())
        }
        
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=QUEUE_NAME,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
                content_type='application/json'
            )
        )
        
        logger.info(f"Published stock update for warehouse {warehouse_id}")
        connection.close()
        
    except Exception as e:
        logger.error(f"Error publishing message: {str(e)}")
        raise 