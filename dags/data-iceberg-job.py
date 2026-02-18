from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor

default_args = {
    'owner': 'ddcj',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def startBatchJob():
    print("Starting batch job...")


def endBatchJob():
    print("Batch job ended.")

with DAG(
    'data-iceberg-populate',
    default_args=default_args,
    description='Submit SparkIceberg job via Spark Operator on K8s',
    schedule=None,  # Trigger manually
    tags=['spark', 'kubernetes', 'data', 'iceberg'],
    catchup=False,
) as dag:

    # Task 1: Submit the Spark Job (Apply the YAML)
    bronze_job = SparkKubernetesOperator(
        task_id='populate_bronze_table',
        namespace='artefact',
        application_file='sparkapp/data-batch-bronze-table.yml',
        kubernetes_conn_id='kubernetes_default',
    )


    # Task 2: Submit the Silver Spark Job (Apply the YAML)
    silver_job = SparkKubernetesOperator(
        task_id='populate_silver_table',
        namespace='artefact',
        application_file='sparkapp/data-batch-silver-table.yml',
        kubernetes_conn_id='kubernetes_default',
    )


    # Task 2: Submit the Silver Spark Job (Apply the YAML)
    gold_job = SparkKubernetesOperator(
        task_id='populate_gold_tables',
        namespace='artefact',
        application_file='sparkapp/data-batch-gold-tables.yml',
        kubernetes_conn_id='kubernetes_default',
    )

    start_batch_task = PythonOperator(
        task_id='start_batch_task',
        python_callable=startBatchJob
    )

    
    end_batch_task = PythonOperator(
        task_id='end_batch_task',
        python_callable=endBatchJob
    )

    start_batch_task >> bronze_job >> silver_job >> gold_job >> end_batch_task
    