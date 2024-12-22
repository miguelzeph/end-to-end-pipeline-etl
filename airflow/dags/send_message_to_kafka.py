import json
import random
from datetime import datetime
from confluent_kafka import Producer
from airflow import DAG
from airflow.operators.python import PythonOperator

# Kafka Producer Configuration
producer_conf = {
    'bootstrap.servers': 'kafka-broker-1:9092,kafka-broker-2:9093'  # Kafka brokers
}

# Kafka topic
KAFKA_TOPIC = 'ARTICLES'

# Function to send messages to Kafka
def send_random_message_to_kafka():
    # Create Kafka producer
    producer = Producer(producer_conf)

    # Generate a random message
    article_id = f"article-{random.randint(1, 10)}"
    
    titles = [
        "Kafka Basics", "Advanced Kafka", "Streaming with Kafka",
        "Kafka for Beginners", "Kafka Architecture", "Kafka in Production",
        "Kafka Streams", "Real-Time Data with Kafka", "Kafka Internals", "Kafka Use Cases"
    ]
    
    contents = [
        "Introduction to Kafka", "Deep dive into Kafka", "Kafka use cases",
        "How Kafka handles streams", "Managing Kafka at scale", "Kafka partitioning explained",
        "Kafka vs. traditional messaging systems", "Kafka architecture overview",
        "Why use Kafka?", "Best practices for Kafka producers"
    ]
    
    # Randomly select a title and content
    message = {
        "id": article_id,
        "title": random.choice(titles),
        "content": random.choice(contents),
        "timestamp": datetime.utcnow().isoformat()  # Add a timestamp to the message
    }
    
    # Send the message
    producer.produce(
        KAFKA_TOPIC,
        key=article_id,  # Using `id` as the key
        value=json.dumps(message).encode('utf-8')
    )
    producer.flush()  # Ensure the message is sent

    print(f"Message sent to Kafka: {message}")

# Define the Airflow DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 1),
    'retries': 1
}

with DAG(
    dag_id='kafka_producer_dag',
    default_args=default_args,
    description='DAG to send messages to Kafka',
    schedule_interval=None,  # Triggered manually
    catchup=False
) as dag:
    
    send_kafka_message = PythonOperator(
        task_id='send_kafka_message',
        python_callable=send_random_message_to_kafka
    )

    send_kafka_message
