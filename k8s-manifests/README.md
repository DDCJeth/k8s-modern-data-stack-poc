## Kubernetes manifests for Poc_rfp_omea ⚙️

Ce dossier contient des manifests Kubernetes pour reproduire l'architecture définie dans `docker-compose.yml`.

Ressources incluses:
- Namespace: `omea`
- MinIO (Deployment + Service + PVC)
- `mc` Job pour initialiser les buckets
- Postgres (Deployment + Service + PVC)
- Iceberg REST (Deployment + Service)
- Trino (Deployment + Service + ConfigMap pour `iceberg.properties`)
- cdr-generator (Deployment + Service + PVC)
- NiFi (Deployment + Service + PVC)
- HPAs pour cdr-generator, trino et iceberg-rest

Déploiement (exemple):

1. Appliquer le namespace + toutes les ressources:

   kubectl apply -f k8s-manifests/

2. Vérifier les ressources:

   kubectl -n omea get all

3. Initialiser MinIO buckets (Job `mc-init` doit se terminer automatiquement):

   kubectl -n omea get jobs

Notes & recommandations 💡:
- Les Services exposés sont de type `LoadBalancer` pour un accès simple; sur un cluster sans LoadBalancer (minikube), utilisez `NodePort` ou configurez un `Ingress`.
- Ajustez les `PersistentVolumeClaim` (taille, storageClass) selon votre infra.
- Si vous souhaitez utiliser HPA, assurez-vous d'avoir le metrics-server installé dans le cluster.
- Les images construites localement (ex: `poc_rfp_omea/cdr-generator:latest`) doivent être disponibles dans le registry du cluster avant de déployer.

Si vous voulez, je peux:
- Générer un `kustomization.yaml` pour faciliter les overlays (dev/prod)
- Ajouter des `NetworkPolicy` et `ResourceQuota` pour production
- Convertir les Services `LoadBalancer` en `Ingress` avec TLS

## Sécrets & sécurité 🔐

- Un `Secret` Kubernetes nommé **`omea-secrets`** est fourni (`secrets.yaml`) pour stocker les credentials (MinIO, Postgres, AWS). Par défaut il contient des valeurs d'exemple — **remplacez-les** avant déploiement en production.
- Exemple (recommandé) pour créer/mettre à jour sans stocker en clair :

  ```bash
  kubectl -n omea create secret generic omea-secrets \
    --from-literal=MINIO_ROOT_USER=admin \
    --from-literal=MINIO_ROOT_PASSWORD=password \
    --from-literal=AWS_ACCESS_KEY_ID=admin \
    --from-literal=AWS_SECRET_ACCESS_KEY=password \
    --from-literal=POSTGRES_USER=iceberg \
    --from-literal=POSTGRES_PASSWORD=iceberg_pass \
    --dry-run=client -o yaml | kubectl apply -f -
  ```

- Pour plus de sécurité, utilisez **Bitnami SealedSecrets** ou **HashiCorp Vault** et évitez de committer les secrets.

---
