
# Data Streaming ETL Pipeline Project

## Project Overview

This project is a data streaming ETL (Extract, Transform, Load) pipeline that collects real-time data from an external API, processes it using Apache Kafka and Apache Spark, and finally stores it in MongoDB. Apache Airflow orchestrates the entire pipeline.

### Architecture

1. **Airflow**: Orchestrates the ETL pipeline, triggering each task in sequence.
2. **Kafka**: Acts as the message broker for streaming data between components.
3. **Spark**: Processes and transforms data streamed from Kafka.
4. **MongoDB**: Stores the processed data for future querying and analysis.
5. **PostgreSQL**: Stores metadata for Airflow.
6. **Docker Compose**: Manages all the services and containers.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- **Docker** and **Docker Compose**
- **Python 3.8** (if you need to install additional dependencies)

---

## Project Structure

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

### 3. Start Docker Containers

Use Docker Compose to start all the services (PostgreSQL, Zookeeper, Kafka, Airflow, Spark, and MongoDB).

```bash
docker-compose up
```

This command will:

- Initialize PostgreSQL for Airflow’s metadata storage.
- Start Kafka and Zookeeper for data streaming.
- Run Airflow’s web server at `http://localhost:8080`.
- Start Spark for data processing.
- Start MongoDB for storing transformed data.

### 4. Configure and Run the Airflow Pipeline

1. Access the Airflow web interface at [http://localhost:8080](http://localhost:8080).
2. Look for the DAG named **`etl_pipeline`**.
3. Activate the DAG by toggling the "Off" switch to "On".
4. Run the DAG manually or wait for it to execute automatically according to its schedule.

### 5. Verify the Data Flow

#### Kafka

To ensure data is streaming correctly into Kafka, you can monitor the `raw_data` topic:

```bash
docker exec -it <kafka_container_name> kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic raw_data --from-beginning
```

#### MongoDB

After the DAG completes its tasks, check MongoDB to ensure the data has been loaded correctly.

```bash
docker exec -it <mongodb_container_name> mongo
use crypto_data
db.transformed_data.find().pretty()
```

---

## Testing the Components

### Individual Component Tests

You can test each part of the pipeline independently:

1. **Extract and Kafka**: Run `fetch_data.py` to fetch data from the API and send it to Kafka.

   ```bash
   python src/api/fetch_data.py
   ```

2. **Spark Transformation**: Run `transform_data.py` to ensure data transformation works as expected.

   ```bash
   python src/spark/transform_data.py
   ```

3. **MongoDB Loading**: Run `load_data.py` to load transformed data into MongoDB.

   ```bash
   python src/mongodb/load_data.py
   ```

### Full Integration Test

Activate the DAG `etl_pipeline` in Airflow and verify that each task runs successfully and that data flows through Kafka, Spark, and into MongoDB.

---

## Troubleshooting

1. **Airflow Errors**: Check task logs in the Airflow web interface for more details.
2. **Kafka Issues**: Ensure Kafka and Zookeeper containers are running. Restart them if necessary.
3. **Spark Errors**: Check Spark logs and ensure the Kafka integration is configured correctly.
4. **MongoDB Connectivity**: Verify MongoDB connection strings and check if the MongoDB container is running.

---

## Access Points

- **Airflow**: [http://localhost:8080](http://localhost:8080)
- **MongoDB**: Access MongoDB at `localhost:27017` or through a MongoDB client.

---

## Future Improvements

1. **Scalability**: Add multiple Kafka partitions and Spark executors to handle larger data volumes.
2. **Monitoring**: Set up monitoring and alerts in Airflow for proactive management.
3. **Data Quality**: Implement data validation steps before loading into MongoDB.

---

## Conclusion

This project demonstrates an end-to-end data streaming ETL pipeline. The modular setup allows for scalability, and Docker simplifies the deployment of each component. Use Airflow to monitor and manage the pipeline as data flows from the API through Kafka, Spark, and finally into MongoDB.