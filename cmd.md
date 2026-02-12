# SFTP SERVER

```bash
docker run --rm --name fileserver -p 2222:22 -d atmoz/sftp:debian foo:pass:::upload
docker run     -v /tmp/upload:/home/foo/upload     -p 2222:22 -d atmoz/sftp:debian     foo:pass:1001
```

# K8S cluster

```bash
minikube start --cpus=4 --memory=8192
minikube start --cpus=6 --memory=16384 -disk-size='100000mb'
```

## DATA STACK

```bash

# I - Ingestion

kubectl create namespace nifi
## App generator CDRs
kubectl apply -f k8s-manifests/app-generator/cdr-generator-deployment.yaml
## Nifi
kubectl apply -f k8s-manifests/nifi/nifi-deployment.yaml

# II - Lakehouse

kubectl create namespace lakehouse
## Minio
helm repo add minio https://charts.min.io/
helm repo update

helm upgrade --install minio minio/minio -f k8s-manifests/lakehouse/values-minio.yaml -n lakehouse --create-namespace --debug --timeout 10m

## Iceberg
### Postgresql
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

helm upgrade  --install db bitnami/postgresql -f k8s-manifests/lakehouse/values-pg.yaml -n lakehouse --create-namespace --debug --timeout 10m
### Iceberg-rest
kubectl apply -f k8s-manifests/lakehouse/iceberg-rest-deploy.yaml




## Kafka
helm repo add strimzi https://strimzi.io/charts/
helm repo update 

### Install the operator
helm install strimzi-kafka-operator strimzi/strimzi-kafka-operator \
  --namespace kafka \
  --create-namespace \
  --set watchAnyNamespace=true

### Install cluster
kubectl apply -f k8s-manifests/kafka/kafka-cluster.yaml


## Spark
### Add Spark operator helm repo
helm repo add spark-operator https://kubeflow.github.io/spark-operator
helm repo update

### Install spark-operator helm chart in spark namespace
helm upgrade --install spark-operator spark-operator/spark-operator \
    -f k8s-manifests/sparkoperator/values-custom.yaml \
    --namespace spark \
    --create-namespace --debug --timeout 10m01s


kubectl apply -f k8s-manifests/lakehouse/minio-credentials.yaml 

## Trino
### Add Trino Repo
helm repo add trino https://trinodb.github.io/charts
helm repo update
### Install Trino
helm upgrade --install trino trino/trino -f k8s-manifests/trino/values-trino.yaml -n trino --create-namespace --debug --timeout 10m


## Superset


## Openmetadata


```



### SPARK STREAMING

```bash
./spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1

## 192.168.49.1 VOICE STREAMING JOBS
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


# KAFKA DOCKER

```bash
docker exec -it broker bash
cd /opt/kafka/bin

./kafka-console-producer.sh --bootstrap-server localhost:9092 --topic cdr-test

./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic cdr-test --from-beginning
```


# SPARK BACTH LAUNCH
```bash


export SBT_OPTS="-Xms2G -Xmx4G -XX:+UseG1GC"
sbt clean assembly

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

```