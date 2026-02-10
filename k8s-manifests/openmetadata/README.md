# Deploy

```bash
# CREATE K8S SECRET
kubectl create secret generic mysql-secrets --from-literal=openmetadata-mysql-password=openmetadata_password
kubectl create secret generic airflow-secrets --from-literal=openmetadata-airflow-password=admin
kubectl create secret generic airflow-mysql-secrets --from-literal=airflow-mysql-password=airflow_pass

# Add helm repo
helm repo add open-metadata https://helm.open-metadata.org/
helm repo update

# Install openmetadata-dependencies

helm show values open-metadata/openmetadata-dependencies > values-dependencies.yaml

helm upgrade --install openmetadata-dependencies open-metadata/openmetadata-dependencies --values values-dependencies.yaml   --n data-gov --create-namespace --debug --timeout 10m

helm uninstall openmetadata-dependencies


# Install openmetadata
helm show values open-metadata/openmetadata > values.yaml
helm upgrade --install openmetadata open-metadata/openmetadata --values values.yaml --n data-gov --create-namespace --debug --timeout 10m



helm uninstall openmetadata -n data-gov
helm uninstall openmetadata-dependencies -n data-gov

```



# LINKS
https://docs.open-metadata.org/latest/quick-start/local-kubernetes-deployment