from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,  # Fail fast for diagnosis
}

with DAG(
    dag_id="test_git_ssh_authentication",
    default_args=default_args,
    description="Diagnostics to verify SSH keys and Git cloning on KubernetesExecutor",
    schedule_interval=None,  # Manual trigger only
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["testing", "ssh", "git"],
) as dag:

    # 1. Perform an actual isolated test clone 
    test_git_checkout = BashOperator(
        task_id="test_repo_checkout",
        bash_command="""
            echo "=== Starting Dry Run Repo Clone ==="
            rm -rf /tmp/test_clone
            
            git clone --depth 1 git@github.com:yuanDataScience/airflow_K8s.git /tmp/test_clone
            
            echo "=== Success! Contents of cloned root: ==="
            ls -la /tmp/test_clone
        """,
    )

    # 2. Test if the DVC CLI executable is present in the runtime container
    check_dvc_installation = BashOperator(
        task_id="check_dvc_version",
        bash_command="dvc --version",
    )

    # 3. Test system environment visibility (Verify user, paths, and configurations)
    check_environment = BashOperator(
        task_id="check_system_environment",
        bash_command="""
            echo "=== Current User ===" && whoami && \
            echo "=== Global DVC Config Location ===" && dvc config --global -l || echo "No global config set"
        """,
    )

    # 4. Optional placeholder: Try initializing a dummy dvc repo or checking status
    # This checks if storage permissions/cache mounts are functioning.
    check_dvc_status = BashOperator(
        task_id="check_dvc_status",
        bash_command="""
            mkdir -p /tmp/dvc_test && cd /tmp/dvc_test && \
            git init --quiet && \
            dvc init --no-scm --quiet && \
            dvc status
        """,
    )

    test_git_checkout >> check_dvc_installation >> check_environment >> check_dvc_status
