from pyspark.sql import SparkSession

spark_session = SparkSession.builder \
    .appName("Kafka & Spark Process messages") \
    .master("spark://spark-master:7077") \
    .getOrCreate()
