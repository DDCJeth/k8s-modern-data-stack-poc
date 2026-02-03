# AIRFLOW

```bash
# host.minikube.internal
## APACHE AIRFLOW CHART HELM
helm repo add apache-airflow https://airflow.apache.org
# helm show values apache-airflow/airflow > values-airflow.yaml

## BITNAMI AIRFLOW CHART HELM
# helm repo add bitnami oci://registry-1.docker.io/bitnamicharts
# helm install my-release bitnami/airflow

kubectl create namespace airflow

kubectl create secret generic github-git-sync-secret --from-literal=GIT_SYNC_USERNAME=DDCJeth --from-literal=GIT_SYNC_PASSWORD=$PAT_GITHUB --from-literal=GITSYNC_USERNAME=DDCJeth --from-literal=GITSYNC_PASSWORD=$PAT_GITHUB -n airflow
kubectl get secret --namespace airflow github-git-sync-secret -o jsonpath="{.data.GIT_SYNC_USERNAME}" | base64 --decode

helm upgrade --install airflow apache-airflow/airflow  -f values-custom.yaml --namespace airflow --debug --timeout 10m01s

kubectl apply -f airflow-spark-rbac.yaml

helm uninstall airflow -n airflow


# https://www.mail-archive.com/commits@airflow.apache.org/msg478648.html
# https://www.youtube.com/watch?v=rIlNF1z18_s
```