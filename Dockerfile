# A.U.R.A (AI-Unified Retention Analytics) - Main Application Dockerfile
# This Dockerfile creates a production-ready container for the A.U.R.A platform
# It includes the complete data pipeline, AI models, and Streamlit dashboard

# Use Python 3.11 slim image as base for optimal performance and security
FROM python:3.11-slim

# Set environment variables for Python and application
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies required for data processing and AI libraries
RUN apt-get update && apt-get install -y \
    # Essential build tools for compiling Python packages
    build-essential \
    gcc \
    g++ \
    make \
    # Required for data processing libraries
    libgomp1 \
    libgfortran5 \
    # Required for visualization libraries
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    # Required for Prophet forecasting model
    libatlas-base-dev \
    # Required for system monitoring and debugging
    htop \
    curl \
    # Clean up to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash aura
USER aura
WORKDIR /home/aura/app

# Copy requirements first for better Docker layer caching
COPY --chown=aura:aura requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application source code
COPY --chown=aura:aura . .

# Create necessary directories for data pipeline (Medallion architecture)
RUN mkdir -p data/bronze data/silver data/gold data/temp \
    && mkdir -p models/forecasting models/decision_engine models/chatbot \
    && mkdir -p uploads logs

# Set proper permissions for data directories
RUN chmod -R 755 data/ models/ uploads/ logs/

# Expose Streamlit port
EXPOSE 8501

# Health check to ensure the application is running properly
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Set default command to run the Streamlit application
CMD ["streamlit", "run", "src/dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]

# Add labels for better container management
LABEL maintainer="A.U.R.A Team" \
      version="1.0" \
      description="AI-Unified Retention Analytics Platform" \
      org.opencontainers.image.title="A.U.R.A" \
      org.opencontainers.image.description="AI-powered platform for client monitoring, churn prediction, and retention strategy optimization"
