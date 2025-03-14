#Assumtion codeing
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import pymongo
import json
import pandas as pd
import pyarrow.parquet as pq
from google.cloud import storage, bigquery
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# MongoDB Connection
MONGO_URI = "mongodb://your_mongo_uri_path"
MONGO_DB = "your_database"
MONGO_COLLECTION = "your_collection"

# GCP Bucket & BigQuery Config
GCS_BUCKET = "your-bucket-name_path"
GCS_PARQUET_PATH = f"gs://{GCS_BUCKET}/data.parquet"
BIGQUERY_DATASET = "your_dataset"
BIGQUERY_TABLE = "your_table"

# Step 1: Extract - Read data from MongoDB
def read_from_mongo():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    return list(collection.find({}))

# Step 2: Transform - Convert to DataFrame & Store as Parquet
def transform_and_store_parquet(data):
    df = pd.DataFrame(data)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, "/tmp/data.parquet")

    # Upload to GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET)
    blob = bucket.blob("data.parquet")
    blob.upload_from_filename("/tmp/data.parquet")

# Step 3: Load - Process Data using Dataproc & Load to BigQuery
def clean_data_with_spark():
    spark = SparkSession.builder.appName("Data Cleaning").getOrCreate()
    df = spark.read.parquet(GCS_PARQUET_PATH)
    
    # Cleaning Steps
    cleaned_df = df.select(
        col("field1").alias("new_field1"),
        col("field2").cast("integer"),
        col("timestamp").cast("timestamp")
    )
    
    # Save cleaned data back to GCS
    cleaned_df.write.mode("overwrite").parquet(f"gs://{GCS_BUCKET}/cleaned_data.parquet")

def load_to_bigquery():
    client = bigquery.Client()
    dataset_ref = client.dataset(BIGQUERY_DATASET)
    table_ref = dataset_ref.table(BIGQUERY_TABLE)
    
    job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.PARQUET)
    uri = f"gs://{GCS_BUCKET}/cleaned_data.parquet"
    
    load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
    load_job.result()

# Run the Pipeline
if __name__ == "__main__":
    data = read_from_mongo()
    transform_and_store_parquet(data)
    clean_data_with_spark()
    load_to_bigquery()
