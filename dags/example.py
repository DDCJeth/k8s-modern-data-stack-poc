from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'spark_pi_k8s_job',
    default_args=default_args,
    description='Submit SparkPi job via Spark Operator on K8s',
    schedule=None,  # Trigger manually
    tags=['spark', 'kubernetes'],
    catchup=False,
) as dag:

    # Task 1: Submit the Spark Job (Apply the YAML)
    submit_job = SparkKubernetesOperator(
        task_id='submit_spark_pi',
        namespace='default',
        application_file='spark-pi.yaml', # Path relative to your DAGs folder
        kubernetes_conn_id='kubernetes_default',
        do_xcom_push=True,
    )

    # Task 2: Monitor the Job (Wait for completion)
    monitor_job = SparkKubernetesSensor(
        task_id='monitor_spark_pi',
        namespace='default',
        application_name="{{ task_instance.xcom_pull(task_ids='submit_spark_pi')['metadata']['name'] }}",
        kubernetes_conn_id='kubernetes_default',
        attach_log=True # Streams Spark driver logs to Airflow
    )

    submit_job >> monitor_job