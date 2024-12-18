from confluent_kafka import Consumer
import json

# Consumer configuration
consumer_conf = {
    'bootstrap.servers': 'kafka:9092,kafka-broker-2:9093',  # Include both brokers
    'group.id': 'articles-processor-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe(['ARTICLES'])

print("Consumer for ARTICLES is waiting for messages...")

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

        # Process the message (example: add 'processed' key)
        article['processed'] = True
        print(f"Processed article: {article}")

finally:
    consumer.close()