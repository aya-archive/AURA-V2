# Dockerfile for Background Agents
# This Dockerfile provides a development environment for background agents
# It includes all necessary development tools without copying application code
# (code will be cloned by the agent during execution)
#
# Key Features:
# - Non-root user for security
# - Comprehensive development toolchain
# - Python and Node.js ecosystems
# - Optimized for background agent workflows

# Use Ubuntu as base image for stability and compatibility
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
ENV NODE_ENV=development

# Update package lists and install essential development tools
# Grouped by functionality for better layer caching
RUN apt-get update && apt-get install -y \
    # Basic system tools
    curl \
    wget \
    git \
    vim \
    nano \
    unzip \
    zip \
    tar \
    gzip \
    # Build essentials for compiling native modules
    build-essential \
    gcc \
    g++ \
    make \
    # Python development tools
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    # Additional useful tools
    jq \
    tree \
    htop \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js using NodeSource repository for latest LTS
# This is separated to improve layer caching
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
# This follows the recommended pattern for background agents
RUN useradd -m -s /bin/bash ubuntu

# Set the user and working directory
# This is the recommended setup for background agents
USER ubuntu
WORKDIR /home/ubuntu

# Set up user environment and shell configuration
# This ensures proper PATH and environment setup
RUN echo 'export PATH=$PATH:/home/ubuntu/.local/bin' >> /home/ubuntu/.bashrc \
    && echo 'export NODE_ENV=development' >> /home/ubuntu/.bashrc

# Install common Python packages globally for the user
# These packages support the A.U.R.A AI model development workflow
RUN pip3 install --user \
    requests \
    numpy \
    pandas \
    matplotlib \
    jupyter \
    pytest \
    black \
    flake8 \
    # Additional packages for A.U.R.A AI model development
    scikit-learn \
    xgboost \
    prophet \
    joblib \
    sweetviz \
    streamlit \
    plotly

# Install common Node.js packages globally
# These support the frontend and development workflow
RUN npm install -g \
    typescript \
    ts-node \
    nodemon \
    eslint \
    prettier \
    jest

# Set default shell for consistent environment
SHELL ["/bin/bash", "-c"]

# Add healthcheck for container monitoring
# This helps ensure the container is running properly
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)" || exit 1

# Expose common development ports (can be overridden)
# These ports support the A.U.R.A application stack
EXPOSE 3000 8000 8080 5000

# Set default command
# This provides an interactive shell for background agents
CMD ["/bin/bash"]
