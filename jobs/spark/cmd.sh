

```bash

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
  cdr.voice



./spark-submit \
  --class LoadToIceberg \
  /home/jeth/Projects/OMEA/POC/Poc_rfp_omea/jobs/spark/spark-iceberg-project/target/scala-2.13/app.jar \
  s3a://datalake/sms/ \
  sms \
  cdr.sms


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

```