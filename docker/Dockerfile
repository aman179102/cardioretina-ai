FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[dev]" 2>/dev/null || pip install --no-cache-dir .

COPY . .

RUN mkdir -p uploads gradcam_outputs checkpoints outputs logs

ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV ENVIRONMENT=production
ENV LOG_LEVEL=INFO

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "cardioretina.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
