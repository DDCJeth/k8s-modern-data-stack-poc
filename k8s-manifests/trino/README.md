## Deploy Trino


```bash
helm repo add trino https://trinodb.github.io/charts
helm repo update
#helm show values trino/trino > values-custom.yaml
helm upgrade --install trino trino/trino -f values-trino.yaml -n lakehouse --create-namespace --debug --timeout 10m

```

## Test
```bash
kubectl -n lakehouse exec -it trino-coordinator-7484c844db-4vrsx -- trino
```

```sql

SHOW CATALOGS;

CREATE SCHEMA IF NOT EXISTS lakehouse.db;

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
```
```