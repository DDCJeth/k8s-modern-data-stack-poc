#!/bin/bash
set -e

# Vérifie si la variable SFTP_USERS est définie
if [ -n "$SFTP_USERS" ]; then
    IFS=';' read -ra USERS <<< "$SFTP_USERS"
    for USER_DATA in "${USERS[@]}"; do
        IFS=':' read -ra DETAILS <<< "$USER_DATA"
        USER=${DETAILS[0]}
        PASS=${DETAILS[1]}
        
        # Création de l'utilisateur et ajout immédiat au groupe sftp_users
        useradd -m -d "/home/$USER" -g sftp_users -s /usr/sbin/nologin "$USER"
        echo "$USER:$PASS" | chpasswd
        
        # Le dossier racine (Chroot) DOIT appartenir à root
        chown root:root "/home/$USER"
        chmod 755 "/home/$USER"
        
        # Création d'un dossier 'upload' où l'utilisateur aura le droit d'écrire
        mkdir -p "/home/$USER/upload"
        chown "$USER:sftp_users" "/home/$USER/upload"
        chmod 755 "/home/$USER/upload"
    done
fi

# Génération des clés d'hôte SSH si elles sont manquantes
ssh-keygen -A

# Lancement du daemon SSH en avant-plan (-D) et affichage des logs dans la console (-e)
exec /usr/sbin/sshd -D -e