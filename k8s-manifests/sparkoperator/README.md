## Deploy Spark Operator

```bash
# Add Spark operator helm repo
helm repo add spark-operator https://kubeflow.github.io/spark-operator

# Check if repo has been added successfuly
helm repo list
helm repo update

# Install spark-operator helm chart in spark namespace
# helm install my-release spark-operator/spark-operator --namespace spark-operator --set "spark.jobNamespaces={test-ns}"

helm upgrade --install spark-operator spark-operator/spark-operator \
    -f values-custom.yaml \
    --namespace spark \
    --create-namespace --debug --timeout 10m01s


# Check status of the helm chart installation
helm status --namespace spark spark-operator

# Delete application
helm delete spark-operator -n spark

# Check deployment
kubectl get all -n spark

kubectl get po -n spark
```

## launch Spark Job

- 
```bash
kubectl apply -f examples/spark-pi.yaml

# View jobs info
kubectl get sparkapplication spark-pi -o=yaml

# Check event
kubectl describe sparkapplication spark-pi
```


## Explaination

```bash
kubectl explain sparkapplication.spec
```

## Links
https://www.kubeflow.org/docs/components/spark-operator/getting-started/
https://medium.com/@SaphE/deploying-apache-spark-on-kubernetes-using-helm-charts-simplified-cluster-management-and-ee5e4f2264fd