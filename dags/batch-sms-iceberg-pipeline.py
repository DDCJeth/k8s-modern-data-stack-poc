from datetime import datetime, timedelta
from airflow import DAG
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
    'image': 'ddcj/spark-job:omea-pocv0.4',
    'service_account': 'spark-operator-spark',
    'secret_name': 'minio-creds',
    'driver_memory': '512m',
    'driver_cores': 1,
    'executor_memory': '512m',
    'executor_cores': 1,
    'executor_instances': 1,
}


with DAG(
    'cdr-sms-iceberg-processing',
    default_args=default_args,
    schedule=None,
    # template_searchpath=['/usr/local/airflow/include'],
    tags=['spark', 'iceberg', 'prod', 'sms'],
    catchup=False,
) as dag:

    # --- ÉTAPE BRONZE ---
    bronze_job = SparkKubernetesOperator(
        task_id='submit_bronze',
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-bronze.yml',
        params={**COMMON_PARAMS, 'job_name': 'sms-bronze', 'main_class': 'PopulateBronzeTable', 'input_path':'s3a://datalake/sms/', 'logType':'sms', 'table_name':'bronze.sms'}
    )



    # --- ÉTAPE SILVER ---
    silver_job = SparkKubernetesOperator(
        task_id='submit_silver',
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-silver.yml',
        params={**COMMON_PARAMS, 'job_name': 'sms-silver', 'main_class': 'SmsSilverTable', 'dateToProcess': '{{ ds }}', 'input_table':'bronze.sms', 'output_table':'silver.sms'}
    )

    # --- ÉTAPE GOLD ---
    gold_job = SparkKubernetesOperator(
        task_id='submit_gold',
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-gold.yml',
        params={**COMMON_PARAMS, 'job_name': 'sms-gold', 'main_class': 'SmsGoldTables', 'dateToProcess': '{{ ds }}', 'input_table':'silver.sms'}
    )



    # Dépendances strictes
    bronze_job >> silver_job >> gold_job