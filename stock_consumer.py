import pika
import json
import logging
from rabbitmq_config import get_connection, EXCHANGE_NAME, QUEUE_NAME, setup_exchange_and_queue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_stock_update(ch, method, properties, body):
    """Process incoming stock update messages"""
    try:
        message = json.loads(body)
        warehouse_id = message['warehouse_id']
        old_stock = message['old_stock']
        new_stock = message['new_stock']
        timestamp = message['timestamp']
        
        logger.info(f"Stock Update - Warehouse: {warehouse_id}")
        logger.info(f"Old Stock: {old_stock}")
        logger.info(f"New Stock: {new_stock}")
        logger.info(f"Timestamp: {timestamp}")
        logger.info("-" * 50)
        
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        # Reject the message and requeue it
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    """Main function to start consuming messages"""
    try:
        # Ensure queue and exchange exist
        setup_exchange_and_queue()
        
        connection = get_connection()
        channel = connection.channel()
        
        # Set prefetch count to 1 to ensure fair dispatch
        channel.basic_qos(prefetch_count=1)
        
        # Start consuming
        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=process_stock_update
        )
        
        logger.info(" [*] Waiting for stock updates. To exit press CTRL+C")
        channel.start_consuming()
        
    except KeyboardInterrupt:
        logger.info("Stopping consumer...")
    except Exception as e:
        logger.error(f"Error in consumer: {str(e)}")
    finally:
        connection.close()

if __name__ == "__main__":
    main() 