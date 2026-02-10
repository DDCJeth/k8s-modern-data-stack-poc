# Deploy Nifi


### Nifi

```bash
kubectl apply -f nifi-deployment.yaml

```


### Zookeeper
```bash
kubectl apply -f zookeeper-sts.yaml

kubectl delete -f zookeeper-sts.yaml
kubectl delete pvc --all -n nifi
```



# LINKS
https://github.com/sakkiii/apache-nifi-helm

These resources were kept due to the resource policy:
[Secret] encryption-sensitive-key
[Secret] certificate-keystore-password

release "nifi" uninstalled