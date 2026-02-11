## Deploy Trino


```bash
helm repo add trino https://trinodb.github.io/charts
helm repo update
#helm show values trino/trino > values-custom.yaml
helm upgrade --install trino trino/trino -f values-trino.yaml -n trino --create-namespace --debug --timeout 10m

helm uninstall trino
```

## Test
```bash
kubectl -n trino get po -o name | grep coordinator
kubectl -n trino exec -it $(kubectl -n trino get po -o name | grep coordinator) -- trino

# # 1. Get the application URL by running these commands:
# export POD_NAME=$(kubectl get pods --namespace data-gov -l "app.kubernetes.io/name=openmetadata,app.kubernetes.io/instance=openmetadata" -o jsonpath="{.items[0].metadata.name}")
# export CONTAINER_PORT=$(kubectl get pod --namespace data-gov $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
```

```sql


SHOW CATALOGS;

SHOW TABLES FROM kafka.default;

SELECT _message FROM kakfa.default."voice-bronze-cdr" LIMIT 10;


CREATE SCHEMA IF NOT EXISTS iceberg.db;

-- Create a table

CREATE TABLE iceberg.db.logs (
    id bigint, 
    message varchar, 
    level varchar
) 
WITH (
    partitioning = ARRAY['level'] -- Partitions by level
);


-- Insert data
INSERT INTO iceberg.db.logs VALUES (1, 'System started', 'INFO'), (2, 'System stop', 'WARN'), (3, 'Null pointer exception', 'ERROR');

-- Query data
SELECT * FROM iceberg.db.logs;



SELECT * FROM tpch.sf3000.customer;

```
