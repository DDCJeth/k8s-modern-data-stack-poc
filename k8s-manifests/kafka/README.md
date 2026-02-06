# Kafka



## Option 1 : Strimzi Kafka Operator

```bash
helm repo add strimzi https://strimzi.io/charts/

helm repo update 

helm show values strimzi/strimzi-kafka-operator > values-strimzi.yaml


# Install the operator
helm install strimzi-kafka-operator strimzi/strimzi-kafka-operator \
  --namespace kafka \
  --create-namespace \
  --set watchAnyNamespace=true


kubectl apply -f kafka-metrics-configmap.yaml

kubectl apply -f kafka-cluster.yaml


```

## [Hands on](https://strimzi.io/docs/operators/latest/deploying.html#deploy-client-access-str)
```bash
#[Producer]
kubectl run kafka-producer -ti --image=quay.io/strimzi/kafka:0.50.0-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092 --topic my-topic
# if producer already exists
kubectl exec -it kafka-producer -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092 --topic my-topic

#[Consumer]
kubectl run kafka-consumer -ti --image=quay.io/strimzi/kafka:0.50.0-kafka-4.1.1 --rm=true --restart=Never -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092 --topic my-topic --from-beginning


```

/opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic data_cdr
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic data_cdr --from-beginning


## Option 2 : Bitnami
- Install
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

helm search repo bitnami/kafka --versions

helm show values bitnami/kafka --version 32.4.3 > values.yaml
helm install kafka bitnami/kafka --version 32.4.3 -f values-kafka.yaml -n streaming --create-namespace --debug --timeout 10m
```

- Navigate
```bash

kubectl run kafka-client --restart='Never' --image docker.io/bitnami/kafka:latest --namespace streaming --command -- sleep infinity

kubectl cp --namespace streaming ./client.properties kafka-client:/tmp/client.properties

```







## LINKS
https://oneuptime.com/blog/post/2026-01-17-helm-kafka-kubernetes-deployment/view
https://artifacthub.io/packages/helm/bitnami/kafka
https://strimzi.io/docs/operators/latest/deploying.html#deploying-cluster-operator-helm-chart-str
https://github.com/strimzi/strimzi-kafka-operator/tree/0.50.0#