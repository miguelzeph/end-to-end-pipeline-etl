from confluent_kafka import Consumer, Producer
import json

# Consumer configuration
consumer_conf = {
    'bootstrap.servers': 'kafka:9092,kafka-broker-2:9093',  # Include both brokers
    'group.id': 'send-msg-topic-group',
    'auto.offset.reset': 'earliest'
}

# Producer configuration
producer_conf = {
    'bootstrap.servers': 'kafka:9092,kafka-broker-2:9093'  # Use the container names
}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

consumer.subscribe(['ARTICLES'])

print("Consumer for ARTICLES is waiting for messages to send to the ARTICLES_PROCESSED topic...")


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
            'ARTICLES_PROCESSED',
            key=str(article.get("id")),  # Using 'id' as the key
            value=json.dumps(processed_message).encode('utf-8')
        )
        producer.flush()
        print(f"Message sent to ARTICLES_PROCESSED: {processed_message}")

finally:
    consumer.close()