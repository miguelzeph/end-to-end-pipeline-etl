"""
The kafka-print-consumer-articles is represented by the file 
kafka/consumers/consumer_print_articles.py, which aims
to: Consume messages from a Kafka topic named "ARTICLES".
It uses a Kafka consumer configured to connect to two
brokers and belongs to a specific consumer group. The 
script reads messages in JSON format, PRINTS the received
content and adds a 'processed' key indicating that the 
message was processed.
"""

import json
import logging

from confluent_kafka import Consumer

# Setting logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Logs
    ]
)

# Consumer configuration
consumer_conf = {
    'bootstrap.servers': 'kafka-broker-1:9092,kafka-broker-2:9093',  # Include both brokers
    'group.id': 'articles-processor-group',
    'auto.offset.reset': 'earliest'
}

KAFKA_TOPIC= 'ARTICLES'

consumer = Consumer(consumer_conf)
consumer.subscribe([KAFKA_TOPIC])

logging.info("Consumer for {} is waiting for messages...".format(KAFKA_TOPIC))

try:
    while True:
        msg = consumer.poll(5.0)  # Wait for 5 seconds
        if msg is None:
            continue
        if msg.error():
            logging.error(f"Consumer error: {msg.error()}")
            continue

        # Decode the message
        article = json.loads(msg.value().decode('utf-8'))
        logging.info(f"Message received: {article}")

        # Process the message (example: add 'processed' key)
        article['processed'] = True
        logging.info(f"Processed article: {article}")

finally:
    consumer.close()