## Deploy Superset

```bash
helm repo add superset https://apache.github.io/superset
helm repo update

helm show values superset/superset > values-superset.yaml

helm upgrade --install --values values-superset.yaml superset superset/superset --n trino --create-namespace --debug --timeout 10m

helm uninstall superset
```

## Links

https://superset.apache.org/docs/installation/kubernetes/
https://stackoverflow.com/questions/75136278/add-trino-dataset-to-apache-superset