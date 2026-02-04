

kubectl delete -f lakehouse/iceberg-rest-deploy.yaml
sleep 5
helm uninstall db -n lakehouse
sleep 5
helm uninstall minio -n lakehouse
sleep 5
kubectl delete pvc data-db-postgresql-0 -n lakehouse

sleep 10


helm upgrade --install minio minio/minio -f lakehouse/values-minio.yaml -n lakehouse --create-namespace --debug --timeout 10m
sleep 5

helm upgrade  --install db bitnami/postgresql -f lakehouse/values-pg.yaml -n lakehouse --create-namespace --debug --timeout 10m
sleep 5

kubectl apply -f lakehouse/iceberg-rest-deploy.yaml

sleep 10