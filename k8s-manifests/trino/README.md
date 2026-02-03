## Deploy Trino

```bash
helm repo add trino https://trinodb.github.io/charts
helm repo update
#helm show values trino/trino > values-custom.yaml
helm upgrade --install trino trino/trino -f values-trino.yaml -n lakehouse --create-namespace --debug --timeout 10m

```