"""
The kafka-consumer-message-to-topic is represented by 
the file kafka/consumers/consumer_message_to_topic.py,
which aims to: Consume messages from the Kafka topic "ARTICLES",
process them and forward them to another topic called
"ARTICLES_PROCESSED". It uses a CONSUMER to receive 
messages in JSON format and a PRODUCER to send a processed
version of the messages, adding the key "processed": True. 
Each message sent to the new topic uses the id field as a key.
The consumer and producer are configured to connect to the
same Kafka brokers, ensuring that the messages are processed
and forwarded correctly.
"""

import json
import logging

from confluent_kafka import Consumer, Producer

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
    'group.id': 'send-msg-topic-group',
    'auto.offset.reset': 'earliest'
}

# Producer configuration (Acessing Producer to send message)
producer_conf = {
    'bootstrap.servers': 'kafka-broker-1:9092,kafka-broker-2:9093'  # Use the container names
}

KAFKA_TOPIC = 'ARTICLES'
KAFKA_TOPIC_PROCESSED = 'ARTICLES_PROCESSED'


consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

consumer.subscribe([KAFKA_TOPIC])

print("Consumer for {} is waiting for messages to send to the {} topic...".format(KAFKA_TOPIC,KAFKA_TOPIC_PROCESSED))


# Expected message format
# {"id":123, "title":"Coding Just War Theory: Artificial Intelligence in Warfare"}

try:
    while True:
        msg = consumer.poll(5.0)  # Wait for 5 seconds
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Decode the message
        article = json.loads(msg.value().decode('utf-8'))
        print(f"Message received: {article}")

        # Process the message (example: send it to the ARTICLES_PROCESSED topic)
        processed_message = {
            "id": article.get("id"),
            "title": article.get("title"),
            "processed": True
        }

        # Send to the ARTICLES_PROCESSED topic
        producer.produce(
            KAFKA_TOPIC_PROCESSED,
            key=str(article.get("id")),  # Using 'id' as the key
            value=json.dumps(processed_message).encode('utf-8')
        )
        producer.flush()
        print(f"Message sent to {KAFKA_TOPIC_PROCESSED}: {processed_message}")

finally:
    consumer.close()