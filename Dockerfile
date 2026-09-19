FROM python:3.10-slim

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU-only first for smaller footprint (~180MB instead of 2GB+)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install web dependencies
COPY requirements_docker.txt .
RUN pip install --no-cache-dir -r requirements_docker.txt

# Copy model, labels, and code
COPY bacteria_classifier_torchscript.pt .
COPY bacteria_labels.txt .
COPY web_app.py .
COPY templates/ templates/

# Expose web port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Start gunicorn web server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "web_app:app"]
