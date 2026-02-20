# Base Debian légère
FROM debian:bookworm-slim

# Installation d'OpenSSH et nettoyage pour réduire le poids de l'image
RUN apt-get update && apt-get install -y \
    openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/run/sshd

# Création du groupe de sécurité AVANT de configurer SSH
RUN groupadd sftp_users

# Configuration de SSH :
# 1. On commente la ligne Subsystem par défaut pour éviter le conflit
# 2. On ajoute nos règles restrictives pour les utilisateurs SFTP
RUN sed -i 's/^Subsystem\tsftp/#Subsystem\tsftp/' /etc/ssh/sshd_config \
    && echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config \
    && echo "PermitRootLogin no" >> /etc/ssh/sshd_config \
    && echo "Subsystem sftp internal-sftp" >> /etc/ssh/sshd_config \
    && echo "Match Group sftp_users" >> /etc/ssh/sshd_config \
    && echo "    ChrootDirectory %h" >> /etc/ssh/sshd_config \
    && echo "    ForceCommand internal-sftp" >> /etc/ssh/sshd_config \
    && echo "    AllowTcpForwarding no" >> /etc/ssh/sshd_config \
    && echo "    X11Forwarding no" >> /etc/ssh/sshd_config

# Copie et droits d'exécution du script de démarrage
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Ouverture du port SSH standard
EXPOSE 22

# Point d'entrée de l'image
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]