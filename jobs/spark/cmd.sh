

## VOICE STREAMING JOBS
./spark-submit \
    --class VoiceSilverStream \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1 \
    /home/jeth/Projects/spark-dev-repo/streaming-kafka/target/scala-2.13/app.jar \
    "localhost:9092" \
    "voice-bronze-cdr" \
    "voice-silver-cdr" \
    "/tmp/checkpoints/voice-silver-cdr"

./spark-submit \
    --class VoiceGoldStream \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1 \
    /home/jeth/Projects/spark-dev-repo/streaming-kafka/target/scala-2.13/app.jar \
    "localhost:9092" \
    "voice-silver-cdr" \
    "voice-gold-cdr" \
    "/tmp/checkpoints/voice-gold-cdr"


./spark-submit \
    --class SmsSilverStream \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1 \
    /home/jeth/Projects/spark-dev-repo/streaming-kafka/target/scala-2.13/app.jar \
    "localhost:9092" \
    "sms-bronze-cdr" \
    "sms-silver-cdr" \
    "/tmp/checkpoints/sms-silver-cdr"

./spark-submit \
    --class SmsGoldStream \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1 \
    /home/jeth/Projects/spark-dev-repo/streaming-kafka/target/scala-2.13/app.jar \
    "localhost:9092" \
    "sms-silver-cdr" \
    "sms-gold-cdr" \
    "/tmp/checkpoints/sms-gold-cdr"

./spark-submit \
    --class DataSilverStream \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1 \
    /home/jeth/Projects/spark-dev-repo/streaming-kafka/target/scala-2.13/app.jar \
    "localhost:9092" \
    "data-bronze-cdr" \
    "data-silver-cdr" \
    "/tmp/checkpoints/data-silver-cdr"

./spark-submit \
    --class DataGoldStream \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1 \
    /home/jeth/Projects/spark-dev-repo/streaming-kafka/target/scala-2.13/app.jar \
    "localhost:9092" \
    "data-silver-cdr" \
    "data-gold-cdr" \
    "/tmp/checkpoints/data-gold-cdr"



```


### BATCH JOBS
```bash

export SBT_OPTS="-Xms2G -Xmx4G -XX:+UseG1GC"

export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=admin
export AWS_SECRET_ACCESS_KEY=password

spark-shell \
  --master local[*] \


./spark-submit \
  --class CreateIcebergTable \
  /home/jeth/Projects/OMEA/POC/Poc_rfp_omea/jobs/spark/spark-iceberg-project/target/scala-2.13/app.jar \
  s3a://datalake/schemas/ \
  voice


./spark-submit \
  --class LoadToIceberg \
  /home/jeth/Projects/OMEA/POC/Poc_rfp_omea/jobs/spark/spark-iceberg-project/target/scala-2.13/app.jar \
  s3a://datalake/voice/ \
  voice \
  bronze.voice


./spark-submit \
  --class LoadVoiceSilverTable \
  /home/jeth/Projects/OMEA/POC/Poc_rfp_omea/jobs/spark/spark-iceberg-project/target/scala-2.13/app.jar \
  "2026-02-02" \
  bronze.voice \
  silver.voice



./spark-submit \
  --class LoadVoiceGoldTables \
  /home/jeth/Projects/OMEA/POC/Poc_rfp_omea/jobs/spark/spark-iceberg-project/target/scala-2.13/app.jar \
  "2026-02-02" \
  silver.voice 


spark-submit \
  --master local[*] \
  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
  --conf spark.sql.catalog.iceberg=org.apache.iceberg.spark.SparkCatalog \
  --conf spark.sql.catalog.iceberg.type=hadoop \
  --conf spark.sql.catalog.iceberg.warehouse=s3a://warehouse/iceberg \
  --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
  --conf spark.hadoop.fs.s3a.access.key=admin \
  --conf spark.hadoop.fs.s3a.secret.key=password \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
  load_to_iceberg.jar



  --conf spark.eventLog.enabled=true \
  --conf spark.eventLog.dir=s3a://spark-logs/ \
  --conf spark.hadoop.fs.s3a.endpoint=http://minio-service.default.svc.cluster.local:9000 \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.hadoop.fs.s3a.access.key=YOUR_ACCESS_KEY \
  --conf spark.hadoop.fs.s3a.secret.key=YOUR_SECRET_KEY
```
