from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from kubernetes.client import models as k8s

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
}

with DAG(
    dag_id="docker_hub_buildkit_modern_pipeline",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["mlops", "docker", "buildkit", "future_proof"],
) as dag:

    build_and_push_image = BashOperator(
        task_id="docker_build_and_push",
        executor_config={
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            security_context=k8s.V1SecurityContext(run_as_user=0),
                            env=[
                                k8s.V1EnvVar(
                                    name="DOCKER_USER",
                                    value_from=k8s.V1EnvVarSource(
                                        secret_key_ref=k8s.V1SecretKeySelector(
                                            name="registry-credentials", key="REGISTRY_USER"
                                        )
                                    )
                                ),
                                k8s.V1EnvVar(
                                    name="DOCKER_PASSWORD",
                                    value_from=k8s.V1EnvVarSource(
                                        secret_key_ref=k8s.V1SecretKeySelector(
                                            name="registry-credentials", key="REGISTRY_PASS"
                                        )
                                    )
                                ),
                            ]
                        )
                    ]
                )
            )
        },
        bash_command="""
            echo "=== Verifying Docker & Buildx Component ==="
            docker version
            docker buildx version
            
            echo "=== Logging into Docker Hub ==="
            echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USER" --password-stdin
            
            echo "=== Preparing Build Context ==="
            cd /tmp && rm -rf context && mkdir context && cd context
            
cat <<EOF > Dockerfile
FROM python:3.10-slim
RUN echo "Building securely inside a custom Airflow worker using modern BuildKit & Buildx!"
EOF

            echo "=== Executing Modern BuildKit Build ==="
            export DOCKER_BUILDKIT=1
            IMAGE_TAG="${DOCKER_USER}/test-buildkit:latest"
            
            # Now using buildx natively with the host socket!
            docker buildx build --progress=plain -t "$IMAGE_TAG" --push .
              
            echo "=== Cleaning Up ==="
            docker logout
        """,
    )