from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="test_hostpath_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["test"],
) as dag:

    hello = BashOperator(
        task_id="hello",
        bash_command="echo 'Hello from Airflow DAG on hostPath'",
    )
