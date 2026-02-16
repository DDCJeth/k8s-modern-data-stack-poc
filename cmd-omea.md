## GENERATION CDR

```bash
# 1. Execute script to generate cdr
kubectl get pods -l app=cdr-generator -o jsonpath='{.items[*].metadata.name}'
kubectl exec -it $(kubectl get pods -l app=cdr-generator -o jsonpath='{.items[*].metadata.name}') -- bash

python /app/scripts/batch_generation_cdr.py --type data --file 100 --records 1000 --storage sftp --sftp-host $SFTP_HOST --sftp-port $SFTP_PORT --sftp-user $SFTP_USER --sftp-password $SFTP_PASS --sftp-path $SFTP_PATH

curl -v telnet://fileserver.artefact.svc.cluster.local:2222

# 2. Check generated cdrs on sftp server
kubectl exec -it $(kubectl get pods -l app=fileserver -o jsonpath='{.items[*].metadata.name}') -- bash
cd /home/foo/upload
```

## KAFKA

```bash
# Check topics
kubectl run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.50.0-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server cluster-kafka-bootstrap.kafka.svc.cluster.local:9092 --topic voice-bronze-cdr --from-beginning

kubectl run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.50.0-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server cluster-kafka-bootstrap.kafka.svc.cluster.local:9092 --topic voice-silver-cdr --from-beginning

kubectl run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.50.0-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server cluster-kafka-bootstrap.kafka.svc.cluster.local:9092 --topic voice-gold-cdr --from-beginning
```

## TRINO CLIENT
```bash
# Deploy Trino pod for client
kubectl run trino-cli -ti --image=trinodb/trino:latest --restart=Never --rm=true  -- /bin/bash -c "trino --server https://trino.trino.svc.cluster.local:8443 --insecure --user=trino --password"
```

```sql
-- Test trino
SELECT * FROM tpch.sf3000.customer limit 10;

-- Test iceberg
CREATE SCHEMA iceberg.test;

CREATE TABLE iceberg.test.logs (
    id bigint, 
    message varchar, 
    level varchar
) 
WITH (
    partitioning = ARRAY['level'] -- Partitions by level
);


-- Insert data
INSERT INTO iceberg.test.logs VALUES (1, 'System started', 'INFO'), (2, 'System stop', 'WARN'), (3, 'Null pointer exception', 'ERROR');

-- Query data
SELECT * FROM iceberg.test.logs;


-- Test Kafka
CREATE CATALOG streaming USING kafka
WITH (
  "kafka.table-names" = 'voice-bronze-cdr,voice-silver-cdr,voice-gold-cdr,voice-gold-cdr-tower,sms-bronze-cdr,sms-silver-cdr,sms-gold-cdr,sms-gold-cdr-tower,data-bronze-cdr,data-silver-cdr,data-gold-cdr,data-gold-cdr-tower',
  "kafka.nodes" = 'cluster-kafka-bootstrap.kafka.svc.cluster.local:9092'
);

```
