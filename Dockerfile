FROM apache/airflow:2.10.5-python3.12

USER root

# Install prerequisites for adding repositories over HTTPS
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Add the official Docker GPG key and repository layout
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg

RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install the standard Docker CLI and the modern Buildx plugin
RUN apt-get update && apt-get install -y \
    docker-ce-cli \
    docker-buildx-plugin \
    git \
    openssh-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*    

# Switch back to the standard airflow user context
USER airflow

RUN pip install --no-cache-dir \
    GitPython==3.1.43 \
    dvc[s3]==3.51.2