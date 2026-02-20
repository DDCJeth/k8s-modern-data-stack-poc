# dataplateform
Dataplatform est un répertoire contenant les modules terraform pour le déploiement de la plateforme data sur EKS

## Les modules terraform sont organisés en plusieurs répertoires :
### trino : contient les modules pour le déploiement de Trino sur EKS

Trino a été mis en place dans eks avec un connecteur iceberg et un metastore postgresql en standalone sur le namespace trino.
Le connecteur iceberg permet de faire des requêtes sur des données stockées dans minio compatible S3.

Keda n'est pas déployé pour le moment sur ce module, mais il n'est pas exclu de le faire par la suite. Karpenter n'est pas déployé pour le moment sur ce module, mais il n'est pas exclu de le faire par la suite.
Keda permetterai de gérer l'auto-scaling des pods Trino en fonction des métriques de charge de travail.

Au niveau des ressources CPU/RAM, la configuration est divisé par 20par rapport à une configuration classique pour permettre de faire tourner le cluster sur un node avec des ressources limitées.

Les mots de passe ont été saisie en dûr pour simplifier le déploiement, mais il est recommandé de les stocker dans un vault ou un secret manager pour une utilisation en production.
Un compte pour se connecter à trino en M2M : - username : trino - password : trino
Un compte pour permettre à trino d'interagir avec la base de données postgresql : username : trino - password : trino123
Un compte minio pour permettre à trino de se connecter et déposer des fichiers dans minio : key : trino - secret : fK8rN2vBzQ5xLmT1WpGh
Le compte minio à accès au bucket nommé trino-data et trino-exchange

Workflow de déploiement :
 - Déploiement d'une base postgresql pour trino
 - Création des buckets et d'un utilisateur dans minio pour trino
 - Création des tables nécessaires pour trino dans la base postgresql
 - Création d'un client id / client secret dans keycloak pour trino
 - Déploiement de trino

Note : l'ordre n'est parfois pas respecté lors du déploiement fluxCD, il faudra ajouter des dépendances pour respecter l'ordre de déploiement

Les tests réalisés :
-   on utilise des exemples du blueprint pour injecter des données via la cli trino
-   on utilise des exemples du blueprint pour requeter des données via la cli trino
Pour des raisons lié au dimensionnement du cluster, les tests ont été réalisé avec une limitation sur 10 au niveau des requetes.

### airflow : contient les modules pour le déploiement d'airflow sur EKS

Airflow a été mis en place dans eks avec une base de données postgres standalone utilisant un stockage objet minio. La base de données est instancié dans le meme namespace que airflow.
Les fichiers dags sont à placé dans le bucket airflow (/opt/airflow/dags) de minio. Les pods airflow inclut un mécanisme de synchronisation pour permettre de detecter la présence d'un via l'ajout d'un sidecar dans les pods airflow.
Le sidecar permet de faire une synchronisation pour récupérer les fichiers dag dans le pod airflow.
Sans ce mécanisme mis en place, les fichiers dag ne seraient pas visible depuis l'IHM d'airflow.

Les mots de passe ont été saisie en dûr pour simplifier le déploiement, mais il est recommandé de les stocker dans un vault ou un secret manager pour une utilisation en production.
Pour la connexion à l'IHM d'airflow, c'est avec l'utilisateur enregistré dans keyclaok en oauth2
Un compte pour permettre à airflow d'interagir avec la base de données postgresql : username : airflow - password : airflow123
Un compte minio pour permettre à airflow de se connecter et déposer des fichiers dans minio : key : airflow - secret : fK8rN2vBzQ5xLmT1WpGh
Le compte minio à accès au bucket nommé airflow

Workflow de déploiement :
- Déploiement d'une base postgresql pour airflow
- Création des buckets et d'un utilisateur dans minio pour airflow
- Création d'un client id / client secret dans keycloak pour airflow
- Déploiement de airflow

Les tests réalisés :
- Ajouter un fichier dag simple dans le bucket airflow/dags et vérifier qu'il est traité par airflow (example_dag ou k8s_example_dag04)
- Lancer le dags

pour permettre de voir les logs dags dans l'ihm, il faut aller dans l'ihm airflow > admin > connections >  et ajouter les informations de connexion minio avec connection id aws_s3_conn et connection type aws
{
"aws_access_key_id": "airflow",
"aws_secret_access_key": "fK8rN2vBzQ5xLmT1WpGh",
"endpoint_url": "http://minio.minio.svc.cluster.local:9000",
"verify": "false", 
"region_name": "eu-north-1"
}

Les logs ne sont pour le moment pas envoyer dans s3, mais il est possible de le faire en configurant le logging d'airflow pour qu'il envoie les logs dans s3. Il faudra pour cela ajouter une configuration dans airflow.cfg pour configurer le remote logging et ajouter les informations de connexion à minio.

python -c "from airflow.providers.amazon.aws.hooks.s3 import S3Hook; hook = S3Hook('aws_s3_conn'); print(hook.list_keys('airflow-logs'))"