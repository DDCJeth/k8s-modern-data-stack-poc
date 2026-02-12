**Overview**

This folder contains Kubernetes manifests to run a simple SFTP file server and a CDR generation application that generates CDR files and sends them to the sftp server.

**Manifests included**
- **Files:** [sftp-server.yaml](k8s-manifests/app-generator/sftp-server.yaml) and [cdr-app-generator.yaml](k8s-manifests/app-generator/cdr-app-generator.yaml)

**What they do**
- **sftp-server.yaml:** Deploys an SFTP server (atmoz/sftp) as a Service + Deployment. The container runs a user `foo` with a password placeholder `passwordSftp` and a chrooted `upload` directory. The manifest grants the container `SYS_ADMIN` capability required by atmoz/sftp.

- **cdr-app-generator.yaml:** Deploys the `ddcj/cdr-generator:v2` application and a PersistentVolumeClaim `cdr-data-pvc`. The app reads SFTP connection details from environment variables (`SFTP_HOST`, `SFTP_PORT`, `SFTP_USER`, `SFTP_PASS`, `SFTP_PATH`). Currently `SFTP_PASS` is set to the literal `passwordSftp` in the manifest — replace this with a Kubernetes Secret for production.

**Quick deployment (local / test)**
1. Create the namespace used in the manifests (if not present):

```
kubectl create namespace app
```

2. (Optional) Create a Secret to hold SFTP credentials and avoid plaintext passwords:

```
kubectl create secret generic sftp-credentials -n app \
	--from-literal=username=foo \
	--from-literal=password=REPLACE_ME
```

3. Apply the SFTP manifest and the CDR app manifest:

```
kubectl apply -f k8s-manifests/app-generator/sftp-server.yaml -n app
kubectl apply -f k8s-manifests/app-generator/cdr-app-generator.yaml -n app
```

4. Verify pods and services:

```
kubectl get pods,svc -n app
kubectl logs -l app=fileserver -n app
kubectl logs -l app=cdr-generator -n app
```

**Recommended secure change (use Secret for SFTP_PASS)**
- Edit `cdr-app-generator.yaml` to pull the password from the Secret instead of a literal. Replace the `env` entry for `SFTP_PASS` with:

```
- name: SFTP_PASS
	valueFrom:
		secretKeyRef:
			name: sftp-credentials
			key: password
```


**Troubleshooting**
- If the fileserver pod fails to start, check `kubectl describe pod <pod>` and `kubectl logs` for permission issues related to chroot or capability requirements.
- If PVC remains Pending, your cluster likely lacks a matching storage class.

**Next steps / production tips**
- Replace plaintext passwords with Secrets and RBAC where appropriate.
- Use a stable storage class for PVCs that supports `ReadWriteMany`.
- Lock down networking (NetworkPolicy) and limit container capabilities if you can provide secure alternatives to `SYS_ADMIN`.

**Files**
- See [sftp-server.yaml](k8s-manifests/app-generator/sftp-server.yaml)
- See [cdr-app-generator.yaml](k8s-manifests/app-generator/cdr-app-generator.yaml)

---



