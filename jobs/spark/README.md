
## REQUIREMENTS

- java version 17 for Spark 4.0.1
- sbt version 1.19

- To view all java versions installed
```bash
sudo update-alternatives --config java
```

- To install java 17 (if applicable)

```bash
sudo apt install openjdk-17-jdk
```

- Install sbt
```bash
echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | sudo tee /etc/apt/sources.list.d/sbt.list

curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo tee /etc/apt/trusted.gpg.d/sbt.asc

sudo apt-get update
sudo apt-get install sbt

sbt --version

```

## BUILD JAR

- Go to the root of the project
```bash
cd spark-iceberg-project
```
- Execute command below to 
```bash
sbt clean assembly
```


## LAUNCH SPARK JOB IN K8S

```bash
# export AWS_REGION=us-east-1
# export AWS_ACCESS_KEY_ID=admin
# export AWS_SECRET_ACCESS_KEY=password

kubectl create secret generic minio-creds \
  --from-literal=AWS_ACCESS_KEY_ID=admin \
  --from-literal=AWS_SECRET_ACCESS_KEY=password \
  --from-literal=AWS_REGION=us-east-1


kubectl apply -f dags/omea-poc-job.yml



# ./spark-submit \
#   --class LoadToIceberg \
#   /home/jeth/Projects/OMEA/POC/Poc_rfp_omea/jobs/spark/spark-iceberg-project/target/scala-2.13/app.jar \
#   s3a://datalake/voice/ \
#   voice \
#   bronze.voice

# ./spark-submit \
#   --class LoadVoiceSilverTable \
#   /home/jeth/Projects/OMEA/POC/Poc_rfp_omea/jobs/spark/spark-iceberg-project/target/scala-2.13/app.jar \
#   "2026-02-02" \
#   bronze.voice \
#   silver.voice

# ./spark-submit \
#   --class LoadVoiceGoldTables \
#   /home/jeth/Projects/OMEA/POC/Poc_rfp_omea/jobs/spark/spark-iceberg-project/target/scala-2.13/app.jar \
#   "2026-02-02" \
#   silver.voice 
```