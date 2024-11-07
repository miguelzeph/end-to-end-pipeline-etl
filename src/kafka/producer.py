from kafka import KafkaProducer
import json

from src.api.fetch_data import get_data

def send_to_kafka(topic, data, kafka_server='kafka:9092'):
    """
    Envia dados ao Kafka no tópico especificado.

    Parâmetros:
    - topic (str): Nome do tópico Kafka.
    - data (dict): Dados a serem enviados ao Kafka.
    - kafka_server (str): Endereço do servidor Kafka.
    """
    producer = KafkaProducer(
        bootstrap_servers=kafka_server,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    producer.send(topic, value=data)
    producer.close()
    


def extract_data():
    """
    Extrai dados da API externa e os envia para o Kafka.
    """
    data = get_data()
    
    # Envia os dados para o Kafka usando o produtor
    send_to_kafka(topic='raw_data', data=data)