import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._


val spark = SparkSession.builder()
    .appName("MinIO to Iceberg")
    .getOrCreate()

// ----------------------------------------------------
// 1. Read file from MinIO (CSV example)
// ----------------------------------------------------

val cdrType = "sms"
val inputPath = s"s3a://datalake/$cdrType"

val df: DataFrame = spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(inputPath)


// Optional: basic transformation
val enrichedDf = df
    .withColumn("ingestion_date", current_date())

// ----------------------------------------------------
// 2. Create Iceberg table if not exists
// ----------------------------------------------------
spark.sql("CREATE NAMESPACE IF NOT EXISTS cdr".stripMargin)

spark.sql(
    """
    |CREATE TABLE IF NOT EXISTS cdr.sms_logs (
    |    `timestamp`        TIMESTAMP,
    |    sms_id             STRING,
    |    sender_msisdn       STRING,
    |    receiver_msisdn     STRING,
    |    sms_type            STRING,
    |    message_length      INT,
    |    cell_id             STRING,
    |    region              STRING,
    |    delivery_status     STRING,
    |    charging_amount     DECIMAL(10,2),
    |    ingestion_date      DATE
    |)
    |USING iceberg
    |PARTITIONED BY (days(`timestamp`));

    """.stripMargin)

// ----------------------------------------------------
// 3. Write data into Iceberg table
// ----------------------------------------------------
enrichedDf
    .writeTo("cdr.sms_logs")
    .append()

spark.stop()






