# Deploy

```bash
helm repo add jetstack https://charts.jetstack.io --force-update

helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.19.2 \
  --set crds.enabled=true


# helm install \
#   cert-manager oci://quay.io/jetstack/charts/cert-manager \
#   --version v1.19.2 \
#   --namespace cert-manager \
#   --create-namespace \
#   --set crds.enabled=true
```


# Links
https://cert-manager.io/docs/installation/helm/