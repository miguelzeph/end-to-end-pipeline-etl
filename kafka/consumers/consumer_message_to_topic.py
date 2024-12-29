"""
The kafka-consumer-message-to-topic is represented by 
the file kafka/consumers/consumer_message_to_topic.py,
which aims to: Consume messages from the Kafka topic "ARTICLES",
process them (using Pyspark) and forward them to another topic called
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
# Kafka
from confluent_kafka import Consumer, Producer
# PySpark
from spark.connect_spark_master import spark_session
from pyspark.sql.functions import col, from_json, lit, struct, to_json
from pyspark.sql.types import StructType, StringType

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

logging.info("Consumer for {} is waiting for messages to send to the {} topic...".format(KAFKA_TOPIC,KAFKA_TOPIC_PROCESSED))


"""
# Expected message format

{
    "id":"article-1",
    "title":"Kafka Basics",
    "content":"Introduction to Kafka"
}
"""

schema = StructType() \
    .add("id", StringType()) \
    .add("title", StringType()) \
    .add("content", StringType()) \
    .add("processed", StringType())


try:
    while True:
        msg = consumer.poll(5.0)  # Wait for 5 seconds
        if msg is None:
            continue
        if msg.error():
            logging.error(f"Consumer error: {msg.error()}")
            continue

        # Decode the message
        # article = json.loads(msg.value().decode('utf-8'))
        # print(f"Message received: {article}")
        
        raw_messages = msg.value().decode('utf-8')

                
        # transform the message into pyspark dataframe
        df = spark_session.read.json(
            spark_session.sparkContext.parallelize(
                [raw_messages]
            ),
            schema
        )

        # Adding processed column
        df_processed = df.withColumn("processed", lit(True))

        # Show 
        df_processed.show(truncate=False)

        # Convert to Dict
        processed_messages = [row.asDict() for row in df_processed.collect()]


        for processed_message in processed_messages:
            logging.info(processed_message)

            # Send to the ARTICLES_PROCESSED topic
            producer.produce(
                KAFKA_TOPIC_PROCESSED,
                key=str(processed_message.get("id")),  # Using 'id' as the key
                value=json.dumps(processed_message).encode('utf-8')
            )
            producer.flush()
            logging.info(f"Message sent to {KAFKA_TOPIC_PROCESSED}: {processed_message}")

finally:
    consumer.close()
    spark_session.close()