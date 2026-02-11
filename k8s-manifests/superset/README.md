## Deploy Superset

```bash
# Deploy of Redis and Postgresql
kubectl create namespace data-viz
kubectl apply -f dependencies.yaml -n data-viz

```


### Bitnami Superset
```bash
#   registry: docker.io
#   repository: bitnamilegacy/superset
#   tag: 5.0.0-debian-12-r70

helm repo update
helm search repo bitnami/superset --versions
helm show values bitnami/superset > values-bitnami.yaml

helm upgrade --install --values values-bitnami.yaml superset bitnami/superset -n data-viz --create-namespace --debug --timeout 10m

helm uninstall superset -n trino
```






### Official Superset
```bash
helm repo add superset https://apache.github.io/superset
helm repo update
helm search repo superset --versions
# helm search repo superset/superset -l
# helm show values superset/superset --version 0.15.2 > values-0.15.2.yaml
# helm show values superset/superset --version 0.15.0 > values-0.15.0.yaml
helm show values superset/superset > values-superset.yaml

helm upgrade --install --values values-superset.yaml superset superset/superset -n trino --create-namespace --debug --timeout 10m

helm uninstall superset -n trino
```

## Links

https://superset.apache.org/docs/installation/kubernetes/
https://stackoverflow.com/questions/75136278/add-trino-dataset-to-apache-superset