
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
- **Python 3.11** (if you need to install additional dependencies)

---

## Project Structure

```
data-streaming-project
├── airflow                       # Main directory for Airflow, used for orchestrating pipelines
│   ├── dags                      # Directory containing the DAGs (workflow definitions)
│   │   └── send_message_to_kafka.py  # Python script defining the DAG to send messages to Kafka
│   ├── Dockerfile_python          # Dockerfile to create the Airflow image with Python setup
│   ├── plugins                    # Directory for custom Airflow plugins
│   └── requirements.txt           # File containing Python dependencies for Airflow
├── docker-compose.yml             # Docker Compose file to orchestrate the application containers
├── kafka                          # Directory for Apache Kafka-related files
│   ├── consumers                  # Directory containing Kafka message consumers
│   │   ├── consumer_message_to_topic.py  # Consumer to process messages from a specific topic
│   │   ├── consumer_print_articles.py    # Consumer to print articles received from Kafka
│   │   └── spark                  # Subdirectory related to Kafka integration with Apache Spark
│   │       └── connect_spark_master.py  # Script to connect Kafka to the Spark master
│   ├── Dockerfile_python          # Dockerfile to configure the Kafka environment with Python
│   └── requirements.txt           # Python dependencies required for Kafka integration
└── README.md                      # Documentation file explaining the project

```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/data-streaming-project.git
cd data-streaming-project
```

### 2. Start Docker Containers - Step by Step

---

1. Starting `AIRFLOW`:

- Execute the command below to start the follows microservices:

```bash
sudo docker-compose up postgres airflow-init airflow-scheduler airflow-webserver
```

- Check the Airflow Interface: **localhost:8080**


**P.S. Don't try to execute any DAGs yet, because the pipeline is integrated with Kafka and Spark, so firtly let's go to the next step and put to run `Kafka` and `Spark`.**

---

2. Starting `KAFKA` and `SPARK`: 

P.S. Before start the Kafka **CONSUMER**, always start the **BROKER/ZOOKEEPER** first and create the **TOPICS** related to the **CONSUMER*** (use the exactly same name in the python script). Only after that then you can start the **CONSUMER**. If you don't do it, you will get error of conection and your container won't work properly.

- `ZOOKEEPER/BROKERS/UI` containers:

```bash
sudo docker-compose up zookeeper kafka-broker-1 kafka-broker-2 kafka-ui spark-master spark-worker-1 spark-worker-2

# P.S if you want to restart from scratch, use --build
sudo docker-compose up --build zookeeper kafka-broker-1 kafka-broker-2 kafka-ui spark-master spark-worker-1 spark-worker-2
```

- Testing UI: Go to **localhost:8001** and create the `TOPICS` (Make sure the topic's name are correct and UPPERCASE):
      - `ARTICLES`
      - `ARTICLES_PROCESSED`

- Now run the Kafka `CONSUMERS`:

```bash
 sudo docker-compose up --build kafka-consumer-print-articles kafka-consumer-message-to-topic
```

- Explanation of two CONSUMERS used as example:

The `kafka-print-consumer-articles` is represented by the file kafka/consumers/`consumer_print_articles.py`, which aims to: Consume messages from a Kafka topic named "ARTICLES". It uses a Kafka consumer configured to connect to two brokers and belongs to a specific consumer group. The script reads messages in JSON format, PRINTS the received content and adds a 'processed' key indicating that the message was processed.

The kafka-consumer-message-to-topic is represented by the file kafka/consumers/`consumer_message_to_topic.py`, which aims to: Consume messages from the Kafka topic "ARTICLES", process them and forward them to another topic called "ARTICLES_PROCESSED". It uses a CONSUMER to receive messages in JSON format and a PRODUCER to send a processed version of the messages, adding the key "processed": True. Each message sent to the new topic uses the id field as a key. The consumer and producer are configured to connect to the same Kafka brokers, ensuring that the messages are processed and forwarded correctly.

- Sending message to the TOPIC ARTICLES (from `Kafka-UI`) 
      - Go to `Topics`
      - click in `ARTICLES` (after created the Topic)
      - click in `Produce Message`
      - right a JSON object: `{"id":"article-1","title":"Kafka Basics","content":"Introduction to Kafka"}`
      - send message

**IMPORTANT MESSAGE FORMAT** - The requirement to send messages is that you create the **"id"**, **"title"** and **"content"** fields because python script (Kafka & Spark) needs this field to process the key.

```json 
{
      "id":"....",
      "title":"....",
      "content":"...."
}
```

- Sending message to the TOPIC ARTICLES (from `Airflow pipeline` )
      - Go to airflow interface (**localhost:8080**)
      - Click in **DAGS**
      - Toogle on the pipeline you cant to run, example **kafka_producer_dag**
      - Click in **Trigger DAG** (Now your pipeline will run it)

So, once we have **Kafka** and **Airflow** running you can send messages to the Kafka BROKER using AIRFLOW's pipeline, which the script connect to the Kafka PRODUCER and you send the message as many as you want.

3. Verify the documents processed on MONGODB-UI (mongo-express):

Acessing the mongo-ui: 

- Go to **localhost:8087** 
- Check the Database/Collection


---

### 3. Useful Docker Commands

To start all containers as defined in the docker-compose.yml file:

```bash
sudo docker-compose up
```

To start the containers and force a rebuild of the images, even if they already exist:

```bash
sudo docker-compose up --build
```

To stop all containers and keeping all resources (networks, volumes, etc.)
```bash
sudo docker-compose stop
```

If you want to removes the created containers and networks, completely shutting down the environment.

```bash
sudo docker-compose down --volumes
```
