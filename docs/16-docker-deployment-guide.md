# Docker Deployment Guide

## Overview

This guide explains how to deploy CardioRetina-AI using Docker containers for consistent, portable deployment.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+ (optional, for compose deployment)
- 4GB+ available RAM
- 10GB+ available disk space

## Quick Start

### Using Docker Compose (Recommended)

```bash
cd docker/
docker compose up --build
```

Access the application at: `http://localhost:8000/`

### Using Docker Directly

```bash
# Build image
docker build -f docker/Dockerfile -t cardioretina-ai .

# Run container
docker run -p 8000:8000 cardioretina-ai
```

## Docker Compose Configuration

### File: `docker/docker-compose.yml`

```yaml
version: '3.8'

services:
  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - MODEL_CHECKPOINT=/app/checkpoints/best_model.pt
      - LOG_LEVEL=info
    volumes:
      - ./checkpoints:/app/checkpoints:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### GPU Support

For GPU-accelerated inference, uncomment in `docker-compose.yml`:

```yaml
services:
  api:
    # ... other config
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

Requires NVIDIA Docker runtime.

## Dockerfile Structure

### Multi-Stage Build

```dockerfile
# Stage 1: Build dependencies
FROM python:3.10-slim as builder

WORKDIR /app
COPY pyproject.toml .
RUN pip install --user -e ".[dev]"

# Stage 2: Runtime image
FROM python:3.10-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "cardioretina.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Volume Mounts

Mount these directories for persistence:

| Host Path | Container Path | Purpose | Mode |
|-----------|---------------|---------|------|
| `./checkpoints` | `/app/checkpoints` | Model files | Read-only |
| `./data` | `/app/data` | Dataset | Read-only |
| `./outputs` | `/app/outputs` | Results | Read-write |

### Example with Volumes

```bash
docker run \
    -p 8000:8000 \
    -v $(pwd)/checkpoints:/app/checkpoints:ro \
    -v $(pwd)/data:/app/data:ro \
    -v $(pwd)/outputs:/app/outputs \
    cardioretina-ai
```

## Environment Variables

Configure via environment:

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_CHECKPOINT` | `checkpoints/best_model.pt` | Path to model |
| `LOG_LEVEL` | `info` | Logging verbosity |
| `DEVICE` | `auto` | cuda/cpu/auto |
| `BATCH_SIZE` | `32` | Inference batch size |
| `MAX_WORKERS` | `4` | Uvicorn workers |

### Example with Environment Variables

```bash
docker run \
    -p 8000:8000 \
    -e MODEL_CHECKPOINT=/app/checkpoints/my_model.pt \
    -e LOG_LEVEL=debug \
    -e DEVICE=cuda \
    cardioretina-ai
```

## Production Deployment

### With Load Balancer

```yaml
version: '3.8'

services:
  api-1:
    build: .
    ports:
      - "8001:8000"
  
  api-2:
    build: .
    ports:
      - "8002:8000"
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api-1
      - api-2
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cardioretina-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cardioretina-ai
  template:
    metadata:
      labels:
        app: cardioretina-ai
    spec:
      containers:
        - name: api
          image: cardioretina-ai:latest
          ports:
            - containerPort: 8000
          resources:
            requests:
              memory: "2Gi"
              cpu: "1000m"
            limits:
              memory: "4Gi"
              cpu: "2000m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
```

## Building Custom Images

### With Specific Model

```dockerfile
FROM cardioretina-ai:base

# Copy custom model
COPY my_model.pt /app/checkpoints/model.pt

ENV MODEL_CHECKPOINT=/app/checkpoints/model.pt
```

Build:
```bash
docker build -t cardioretina-ai:custom -f Dockerfile.custom .
```

### Minimal Runtime Image

```dockerfile
FROM python:3.10-slim

# Install only runtime dependencies
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install fastapi uvicorn pillow numpy pandas

COPY cardioretina/ /app/cardioretina/
COPY checkpoints/best_model.pt /app/checkpoints/

WORKDIR /app

EXPOSE 8000
CMD ["uvicorn", "cardioretina.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Monitoring and Logging

### View Logs

```bash
# Docker logs
docker logs cardioretina-ai-container

# Follow logs
docker logs -f cardioretina-ai-container

# Compose logs
docker compose logs -f
```

### Health Checks

Built-in health check at `/health`:
```bash
curl http://localhost:8000/health
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Container exits immediately | Check logs: `docker logs <container>` |
| Model not found | Verify volume mount and MODEL_CHECKPOINT path |
| Out of memory | Increase container memory limit |
| Port already in use | Change port mapping: `-p 8080:8000` |
| Slow startup | Normal for first run (model loading) |
| GPU not available | Install nvidia-docker-runtime |

## Security Considerations

### Non-Root User

Run container as non-root:

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### Read-Only Root Filesystem

```bash
docker run --read-only \
    --tmpfs /tmp \
    --tmpfs /var/tmp \
    cardioretina-ai
```

### Resource Limits

```bash
docker run \
    --memory=4g \
    --cpus=2.0 \
    --pids-limit=100 \
    cardioretina-ai
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t cardioretina-ai:${{ github.sha }} .
      
      - name: Test container
        run: |
          docker run -d -p 8000:8000 cardioretina-ai:${{ github.sha }}
          sleep 10
          curl -f http://localhost:8000/health
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push cardioretina-ai:${{ github.sha }}
```

## Cleanup

```bash
# Stop and remove containers
docker compose down

# Remove images
docker rmi cardioretina-ai

# Prune unused volumes
docker volume prune

# Full cleanup
docker system prune -a
```

---

*Docker deployment ensures consistent, reproducible environments across development and production.*
