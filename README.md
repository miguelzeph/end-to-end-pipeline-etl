
# Data Streaming ETL Pipeline Project

## Project Overview

This project is an simple example of data streaming ETL (Extract, Transform, Load) pipeline that collects real-time data from an external API, processes it using `Apache Kafka` and `Apache Spark`, and finally stores it in `MongoDB`. `Apache Airflow` was used to orchestrate the entire pipeline.

### Architecture

1. **Airflow**: **Orchestrates the ETL pipeline**, triggering each task in sequence.
2. **Kafka**: Acts as the **message broker** for streaming data between components.
3. **Spark**: **Processes and transforms** data streamed from Kafka.
4. **MongoDB**: **Stores the processed data** for future querying and analysis.
5. **PostgreSQL**: **Stores metadata** for Airflow.
6. **Docker Compose**: **Manages all microservices** and containers.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- **Docker** and **Docker Compose**
- **Python 3.8** (if you need to install additional dependencies)

---

## Project Structure


ATUALIZAR A ESTRUTURA DO PROJETO DEPOIS!!!!

```
data-streaming-project/
│
├── docker/                           # Docker configuration files
│   ├── docker-compose.yml            # Docker Compose file to orchestrate all services
│   ├── Dockerfile_airflow             # Dockerfile for customizing Airflow
│   └── Dockerfile_spark               # Dockerfile for customizing Spark
│
├── requirements.txt                  # Python dependencies for the project
│
├── src/                              # Main source code
│   ├── api/                          # API data collection
│   │   └── fetch_data.py             # Script to fetch data from API and send to Kafka
│   │
│   ├── airflow/                      # Apache Airflow DAGs
│   │   └── dags/
│   │       └── etl_dag.py            # Main DAG for ETL pipeline
│   │
│   ├── kafka/                        # Kafka producer script
│   │   └── producer.py               # Kafka producer module
│   │
│   ├── spark/                        # Spark data transformation scripts
│   │   └── transform_data.py         # Script to transform data in Spark
│   │
│   └── mongodb/                      # MongoDB loading script
│       └── load_data.py              # Script to load data into MongoDB
│
└── README.md                         # Documentation for the project
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/data-streaming-project.git
cd data-streaming-project
```

### 2. Add Required Python Dependencies

Ensure that the following dependencies are listed in `requirements.txt`:

```text
kafka-python
pymongo
pyspark
psycopg2
apache-airflow
```

### 3. Start Docker Containers - Step by Step

---

1. Starting `Airflow`:

- Execute the command below to start the follows microservices:

```bash
sudo docker-compose up postgres airflow-init airflow-scheduler airflow-webserver
```

- Check the Airflow Interface: **localhost:8080**


**P.S. Don't try to execute any DAGs yet, because the pipeline is integrated with Kafka and Spark, so firtly let's go to the next step and put to run `Kafka`.**

---

2. Starting `Kafka`: 

P.S. Before start the CONSUMER, always start the BROKER/ZOOKEEPER first and create the TOPICS related to the CONSUMER (SAME NAME). Only after that then you can start the CONSUMER. If you don't do it, you will get error of conection.

- Starting Kafka `ZOOKEEPER/BROKERS/UI`

```bash
docker-compose up zookeeper kafka-broker-1 kafka-broker-2 kafka-ui

# P.S if you want to restart from scratch, use --build
docker-compose up --build zookeeper kafka-broker-1 kafka-broker-2 kafka-ui
```

- Go to **localhost:8001** and create the topics (Make sure the topic's name are correct and UPPERCASE):
      - `ARTICLES`
      - `ARTICLES_PROCESSED`

- Now run the CONSUMERS:

```bash
 sudo docker-compose up --build kafka-consumer-print-articles kafka-consumer-message-to-topic
```

- Explanation of two consumers used as example:

The `kafka-print-consumer-articles` is represented by the file kafka/consumers/`consumer_print_articles.py`, which aims to: Consume messages from a Kafka topic named "ARTICLES". It uses a Kafka consumer configured to connect to two brokers and belongs to a specific consumer group. The script reads messages in JSON format, PRINTS the received content and adds a 'processed' key indicating that the message was processed.

The kafka-consumer-message-to-topic is represented by the file kafka/consumers/`consumer_message_to_topic.py`, which aims to: Consume messages from the Kafka topic "ARTICLES", process them and forward them to another topic called "ARTICLES_PROCESSED". It uses a CONSUMER to receive messages in JSON format and a PRODUCER to send a processed version of the messages, adding the key "processed": True. Each message sent to the new topic uses the id field as a key. The consumer and producer are configured to connect to the same Kafka brokers, ensuring that the messages are processed and forwarded correctly.

- Sending message to the TOPIC ARTICLES (from Kafka-UI) 
      - Go to `Topics`
      - click in `ARTICLES` (after created the Topic)
      - click in `Produce Message`
      - right a JSON object: {"id":"article-1","title":"Kafka Basics","content":"Introduction to Kafka"}
      - send message

**IMPORTANT** - The only requirement to send messages is that you create the **"id"** field because our python script needs this field to process the key, in the other fields, you can write whatever you want.


- Sending message to the TOPIC ARTICLES (from Airflow pipeline )
      - Go to airflow interface (**localhost:8080**)
      - Click in **DAGS**
      - Toogle on the pipeline you cant to run, example **kafka_producer_dag**
      - Click in **Trigger DAG** (Now your pipeline will run it)

So, once we have **Kafka** and **Airflow** running you can send messages to the Kafka BROKER using AIRFLOW's pipeline, which the script connect to the Kafka PRODUCER and you send the message as many as you want.

---

To stop all containers and keeping all resources (networks, volumes, etc.)
```bash
sudo docker-compose stop
```

If you want to removes the created containers and networks, completely shutting down the environment.

```bash
sudo docker-compose down --volumes
```

