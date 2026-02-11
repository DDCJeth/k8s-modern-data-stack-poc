# Deploy

```bash
# CREATE K8S SECRET
kubectl create ns data-gov 
kubectl create secret generic mysql-secrets --from-literal=openmetadata-mysql-password=openmetadata_password -n data-gov
kubectl create secret generic airflow-secrets --from-literal=openmetadata-airflow-password=admin -n data-gov
kubectl create secret generic airflow-mysql-secrets --from-literal=airflow-mysql-password=airflow_pass -n data-gov

# Add helm repo
helm repo add open-metadata https://helm.open-metadata.org/
helm repo update

# Install openmetadata-dependencies

helm show values open-metadata/openmetadata-dependencies > values-dependencies.yaml

helm upgrade --install openmetadata-dependencies open-metadata/openmetadata-dependencies --values values-dependencies.yaml -n data-gov --create-namespace --debug --timeout 10m

helm uninstall openmetadata-dependencies


# Install openmetadata
helm show values open-metadata/openmetadata > values-openmetadata.yaml
helm upgrade --install openmetadata open-metadata/openmetadata --values values.yaml -n data-gov --create-namespace --debug --timeout 10m



helm uninstall openmetadata -n data-gov
helm uninstall openmetadata-dependencies -n data-gov


# NOTES:
# 1. Get the application URL by running these commands:
export POD_NAME=$(kubectl get pods --namespace data-gov -l "app.kubernetes.io/name=openmetadata,app.kubernetes.io/instance=openmetadata" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace data-gov $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
# echo "Visit http://127.0.0.1:8585 to use your application"
kubectl --namespace data-gov port-forward $POD_NAME 8585:$CONTAINER_PORT

## admin@open-metadata.org:admin
```



# LINKS
https://docs.open-metadata.org/latest/quick-start/local-kubernetes-deployment