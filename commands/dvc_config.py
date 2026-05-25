# Configure DVC to look at your on-premise MinIO NodePort instead of AWS S3
with dvc.config.ConfigManager(workspace_dir).edit() as conf:
    conf["remote"]["my_minio"] = {
        "url": "s3://my-dvc-bucket",
        "endpointurl": "http://<YOUR_NODE_IP>:<YOUR_NODEPORT>", # e.g., http://192.168.1.50:30005
        "access_key_id": "your_minio_access_key",
        "secret_access_key": "your_minio_secret_key"
    }
    conf["core"]["remote"] = "my_minio"

    