from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id="test_taskflow_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["test"],
)
def test_hostpath_dag():

    @task.bash
    def hello():
        return "echo 'Hello from Airflow DAG on hostPath'"

    hello()

test_hostpath_dag()