
```bash

docker build --no-cache -t mon-sftp-debian .

docker run --rm \
    -p 2222:22 \
    -e SFTP_USERS="bob:password123" \
    --name mon-serveur-sftp \
    mon-sftp-debian


```bash