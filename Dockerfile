# Use Python 3.11 slim image for smaller size and security
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PORT=5000

# Install system dependencies (minimal set)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create non-root user for security
RUN addgroup --system appgroup && \
    adduser --system --group appuser && \
    mkdir -p /app/static /app/templates && \
    chown -R appuser:appgroup /app

# Copy application code with proper ownership
COPY --chown=appuser:appgroup . .

# Make start script executable
RUN chmod +x start.sh

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Use gunicorn for production
CMD ["./start.sh"]
