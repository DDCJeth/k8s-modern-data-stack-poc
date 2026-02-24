## GENERATION CDR

```bash
# 1. Execute script to generate cdr
kubectl get pods -l app=cdr-generator -o jsonpath='{.items[*].metadata.name}'
kubectl exec -it $(kubectl get pods -l app=cdr-generator -o jsonpath='{.items[*].metadata.name}') -- bash

## 1.1 Send to SFTP
python /app/scripts/batch_generation_cdr.py --type voice --storage sftp --sftp-host $SFTP_HOST --sftp-port $SFTP_PORT --sftp-user $SFTP_USER --sftp-password $SFTP_PASS --sftp-path $SFTP_PATH

python /app/scripts/batch_generation_cdr.py --type voice --file 2 --storage sftp --sftp-host $SFTP_HOST --sftp-port $SFTP_PORT --sftp-user $SFTP_USER --sftp-password $SFTP_PASS --sftp-path $SFTP_PATH

python /app/scripts/batch_generation_cdr.py --type sms --file 90 --storage sftp --sftp-host $SFTP_HOST --sftp-port $SFTP_PORT --sftp-user $SFTP_USER --sftp-password $SFTP_PASS --sftp-path $SFTP_PATH

python /app/scripts/batch_generation_cdr.py --type data --file 90 --storage sftp --sftp-host $SFTP_HOST --sftp-port $SFTP_PORT --sftp-user $SFTP_USER --sftp-password $SFTP_PASS --sftp-path $SFTP_PATH

## 1.2 Send to Minio
python /app/scripts/batch_generation_cdr.py --type voice --file 2 --storage s3 --bucket rawdata --endpoint-url http://minio.minio.svc.cluster.local:9000 --access-key $AWS_ACCESS_KEY_ID --secret-key $AWS_SECRET_ACCESS_KEY

# python /app/scripts/batch_generation_cdr.py --type data --file 100 --records 1000 --storage sftp --sftp-host $SFTP_HOST --sftp-port $SFTP_PORT --sftp-user $SFTP_USER --sftp-password $SFTP_PASS --sftp-path $SFTP_PATH

# python /app/scripts/continue_generation_cdr.py --type data --file 100 --records 1000 --storage sftp --sftp-host $SFTP_HOST --sftp-port $SFTP_PORT --sftp-user $SFTP_USER --sftp-password $SFTP_PASS --sftp-path $SFTP_PATH

# 1.1 Network Tshoot
kubectl run debug-network --rm -it --image=nicolaka/netshoot -- /bin/bash

curl -v telnet://fileserver.artefact.svc.cluster.local:9222

# 2. Check generated cdrs on sftp server
kubectl exec -it $(kubectl get pods -l app=fileserver -o jsonpath='{.items[*].metadata.name}') -- bash
cd /home/foo/upload
```

## KAFKA

```bash

# List topics
kubectl run kafka-topics-list -ti --image=quay.io/strimzi/kafka:0.50.0-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-topics.sh --bootstrap-server cluster-kafka-bootstrap.kafka.svc.cluster.local:9092 --list

# Check topics
kubectl run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.50.0-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server cluster-kafka-bootstrap.kafka.svc.cluster.local:9092 --topic voice-bronze-cdr --from-beginning

kubectl run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.50.0-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server cluster-kafka-bootstrap.kafka.svc.cluster.local:9092 --topic voice-silver-cdr --from-beginning

kubectl run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.50.0-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server cluster-kafka-bootstrap.kafka.svc.cluster.local:9092 --topic voice-gold-cdr --from-beginning

##############
# Delete topics
kubectl run kafka-topic-delete -ti --image=quay.io/strimzi/kafka:0.50.0-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-topics.sh --bootstrap-server cluster-kafka-bootstrap.kafka.svc.cluster.local:9092 --delete --topic sms-bronze-cdr
```


## TRINO CLIENT
```bash
# Deploy Trino pod for client
kubectl run trino-cli -ti --image=trinodb/trino:latest --restart=Never --rm=true  -- /bin/bash -c "trino --server https://trino.trino.svc.cluster.local:8443 --insecure --user=trino --password"
```

```sql

--- données du POC
/* ICEBERG*/
select count(*) from iceberg.bronze.voice; --800000
select count(*) from iceberg.silver.voice;


select count(*) from iceberg.bronze.sms;
select count(*) from iceberg.silver.sms;


select count(*) from iceberg.bronze.data;
select count(*) from iceberg.silver.data;

/* KAFKA */
select count(*) from kafka.default."voice-bronze-cdr";
select count(*) from kafka.default."voice-silver-cdr";

select count(*) from kafka.default."sms-bronze-cdr";
select count(*) from kafka.default."sms-silver-cdr";

select count(*) from kafka.default."data-bronze-cdr";
select count(*) from kafka.default."data-silver-cdr";

-- Test trino
SELECT * FROM tpch.sf3000.customer limit 10;

-- Test iceberg
DROP TABLE iceberg.test.logs;
DROP SCHEMA iceberg.test;
CREATE SCHEMA iceberg.test;

CREATE TABLE iceberg.test.logs (
    id bigint, 
    message varchar, 
    level varchar
) ;
WITH (
    partitioning = ARRAY['level']
);


-- Insert data
INSERT INTO iceberg.test.logs VALUES (1, 'System started', 'INFO'), (2, 'System stop', 'WARN'), (3, 'Null pointer exception', 'ERROR');

-- Query data
SELECT * FROM iceberg.test.logs;


-- Test Kafka
CREATE CATALOG streaming USING kafka
WITH (
  "kafka.table-names" = 'voice-bronze-cdr',
  "kafka.nodes" = 'cluster-kafka-bootstrap.kafka.svc.cluster.local:9092'
);

CREATE CATALOG streaming USING kafka
WITH (
  "kafka.table-names" = 'voice-bronze-cdr,voice-silver-cdr,voice-gold-cdr,voice-gold-cdr-tower,sms-bronze-cdr,sms-silver-cdr,sms-gold-cdr,sms-gold-cdr-tower,data-bronze-cdr,data-silver-cdr,data-gold-cdr,data-gold-cdr-tower',
  "kafka.nodes" = 'cluster-kafka-bootstrap.kafka.svc.cluster.local:9092'
);




-- TEST DAVID
create schema if not exists iceberg.iceberg_schema
    with (LOCATION = 's3://trino-data/icebergtest/');

CREATE TABLE IF NOT EXISTS iceberg.test2.log (
    id INT,
    message VARCHAR,
    level VARCHAR
)
WITH (
    format = 'PARQUET'
);


INSERT INTO iceberg.test2.log VALUES (1, 'hello iceberg', 'INFO')


```


## SPARK-SHELL
```bash
# Deploy Trino pod for client
kubectl run sparkshell -it --rm --restart=Never  --image=ddcj/spark-job:omea-pocv0.1 -- /bin/bash -c "sleep infinity"
kubectl exec -it sparkshell -- bash

```
