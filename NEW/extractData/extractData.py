from pyspark.sql import SparkSession

num_workers = 4;
spark = SparkSession \
    .builder \
    .master("local[%d]"%(num_workers)) \
    .appName("WINF") \
    .getOrCreate() 

sc = spark.sparkContext

RAW_DATA_URL = "/user/root/wikidata5m_entity.txt"
EXTRACTED_DATA_URL = "/user/root/extracted_data"


def exctractRawData(sc, rawDataPath):
    raw_data = sc.textFile(rawDataPath)\
                 .map(lambda row: (row.split("\t")[0], ";".join(row.split("\t")[1:])))\
                 .toDF(["title_id", "alt_names"])

    return raw_data


if __name__ == '__main__':

    raw_data_df = exctractRawData(sc, RAW_DATA_URL)
    raw_data_df.write\
            .mode("overwrite")\
            .option("header", "true")\
            .option("footer", "true")\
            .parquet(EXTRACTED_DATA_URL)\

    print("Data boli extrahovane a ulozene!")
