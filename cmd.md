


# AIRFLOW

```bash
# host.minikube.internal
## APACHE AIRFLOW CHART HELM
helm repo add apache-airflow https://airflow.apache.org
# helm show values apache-airflow/airflow > values-airflow.yaml

## BITNAMI AIRFLOW CHART HELM
# helm repo add bitnami oci://registry-1.docker.io/bitnamicharts
# helm install my-release bitnami/airflow

kubectl create namespace airflow

kubectl create secret generic github-git-sync-secret --from-literal=GIT_SYNC_USERNAME=DDCJeth --from-literal=GIT_SYNC_PASSWORD=$PAT_GITHUB --from-literal=GITSYNC_USERNAME=DDCJeth --from-literal=GITSYNC_PASSWORD=$PAT_GITHUB -n airflow
kubectl get secret --namespace airflow github-git-sync-secret -o jsonpath="{.data.GIT_SYNC_USERNAME}" | base64 --decode

kubectl apply -f airflow-sa.yaml

helm upgrade --install airflow apache-airflow/airflow  -f values-airflow-custom.yaml --namespace airflow --debug --timeout 10m01s

kubectl get secret --namespace airflow airflow-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode
# dFNmMGxSS2xId3pySXJJNHFxUm1xd1FHQjFxa0Z3eko=
helm uninstall airflow -n airflow

```







# SPARK 
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

```