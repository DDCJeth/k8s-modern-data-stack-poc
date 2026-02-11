#!/bin/bash
set -e

echo "=== Initialisation de Superset ==="

# Initialiser la base de donnees interne de Superset
echo "[1/3] Mise a jour de la base de donnees..."
superset db upgrade

# Creer le compte admin (ignore si deja existant)
echo "[2/3] Creation du compte admin..."
superset fab create-admin \
  --username "${SUPERSET_ADMIN_USERNAME:-admin}" \
  --firstname "${SUPERSET_ADMIN_FIRST_NAME:-Admin}" \
  --lastname "${SUPERSET_ADMIN_LAST_NAME:-Admin}" \
  --email "${SUPERSET_ADMIN_EMAIL:-admin@example.com}" \
  --password "${SUPERSET_ADMIN_PASSWORD:-admin}" || true

# Initialiser les roles et permissions
echo "[3/3] Initialisation des roles et permissions..."
superset init

echo "=== Superset est pret ==="
echo "=== Demarrage du serveur sur le port 8088 ==="

# Demarrer le serveur Superset
/usr/bin/run-server.sh