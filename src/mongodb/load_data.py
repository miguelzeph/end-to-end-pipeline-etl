from pyspark.sql import SparkSession
from pymongo import MongoClient

def load_data():
    spark = SparkSession.builder.appName("LoadData").getOrCreate()
    df = spark.read.json("/tmp/transformed_data.json")
    client = MongoClient('mongodb://mongodb:27017/')
    db = client['crypto_data']
    collection = db['transformed_data']
    for row in df.collect():
        collection.insert_one(row.asDict())
    spark.stop()
