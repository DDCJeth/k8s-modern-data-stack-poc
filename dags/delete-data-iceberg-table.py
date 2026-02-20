from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor

default_args = {
    'owner': 'ddcj',
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Configuration commune pour éviter la répétition
COMMON_PARAMS = {
    'namespace': 'airflow',
    'image': 'ddcj/spark-job:omea-pocv0.2',
    'service_account': 'spark-operator-spark',
    'secret_name': 'minio-creds',
    'driver_memory': '512m',
    'driver_cores': 1,
    'executor_memory': '512m',
    'executor_cores': 1,
    'executor_instances': 1,
    'minio_region': 'eu-north-1',
    'minio_access_key': Variable.get("minio_access_key"),
    'minio_secret_key': Variable.get("minio_secret_key"),
}


with DAG(
    'delete-data-iceberg-tables',
    default_args=default_args,
    schedule=None,
    # template_searchpath=['/usr/local/airflow/include'],
    tags=['spark', 'iceberg', 'prod', 'data'],
    catchup=False,
) as dag:

    # --- ÉTAPE BRONZE ---
    bronze_table = SparkKubernetesOperator(
        task_id='delete_bronze',
        log_events_on_failure=True,
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-deleteTable.yml',
        params={**COMMON_PARAMS, 'job_name': 'delete-data-bronze', 'main_class': 'DropIcebergTable', 'schema':'bronze', 'logType':'data'}
    )


    # --- ÉTAPE SILVER ---
    silver_table = SparkKubernetesOperator(
        task_id='delete_silver',
        log_events_on_failure=True,
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-deleteTable.yml',
        params={**COMMON_PARAMS, 'job_name': 'delete-data-silver', 'main_class': 'DropIcebergTable', 'schema': 'silver', 'logType':'data'}
    )

    # --- ÉTAPE GOLD 1---
    gold_table = SparkKubernetesOperator(
        task_id='delete_gold',
        log_events_on_failure=True,
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-deleteTable.yml',
        params={**COMMON_PARAMS, 'job_name': 'delete-data-gold', 'main_class': 'DropIcebergTable', 'schema': 'gold', 'logType':'data_daily_global_kpis'}
    )

    # --- ÉTAPE GOLD 2---
    gold_tower_table = SparkKubernetesOperator(
        task_id='delete_gold_tower',
        log_events_on_failure=True,
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-deleteTable.yml',
        params={**COMMON_PARAMS, 'job_name': 'delete-data-gold-tower', 'main_class': 'DropIcebergTable', 'schema': 'gold', 'logType':'data_daily_tower_kpis'}
    )


    # Dépendances strictes
    bronze_table >> silver_table >> gold_table >> gold_tower_table