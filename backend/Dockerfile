# Multi-stage build for production
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim as production

# Create non-root user
RUN groupadd -r synthai && useradd -r -g synthai synthai

# Create application directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY src/ ./src/
COPY run.py .

# Create necessary directories
RUN mkdir -p /app/logs /app/models && \
    chown -R synthai:synthai /app

# Switch to non-root user
USER synthai

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["gunicorn", "src.app:create_app()", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]

# Development stage
FROM production as development

USER root

# Install development tools
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Install debugpy for remote debugging
RUN pip install debugpy

USER synthai

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "8000"]
