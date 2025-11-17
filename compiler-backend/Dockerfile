# Online Code Runner - Backend Compiler Service
# Multi-stage build for security and optimization

FROM python:3.11-slim AS base

# Install compilers and build tools
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash coderunner

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Change ownership to non-root user
RUN chown -R coderunner:coderunner /app

# Create temp directory for code execution
RUN mkdir -p /tmp/code_runner && chown coderunner:coderunner /tmp/code_runner

# Switch to non-root user
USER coderunner

# Expose port (Railway/Render will use PORT env var)
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/').read()"

# Run the application
CMD ["python", "app.py"]
