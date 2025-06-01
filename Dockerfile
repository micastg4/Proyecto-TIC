# scripts/Dockerfile
FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sysbench \
        default-mysql-client \
        git curl procps && \
    pip install --upgrade pip && \
    pip install jupyter matplotlib psutil && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY . .

EXPOSE 8888
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]