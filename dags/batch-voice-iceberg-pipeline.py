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
    'image': 'ddcj/spark-job:omea-pocv0.1',
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
    'cdr-voice-iceberg-processing',
    default_args=default_args,
    schedule=None,
    # template_searchpath=['/usr/local/airflow/include'],
    tags=['spark', 'iceberg', 'prod', 'voice'],
    catchup=False,
) as dag:

    # --- ÉTAPE BRONZE ---
    bronze_job = SparkKubernetesOperator(
        task_id='submit_bronze',
        log_events_on_failure=True,
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-bronze.yml',
        params={**COMMON_PARAMS, 'job_name': 'voice-bronze', 'main_class': 'PopulateBronzeTable', 'input_path':'s3a://datalake/voice/', 'logType':'voice', 'table_name':'bronze.voice'}
    )


    # --- ÉTAPE SILVER ---
    silver_job = SparkKubernetesOperator(
        task_id='submit_silver',
        log_events_on_failure=True,
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-silver.yml',
        params={**COMMON_PARAMS, 'job_name': 'voice-silver', 'main_class': 'VoiceSilverTable', 'dateToProcess': '{{ ds }}', 'input_table':'bronze.voice', 'output_table':'silver.voice'}
    )

    # --- ÉTAPE GOLD ---
    gold_job = SparkKubernetesOperator(
        task_id='submit_gold',
        log_events_on_failure=True,
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-gold.yml',
        params={**COMMON_PARAMS, 'job_name': 'voice-gold', 'main_class': 'VoiceGoldTables', 'dateToProcess': '{{ ds }}', 'input_table':'silver.voice'}
    )



    # Dépendances strictes
    bronze_job >> silver_job >> gold_job