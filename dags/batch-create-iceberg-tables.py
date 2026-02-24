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
    'image': 'ddcj/spark-job:omea-pocv0.3',
    'service_account': 'spark-operator-spark',
    'secret_name': 'minio-creds',
    'driver_memory': '512m',
    'driver_cores': 1,
    'executor_memory': '512m',
    'executor_cores': 1,
    'executor_instances': 1,
}


with DAG(
    'create-iceberg-tables',
    default_args=default_args,
    schedule=None,
    tags=['spark', 'iceberg', 'prod', 'bronze', 'tables', 'creation'],
    catchup=False,
) as dag:

    # --- ÉTAPE BRONZE ---
    voice_table = SparkKubernetesOperator(
        task_id='voice_table',
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-createTable.yml',
        params={**COMMON_PARAMS, 'job_name': 'voice-bronze', 'main_class': 'CreateIcebergTable', 'schema_base_path':'s3a://datalake/schemas/', 'logType':'voice'}
    )


    # --- ÉTAPE SILVER ---
    data_table = SparkKubernetesOperator(
        task_id='data_table',
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-createTable.yml',
        params={**COMMON_PARAMS, 'job_name': 'data-bronze', 'main_class': 'CreateIcebergTable', 'schema_base_path':'s3a://datalake/schemas/', 'logType':'data'}
    )

    # --- ÉTAPE GOLD ---
    sms_table = SparkKubernetesOperator(
        task_id='sms_table',
        namespace=COMMON_PARAMS['namespace'],
        application_file='batch-template-createTable.yml',
        params={**COMMON_PARAMS, 'job_name': 'sms-bronze', 'main_class': 'CreateIcebergTable', 'schema_base_path':'s3a://datalake/schemas/', 'logType':'sms'}
    )


    # Dépendances
    [voice_table, data_table, sms_table]
    
