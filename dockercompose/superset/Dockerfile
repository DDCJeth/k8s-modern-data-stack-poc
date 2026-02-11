FROM apache/superset:latest

# Passer en root pour installer les dependances
USER root

# Installer le driver Trino dans le virtualenv de Superset
RUN pip install --no-cache-dir --target /app/.venv/lib/python3.10/site-packages trino sqlalchemy-trino

# Copier le script d'initialisation
COPY superset-init.sh /app/superset-init.sh
RUN chmod +x /app/superset-init.sh

# Revenir a l'utilisateur superset
USER superset

# Lancer l'init puis demarrer Superset
ENTRYPOINT ["/app/superset-init.sh"]