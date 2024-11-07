from pyspark.sql import SparkSession

def transform_data():
    spark = SparkSession.builder.appName("TransformData").getOrCreate()
    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "raw_data")
        .load()
    )
    transformed_df = df.selectExpr("CAST(value AS STRING)")
    transformed_df.write.mode("overwrite").json("/tmp/transformed_data.json")
    spark.stop()
