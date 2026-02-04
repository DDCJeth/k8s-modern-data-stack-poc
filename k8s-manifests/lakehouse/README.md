## Deploy Minio

```bash
helm repo add minio https://charts.min.io/
helm repo update
#helm show values minio/minio > values-custom.yaml
kubectl create ns lakehouse
helm upgrade --install minio minio/minio -f values-minio.yaml -n lakehouse --create-namespace --debug --timeout 10m

```

## Deploy Postgresql

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
#helm show values bitnami/postgresql > values-custom.yaml
helm upgrade  --install db bitnami/postgresql -f values-pg.yaml -n lakehouse --create-namespace --debug --timeout 10m 

helm uninstall db -n lakehouse
kubectl delete pvc data-db-postgresql-0 -n lakehouse
```


## Deploy iceberg-rest

- With Manifest
```bash
kubectl apply -f iceberg-rest-deploy.yaml
```

- With helm chart (Bug with the postgres image : not possible to update image in values)

```bash
# helm repo add iceberg-rest-fixture https://ahmetfurkandemir.github.io/charts/demir-open-source/iceberg-rest-fixture/
# #helm show values iceberg-rest-fixture/iceberg-rest --version 0.0.1 > values.yaml
# k apply -f iceberg-s3-cred.yaml
# helm upgrade --install iceberg-rest iceberg-rest-fixture/iceberg-rest -f values-iceberg.yaml --version 0.0.1 -n lakehouse --debug --timeout 10m
# helm uninstall iceberg-rest -n lakehouse

```

## Links

https://artifacthub.io/packages/helm/iceberg-rest-fixture/iceberg-rest