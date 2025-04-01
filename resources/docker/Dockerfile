# Base image
FROM python:3.12-slim

RUN apt-get update && apt-get install -y git

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENV PYTHONPATH=/kube-transform/app:/kube-transform/pkg

# Set working directory
WORKDIR /kube-transform

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
RUN pip install git+https://github.com/dtoth/kube-transform.git@refactor-kt-package

COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

# Copy the application code into the container
COPY . app

# Entrypoint command will be specified in the k8s manifests
