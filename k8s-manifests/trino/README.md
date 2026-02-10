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
```bash
kubectl -n trino get po -o name | grep coordinator
kubectl -n trino exec -it $(kubectl -n trino get po -o name | grep coordinator) -- trino

SELECT _message FROM kakfa
```

```sql


SHOW CATALOGS;


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
