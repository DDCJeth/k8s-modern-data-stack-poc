from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor

default_args = {
    'owner': 'ddcj',
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Configuration commune pour éviter la répétition
COMMON_PARAMS = {
    'namespace': 'artefact',
    'image': 'ddcj/spark-job:omea-pocv0.1',
    'service_account': 'spark-operator-spark',
    'secret_name': 'minio-creds',
    'driver_memory': '512m',
    'driver_cores': 1,
    'executor_memory': '512m',
    'executor_cores': 1,
    'executor_instances': 1,
}


with DAG(
    'data-iceberg-industrialized',
    default_args=default_args,
    schedule=None,
    # template_searchpath=['/usr/local/airflow/include'],
    tags=['spark', 'iceberg', 'prod'],
    catchup=False,
) as dag:

    # --- ÉTAPE BRONZE ---
    bronze_job = SparkKubernetesOperator(
        task_id='submit_bronze',
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-bronze.yml',
        params={**COMMON_PARAMS, 'job_name': 'data-bronze', 'main_class': 'PopulateBronzeTable', 'input_path':'s3a://datalake/data/', 'logType':'data', 'table_name':'bronze.data'}
    )

    # Le Sensor attend que le job Kubernetes atteigne l'état "Succeeded"
    monitor_bronze = SparkKubernetesSensor(
        task_id='monitor_bronze',
        namespace=COMMON_PARAMS['namespace'],
        application_name="{{ task_instance.xcom_pull(task_ids='submit_bronze')['metadata']['name'] }}",
        kubernetes_conn_id='kubernetes_default',
        poke_interval=30,  # Vérifie toutes les 30 secondes
        timeout=3600       # Timeout après 1h
    )

    # --- ÉTAPE SILVER ---
    silver_job = SparkKubernetesOperator(
        task_id='submit_silver',
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-silver.yml',
        params={**COMMON_PARAMS, 'job_name': 'data-silver', 'main_class': 'DataSilverTable', 'dateToProcess': '{{ ds }}', 'input_table':'bronze.data', 'output_table':'silver.data'}
    )

    monitor_silver = SparkKubernetesSensor(
        task_id='monitor_silver',
        namespace=COMMON_PARAMS['namespace'],
        application_name="{{ task_instance.xcom_pull(task_ids='submit_silver')['metadata']['name'] }}",
        kubernetes_conn_id='kubernetes_default',
        poke_interval=30
    )


    # --- ÉTAPE GOLD ---
    gold_job = SparkKubernetesOperator(
        task_id='submit_gold',
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-gold.yml',
        params={**COMMON_PARAMS, 'job_name': 'data-gold', 'main_class': 'DataGoldTables', 'dateToProcess': '{{ ds }}', 'input_table':'silver.data'}
    )

    monitor_gold = SparkKubernetesSensor(
        task_id='monitor_gold',
        namespace=COMMON_PARAMS['namespace'],
        application_name="{{ task_instance.xcom_pull(task_ids='submit_gold')['metadata']['name'] }}",
        kubernetes_conn_id='kubernetes_default',
        poke_interval=30
    )


    # Dépendances strictes
    bronze_job >> monitor_bronze >> silver_job >> monitor_silver >> gold_job >> monitor_gold